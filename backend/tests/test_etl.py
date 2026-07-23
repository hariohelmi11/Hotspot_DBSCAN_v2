import pytest
from app.services.etl.cleaner import clean_record, deduplicate, batch_clean
from app.services.etl.government_collector import get_severity
from datetime import date


class TestCleaner:
    def test_clean_valid_record(self):
        record = {
            "incident_type": "tawuran",
            "incident_year": 2024,
            "district": "jakarta pusat",
            "latitude": -6.17,
            "longitude": 106.82,
        }
        result = clean_record(record)
        assert result is not None
        assert result["incident_type"] == "TAWURAN"
        assert result["district"] == "JAKARTA PUSAT"
        assert isinstance(result["incident_date"], date)

    def test_clean_invalid_record_no_type(self):
        record = {"incident_year": 2024}
        assert clean_record(record) is None

    def test_severity_clamped(self):
        record = {"incident_type": "TEST", "severity_score": 99}
        result = clean_record(record)
        assert result["severity_score"] == 5

    def test_deduplicate(self):
        records = [
            {"district": "JKT", "subdistrict": "A", "incident_type": "TAWURAN",
             "incident_year": 2024, "latitude": -6.17, "longitude": 106.82},
            {"district": "JKT", "subdistrict": "A", "incident_type": "TAWURAN",
             "incident_year": 2024, "latitude": -6.17, "longitude": 106.82},
        ]
        result = deduplicate(records)
        assert len(result) == 1


class TestSeverity:
    def test_tawuran_severity(self):
        assert get_severity("TAWURAN (WARGA / PELAJAR)") == 5

    def test_pkl_severity(self):
        assert get_severity("PKL") == 3

    def test_pengemis_severity(self):
        assert get_severity("PENGEMIS") == 2

    def test_unknown_severity(self):
        assert get_severity("SESUATU YANG TIDAK DIKENALI") == 2
