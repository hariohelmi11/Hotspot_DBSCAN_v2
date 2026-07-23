import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    def test_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestDashboardEndpoint:
    @patch("app.api.v1.dashboard.get_dashboard_data")
    def test_get_dashboard(self, mock_fn):
        mock_fn.return_value = {
            "stats": {
                "total_incidents": 100,
                "total_hotspots": 10,
                "high_risk_areas": 3,
                "critical_areas": 1,
            },
            "trend": [],
            "type_distribution": [],
            "risk_distribution": [],
            "top_wilayah": [],
        }
        response = client.get("/api/v1/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert data["stats"]["total_incidents"] == 100


class TestHotspotsEndpoint:
    @patch("app.api.v1.hotspots.HotspotRepository")
    def test_list_hotspots_empty(self, mock_repo_cls):
        mock_repo = MagicMock()
        mock_repo.get_all.return_value = []
        mock_repo_cls.return_value = mock_repo
        response = client.get("/api/v1/hotspots")
        assert response.status_code == 200
        assert response.json() == []


class TestGeoJSONEndpoint:
    @patch("app.api.v1.geojson.HotspotRepository")
    def test_hotspots_geojson(self, mock_repo_cls):
        mock_repo = MagicMock()
        mock_repo.get_all.return_value = []
        mock_repo_cls.return_value = mock_repo
        response = client.get("/api/v1/geojson/hotspots")
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "FeatureCollection"
        assert data["features"] == []
