"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-07-14
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import geoalchemy2

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("password_hash", sa.Text, nullable=False),
        sa.Column("role", sa.String(50), server_default="viewer"),
    )
    op.create_index("uq_users_username", "users", ["username"], unique=True)

    op.create_table(
        "hotspot_clusters",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("cluster_label", sa.Integer),
        sa.Column("cluster_display_id", sa.String(20)),
        sa.Column("total_incidents", sa.Integer),
        sa.Column("dominant_type", sa.String(100)),
        sa.Column("risk_score", sa.Numeric(10, 2)),
        sa.Column("hotspot_level", sa.String(50)),
        sa.Column("radius_meters", sa.Float),
        sa.Column("analysis_year", sa.Integer),
        sa.Column("centroid", geoalchemy2.Geometry("POINT", srid=4326), nullable=True),
        sa.Column("centroid_lat", sa.Float),
        sa.Column("centroid_lon", sa.Float),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.text("NOW()")),
    )
    op.create_index("idx_hotspot_year", "hotspot_clusters", ["analysis_year"])
    op.create_index(
        "idx_hotspot_centroid", "hotspot_clusters", ["centroid"],
        postgresql_using="gist",
    )

    op.create_table(
        "public_order_incidents",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("incident_date", sa.Date),
        sa.Column("incident_year", sa.Integer),
        sa.Column("location_name", sa.Text),
        sa.Column("district", sa.String(100)),
        sa.Column("subdistrict", sa.String(100)),
        sa.Column("incident_type", sa.String(100)),
        sa.Column("severity_score", sa.Integer),
        sa.Column("source", sa.String(50)),
        sa.Column("article_url", sa.Text),
        sa.Column("latitude", sa.Float),
        sa.Column("longitude", sa.Float),
        sa.Column("geom", geoalchemy2.Geometry("POINT", srid=4326), nullable=True),
        sa.Column("hotspot_cluster_id", sa.BigInteger, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.text("NOW()")),
    )
    op.create_index("idx_incident_year", "public_order_incidents", ["incident_year"])
    op.create_index("idx_incident_cluster", "public_order_incidents", ["hotspot_cluster_id"])
    op.create_index(
        "idx_incident_geom", "public_order_incidents", ["geom"],
        postgresql_using="gist",
    )

    op.create_table(
        "scrape_logs",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("execution_time", sa.TIMESTAMP, server_default=sa.text("NOW()")),
        sa.Column("source", sa.String(100)),
        sa.Column("total_records", sa.Integer, server_default="0"),
        sa.Column("success", sa.Boolean, server_default="false"),
        sa.Column("error_message", sa.Text),
    )


def downgrade() -> None:
    op.drop_table("scrape_logs")
    op.drop_table("public_order_incidents")
    op.drop_table("hotspot_clusters")
    op.drop_table("users")
