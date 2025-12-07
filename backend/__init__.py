"""Backend package initialization"""
from backend.scraper import (
    fetch_from_multiple_sources,
    parse_job_data_csv,
    average_duplicate_majors,
    save_to_json,
)
from backend.database import Database
from backend.config import config

__all__ = [
    "fetch_from_multiple_sources",
    "parse_job_data_csv",
    "average_duplicate_majors",
    "save_to_json",
    "Database",
    "config",
]
