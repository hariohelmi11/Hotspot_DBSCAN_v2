import logging
import time
from typing import Optional
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

logger = logging.getLogger(__name__)

_geocoder = Nominatim(user_agent="hotspot-gis-jakarta/1.0", timeout=10)

# Jakarta bounding box
LAT_MIN, LAT_MAX = -6.5, -6.08
LON_MIN, LON_MAX = 106.5, 107.2


def geocode_address(address: str, retries: int = 3) -> Optional[tuple[float, float]]:
    """Geocode address using Nominatim. Returns (lat, lon) or None."""
    for attempt in range(retries):
        try:
            location = _geocoder.geocode(
                f"{address}, Jakarta, Indonesia",
                country_codes="id",
                viewbox=[
                    (-5.9, 106.5),
                    (-6.5, 107.2),
                ],
                bounded=True,
            )
            if location:
                lat, lon = location.latitude, location.longitude
                if LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX:
                    return lat, lon
            return None
        except GeocoderTimedOut:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
        except GeocoderServiceError as e:
            logger.error(f"Geocoder service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Geocoding unexpected error: {e}")
            return None
    return None


def geocode_records(records: list[dict]) -> list[dict]:
    """
    Geocode records missing coordinates.
    Respects Nominatim 1 req/s rate limit.
    """
    result = []
    for record in records:
        if record.get("latitude") and record.get("longitude"):
            result.append(record)
            continue

        address = _build_address(record)
        if not address:
            result.append(record)
            continue

        coords = geocode_address(address)
        if coords:
            record["latitude"], record["longitude"] = coords
            logger.debug(f"Geocoded '{address}' → {coords}")
        else:
            logger.warning(f"Could not geocode: '{address}'")

        result.append(record)
        time.sleep(1.1)  # Nominatim policy: max 1 req/s

    return result


def _build_address(record: dict) -> Optional[str]:
    parts = []
    if record.get("location_name"):
        parts.append(record["location_name"])
    elif record.get("subdistrict"):
        parts.append(record["subdistrict"])
    if record.get("district"):
        parts.append(record["district"])
    return ", ".join(parts) if parts else None
