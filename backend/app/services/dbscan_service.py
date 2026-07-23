import logging
from collections import Counter
import numpy as np
from sqlalchemy.orm import Session
from sklearn.cluster import DBSCAN
from geoalchemy2.elements import WKTElement
from app.repositories.incident_repository import IncidentRepository
from app.repositories.hotspot_repository import HotspotRepository
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

RISK_THRESHOLDS = {"CRITICAL": 100, "HIGH": 50, "MEDIUM": 25}


def run_dbscan(db: Session, year: int = None) -> dict:
    """Run DBSCAN clustering and persist hotspot results."""
    incident_repo = IncidentRepository(db)
    hotspot_repo = HotspotRepository(db)

    incidents = incident_repo.get_all_with_coords(year=year)
    if not incidents:
        return {"clusters_created": 0, "noise_points": 0, "message": "No incidents found"}

    coords = np.array([[i.latitude, i.longitude] for i in incidents])

    # Convert degree-based eps to radians for haversine metric
    # 0.003 degrees ≈ 333 meters
    eps_rad = np.radians(settings.dbscan_eps)
    coords_rad = np.radians(coords)

    db_model = DBSCAN(
        eps=eps_rad,
        min_samples=settings.dbscan_min_samples,
        algorithm="ball_tree",
        metric="haversine",
    )
    labels = db_model.fit_predict(coords_rad)

    noise_count = int(np.sum(labels == -1))
    unique_labels = sorted(set(labels) - {-1})
    logger.info(f"DBSCAN: {len(unique_labels)} clusters, {noise_count} noise points")

    # Clear existing data for the analysis year(s)
    analysis_year = year or _dominant_year(incidents)
    hotspot_repo.delete_by_year(analysis_year)
    incident_repo.reset_clusters(year=year)

    # Build hotspot records
    cluster_counter = 0
    incident_cluster_map: dict[int, int] = {}  # incident.id → hotspot.id

    for label in unique_labels:
        mask = labels == label
        cluster_incidents = [incidents[i] for i in range(len(incidents)) if mask[i]]

        if not cluster_incidents:
            continue

        cluster_counter += 1
        cluster_coords = np.array([[i.latitude, i.longitude] for i in cluster_incidents])

        centroid_lat = float(np.mean(cluster_coords[:, 0]))
        centroid_lon = float(np.mean(cluster_coords[:, 1]))
        radius = _calc_radius_meters(centroid_lat, centroid_lon, cluster_coords)

        risk_score = sum(i.severity_score or 2 for i in cluster_incidents)
        risk_level = _get_risk_level(risk_score)

        types = [i.incident_type for i in cluster_incidents if i.incident_type]
        dominant_type = Counter(types).most_common(1)[0][0] if types else "UNKNOWN"

        years = [i.incident_year for i in cluster_incidents if i.incident_year]
        cluster_year = Counter(years).most_common(1)[0][0] if years else analysis_year

        hotspot = hotspot_repo.create({
            "cluster_label": int(label),
            "cluster_display_id": f"H-{cluster_counter}",
            "total_incidents": len(cluster_incidents),
            "dominant_type": dominant_type,
            "risk_score": float(risk_score),
            "hotspot_level": risk_level,
            "radius_meters": radius,
            "analysis_year": cluster_year,
            "centroid": WKTElement(f"POINT({centroid_lon} {centroid_lat})", srid=4326),
            "centroid_lat": centroid_lat,
            "centroid_lon": centroid_lon,
        })

        for inc in cluster_incidents:
            incident_cluster_map[inc.id] = hotspot.id

    # Bulk update incident→hotspot links
    if incident_cluster_map:
        mappings = [
            {"id": inc_id, "hotspot_cluster_id": hid}
            for inc_id, hid in incident_cluster_map.items()
        ]
        incident_repo.bulk_update_cluster(mappings)

    db.commit()

    return {
        "clusters_created": cluster_counter,
        "noise_points": noise_count,
        "total_incidents_processed": len(incidents),
    }


def _get_risk_level(risk_score: float) -> str:
    if risk_score >= RISK_THRESHOLDS["CRITICAL"]:
        return "CRITICAL"
    elif risk_score >= RISK_THRESHOLDS["HIGH"]:
        return "HIGH"
    elif risk_score >= RISK_THRESHOLDS["MEDIUM"]:
        return "MEDIUM"
    return "LOW"


def _calc_radius_meters(centroid_lat: float, centroid_lon: float, coords: np.ndarray) -> float:
    """Haversine max distance from centroid to cluster boundary in meters."""
    R = 6_371_000.0
    lat1 = np.radians(centroid_lat)
    lon1 = np.radians(centroid_lon)
    lat2 = np.radians(coords[:, 0])
    lon2 = np.radians(coords[:, 1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    distances = R * 2 * np.arcsin(np.sqrt(a))
    return float(np.max(distances)) if len(distances) > 0 else 0.0


def _dominant_year(incidents) -> int:
    years = [i.incident_year for i in incidents if i.incident_year]
    return Counter(years).most_common(1)[0][0] if years else 2024
