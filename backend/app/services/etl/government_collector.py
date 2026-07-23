import os
import pandas as pd
from datetime import date
from app.config import get_settings

settings = get_settings()

# Raw coordinates in data-rawan.xls are stored as integer × 1,000,000
# e.g. -6170529 → -6.170529, 106819195 → 106.819195
COORDINATE_SCALE = 1_000_000

# Jakarta bounding box for validation
LAT_MIN, LAT_MAX = -6.5, -5.9
LON_MIN, LON_MAX = 106.5, 107.2


def get_severity(incident_type: str) -> int:
    upper = incident_type.upper()
    if "TAWURAN" in upper:
        return 5
    elif any(k in upper for k in ("KRIMINALITAS", "PREMANISME", "NARKOBA", "PENODONGAN", "PENCURIAN")):
        return 4
    elif any(k in upper for k in ("GANGGUAN", "PKL", "MIRAS", "BALAP LIAR", "PROSTITUSI", "JUDI")):
        return 3
    elif any(k in upper for k in ("PENGEMIS", "GELANDANGAN", "PARKIR", "PELANGGARAN", "VANDALISME")):
        return 2
    else:
        return 2


def collect_government_data() -> list[dict]:
    file_path = os.path.join(settings.data_dir, settings.government_data_file)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Government data file not found: {file_path}")

    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip().str.lower()

    required = {"periode_data", "wilayah", "kecamatan", "kelurahan", "latitude", "longitude", "jenis_rawan"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in data file: {missing}")

    # Convert coordinates: divide by 1,000,000 to get WGS84 decimal degrees
    df["latitude"] = df["latitude"].astype(float) / COORDINATE_SCALE
    df["longitude"] = df["longitude"].astype(float) / COORDINATE_SCALE

    records = []
    for _, row in df.iterrows():
        lat = float(row["latitude"])
        lon = float(row["longitude"])

        # Skip coordinates outside Jakarta region
        if not (LAT_MIN <= lat <= LAT_MAX) or not (LON_MIN <= lon <= LON_MAX):
            continue

        incident_type = str(row["jenis_rawan"]).strip().upper()
        year = int(row["periode_data"])

        record = {
            "incident_date": date(year, 1, 1),
            "incident_year": year,
            "location_name": f"{str(row['kelurahan']).strip()}, {str(row['kecamatan']).strip()}",
            "district": str(row["wilayah"]).strip().upper(),
            "subdistrict": str(row["kecamatan"]).strip().upper(),
            "incident_type": incident_type,
            "severity_score": get_severity(incident_type),
            "source": "pemerintah",
            "article_url": None,
            "latitude": lat,
            "longitude": lon,
        }
        records.append(record)

    return records
