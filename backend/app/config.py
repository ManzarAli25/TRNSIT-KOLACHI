"""Configuration settings for the TRNSIT Kolachi backend."""
import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    API_TITLE: str = "TRNSIT Kolachi API"
    API_VERSION: str = "0.1.0"
    API_DESCRIPTION: str = "Transit routing API for Karachi public transport"

    # CORS
    CORS_ORIGINS: list[str] = ["*"]

    # Valhalla Settings
    VALHALLA_URL: str = "http://localhost:8002"
    VALHALLA_TIMEOUT: int = 30

    # Data Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    GTFS_DIR: Path = BASE_DIR / "data" / "gtfs"
    VALHALLA_DIR: Path = BASE_DIR / "valhalla"

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
