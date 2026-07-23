import os
import pandas as pd
from datetime import date
import logging
from app.config import get_settings
from app.services.etl.government_collector import get_severity

logger = logging.getLogger(__name__)
settings = get_settings()

LAT_MIN, LAT_MAX = -6.5, -6.08
LON_MIN, LON_MAX = 106.5, 107.2

def collect_scraped_news_data(filename="data_rawan_hasil_scraping_jakarta.xlsx") -> list[dict]:
    file_path = os.path.join(settings.data_dir, filename)
    
    if not os.path.exists(file_path):
        logger.warning(f"Scraped news file not found: {file_path}")
        return []

    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip().str.lower()
    
    records = []
    for _, row in df.iterrows():
        try:
            lat = float(row.get("latitude", 0)) if pd.notnull(row.get("latitude")) else None
            lon = float(row.get("longitude", 0)) if pd.notnull(row.get("longitude")) else None
            
            if lat is not None and lon is not None:
                if not (LAT_MIN <= lat <= LAT_MAX) or not (LON_MIN <= lon <= LON_MAX):
                    lat = None
                    lon = None
                    
            incident_type = str(row.get("jenis_rawan", "GANGGUAN KETERTIBAN")).strip().upper()
            year_val = row.get("periode_data")
            year = int(float(year_val)) if pd.notnull(year_val) else 2025
            
            source_val = str(row.get("sumber_berita", "news_scraping"))
            url_val = str(row.get("link_berita", ""))
            if url_val == "nan": url_val = None
            
            record = {
                "incident_date": date(year, 1, 1),
                "incident_year": year,
                "location_name": f"{str(row.get('kelurahan', '')).strip()}, {str(row.get('kecamatan', '')).strip()}",
                "district": str(row.get("wilayah", "")).strip().upper(),
                "subdistrict": str(row.get("kecamatan", "")).strip().upper(),
                "incident_type": incident_type,
                "severity_score": get_severity(incident_type),
                "source": source_val,
                "article_url": url_val,
                "latitude": lat,
                "longitude": lon,
            }
            records.append(record)
        except Exception as e:
            continue
            
    return records
