import logging
from sqlalchemy.orm import Session
from geoalchemy2.elements import WKTElement
from app.services.etl.government_collector import collect_government_data
from app.services.etl.news_collector import collect_news_data
from app.services.etl.scraped_news_collector import collect_scraped_news_data
from app.services.etl.cleaner import batch_clean
from app.services.etl.geocoder import geocode_records
from app.repositories.incident_repository import IncidentRepository
from app.models.scrape_log import ScrapeLog

logger = logging.getLogger(__name__)


def run_etl_pipeline(db: Session, source: str = "all", year: int = 2024) -> dict:
    """
    Run ETL pipeline.
    source: 'government' | 'news' | 'all'
    """
    results: dict = {"records_inserted": 0, "errors": []}
    repo = IncidentRepository(db)
    raw_records: list[dict] = []

    # --- Extract ---
    if source in ("government", "all"):
        try:
            gov_records = collect_government_data()
            raw_records.extend(gov_records)
            logger.info(f"Government data: {len(gov_records)} records")
            _log_scrape(db, "pemerintah", len(gov_records), True)
        except Exception as e:
            logger.error(f"Government collection failed: {e}")
            _log_scrape(db, "pemerintah", 0, False, str(e))
            results["errors"].append(f"government: {e}")

    if source in ("news", "all"):
        for news_year in [2025, 2026]:
            try:
                news_recs = collect_news_data(news_year)
                raw_records.extend(news_recs)
                logger.info(f"News {news_year}: {len(news_recs)} records")
                _log_scrape(db, f"news_{news_year}", len(news_recs), True)
            except Exception as e:
                logger.error(f"News {news_year} failed: {e}")
                _log_scrape(db, f"news_{news_year}", 0, False, str(e))
                results["errors"].append(f"news_{news_year}: {e}")
        
        # Ingest pre-scraped news from Excel
        try:
            scraped_recs = collect_scraped_news_data()
            raw_records.extend(scraped_recs)
            logger.info(f"Scraped News (Excel): {len(scraped_recs)} records")
            _log_scrape(db, "scraped_news_excel", len(scraped_recs), True)
        except Exception as e:
            logger.error(f"Scraped news (Excel) collection failed: {e}")
            _log_scrape(db, "scraped_news_excel", 0, False, str(e))
            results["errors"].append(f"scraped_news_excel: {e}")

    # --- Transform ---
    cleaned = batch_clean(raw_records)
    logger.info(f"After cleaning/dedup: {len(cleaned)} records")

    # Separate records: those with coords vs those needing geocoding
    with_coords = [r for r in cleaned if r.get("latitude") and r.get("longitude")]
    without_coords = [r for r in cleaned if not r.get("latitude") or not r.get("longitude")]

    logger.info(f"With coords: {len(with_coords)}, needs geocoding: {len(without_coords)}")
    geocoded = geocode_records(without_coords)

    all_records = with_coords + geocoded
    valid = [r for r in all_records if r.get("latitude") and r.get("longitude")]
    logger.info(f"Valid records for insert: {len(valid)}")

    # --- Load ---
    insert_records = []
    for record in valid:
        wkt = f"POINT({record['longitude']} {record['latitude']})"
        record["geom"] = WKTElement(wkt, srid=4326)
        record.setdefault("hotspot_cluster_id", None)
        insert_records.append(record)

    if insert_records:
        from app.models.incident import PublicOrderIncident
        
        # Prevent duplicates by deleting existing records for the extracted sources
        sources = list(set(r.get("source") for r in insert_records if r.get("source")))
        if sources:
            db.query(PublicOrderIncident).filter(PublicOrderIncident.source.in_(sources)).delete(synchronize_session=False)
            db.commit()

        repo.bulk_insert(insert_records)
        results["records_inserted"] = len(insert_records)
        logger.info(f"Inserted {len(insert_records)} records")

    return results


def _log_scrape(db: Session, source: str, total: int, success: bool, error: str = None):
    log = ScrapeLog(source=source, total_records=total, success=success, error_message=error)
    db.add(log)
    db.commit()
