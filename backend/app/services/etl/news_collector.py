import logging
import httpx
from bs4 import BeautifulSoup
from datetime import date
from typing import Optional
from app.services.etl.government_collector import get_severity

logger = logging.getLogger(__name__)

SCRAPING_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8",
}

KEYWORDS = [
    "tawuran jakarta",
    "gangguan ketertiban umum jakarta",
    "kerawanan wilayah jakarta",
    "kriminalitas jakarta",
]

JAKARTA_DISTRICTS = [
    "JAKARTA PUSAT",
    "JAKARTA BARAT",
    "JAKARTA TIMUR",
    "JAKARTA SELATAN",
    "JAKARTA UTARA",
]

SOURCES = [
    {
        "name": "detik",
        "search_url": "https://www.detik.com/search/searchall",
        "params": {"query": "{keyword}"},
        "article_selector": "article.list-content__item",
        "title_selector": "h3.media__title",
        "link_selector": "a",
    },
    {
        "name": "kompas",
        "search_url": "https://search.kompas.com/search/",
        "params": {"q": "{keyword}"},
        "article_selector": "div.article__asset",
        "title_selector": "h2.article__title",
        "link_selector": "a",
    },
]


def collect_news_data(year: int) -> list[dict]:
    """Scrape news articles for a given year. Returns incident records."""
    records: list[dict] = []
    for source in SOURCES:
        try:
            source_records = _scrape_source(source, year)
            records.extend(source_records)
            logger.info(f"[{source['name']}] Collected {len(source_records)} records for {year}")
        except Exception as e:
            logger.error(f"[{source['name']}] Scraping failed for {year}: {e}")
    return records


def _scrape_source(source_cfg: dict, year: int) -> list[dict]:
    records: list[dict] = []
    for keyword in KEYWORDS:
        try:
            params = {
                k: v.replace("{keyword}", keyword)
                for k, v in source_cfg["params"].items()
            }
            with httpx.Client(timeout=30, headers=SCRAPING_HEADERS, follow_redirects=True) as client:
                response = client.get(source_cfg["search_url"], params=params)
                response.raise_for_status()
            articles = _parse_articles(
                html=response.text,
                source_name=source_cfg["name"],
                article_sel=source_cfg["article_selector"],
                title_sel=source_cfg["title_selector"],
                link_sel=source_cfg["link_selector"],
                year=year,
            )
            records.extend(articles)
        except Exception as e:
            logger.warning(f"[{source_cfg['name']}] keyword='{keyword}': {e}")
    return records


def _parse_articles(
    html: str,
    source_name: str,
    article_sel: str,
    title_sel: str,
    link_sel: str,
    year: int,
) -> list[dict]:
    records: list[dict] = []
    soup = BeautifulSoup(html, "lxml")
    articles = soup.select(article_sel) or soup.find_all("article")

    for article in articles[:20]:
        try:
            title_tag = article.select_one(title_sel) or article.find(["h2", "h3", "h4"])
            title = title_tag.get_text(strip=True) if title_tag else ""
            if not title or not _is_relevant(title):
                continue

            link_tag = article.select_one(link_sel) or article.find("a", href=True)
            url = link_tag["href"] if link_tag and link_tag.get("href") else None

            incident_type = _classify_incident(title)
            district = _extract_district(title)

            records.append({
                "incident_date": date(year, 1, 1),
                "incident_year": year,
                "location_name": district or "DKI JAKARTA",
                "district": district,
                "subdistrict": None,
                "incident_type": incident_type,
                "severity_score": get_severity(incident_type),
                "source": source_name,
                "article_url": url,
                "latitude": None,
                "longitude": None,
            })
        except Exception:
            continue
    return records


def _is_relevant(title: str) -> bool:
    keywords = [
        "tawuran", "ketertiban", "kriminal", "geng",
        "premanisme", "narkoba", "jakart", "gangguan",
    ]
    title_lower = title.lower()
    return any(kw in title_lower for kw in keywords)


def _classify_incident(title: str) -> str:
    t = title.lower()
    if "tawuran" in t:
        return "TAWURAN"
    elif "narkoba" in t or "kriminal" in t or "pencurian" in t:
        return "KRIMINALITAS"
    elif "premanisme" in t or "geng" in t:
        return "PREMANISME"
    elif "miras" in t:
        return "MIRAS"
    elif "pkl" in t or "pedagang" in t:
        return "PKL"
    else:
        return "GANGGUAN KETERTIBAN"


def _extract_district(title: str) -> Optional[str]:
    for district in JAKARTA_DISTRICTS:
        if district.lower() in title.lower():
            return f"KOTA ADM. {district}"
    if "jakarta" in title.lower():
        return "DKI JAKARTA"
    return None
