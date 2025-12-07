"""Scraper package for fetching and parsing college major data"""
from .fetcher import fetch_from_multiple_sources, fetch_page_html
from .parser import parse_job_data_csv, average_duplicate_majors, save_to_json, parse_income_value
from .sources import BASE_URL, ALTERNATE_SOURCES, ALL_SOURCES

__all__ = [
    'fetch_from_multiple_sources',
    'fetch_page_html',
    'parse_job_data_csv',
    'average_duplicate_majors',
    'save_to_json',
    'parse_income_value',
    'BASE_URL',
    'ALTERNATE_SOURCES',
    'ALL_SOURCES'
]
