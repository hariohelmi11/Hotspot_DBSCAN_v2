from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = "postgresql://hotspot_user:hotspot_pass@localhost:5432/hotspot_db"
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    data_dir: str = "./data"
    government_data_file: str = "data-rawan.xls"

    # DBSCAN parameters (eps in degrees ≈ 333m)
    dbscan_eps: float = 0.003
    dbscan_min_samples: int = 5

    # Risk score thresholds
    risk_critical: int = 100
    risk_high: int = 50
    risk_medium: int = 25

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
