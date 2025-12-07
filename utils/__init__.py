"""Utils package for Income-By-Major scraper and visualizer"""
from .api import app
from .scraper import (
    fetch_from_multiple_sources,
    parse_job_data_csv,
    average_duplicate_majors,
    save_to_json
)
from .statplot import Plotter

__all__ = [
    'app',
    'fetch_from_multiple_sources',
    'parse_job_data_csv',
    'average_duplicate_majors',
    'save_to_json',
    'Plotter'
]
