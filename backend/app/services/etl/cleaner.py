from datetime import date
from typing import Optional


def clean_record(record: dict) -> Optional[dict]:
    """Validate and clean a single incident record. Returns None if invalid."""
    if not record.get("incident_type"):
        return None

    # Normalize strings
    for field in ("location_name", "district", "subdistrict", "incident_type", "source"):
        if record.get(field):
            record[field] = str(record[field]).strip()

    record["incident_type"] = record["incident_type"].upper()

    if record.get("district"):
        record["district"] = record["district"].upper()
    if record.get("subdistrict"):
        record["subdistrict"] = record["subdistrict"].upper()

    # Ensure incident_date
    if not record.get("incident_date"):
        year = record.get("incident_year", 2024)
        record["incident_date"] = date(year, 1, 1)

    # Ensure incident_year
    if not record.get("incident_year") and record.get("incident_date"):
        record["incident_year"] = record["incident_date"].year

    # Clamp severity
    score = record.get("severity_score", 2)
    record["severity_score"] = max(1, min(5, int(score) if score else 2))

    return record


def deduplicate(records: list[dict]) -> list[dict]:
    """Remove duplicates based on district + subdistrict + type + year + coords."""
    seen: set = set()
    unique: list[dict] = []
    for record in records:
        key = (
            str(record.get("district", "")).upper(),
            str(record.get("subdistrict", "")).upper(),
            str(record.get("incident_type", "")).upper(),
            record.get("incident_year"),
            round(float(record.get("latitude") or 0), 4),
            round(float(record.get("longitude") or 0), 4),
        )
        if key not in seen:
            seen.add(key)
            unique.append(record)
    return unique


def batch_clean(records: list[dict]) -> list[dict]:
    cleaned = [clean_record(r) for r in records]
    cleaned = [r for r in cleaned if r is not None]
    return deduplicate(cleaned)
