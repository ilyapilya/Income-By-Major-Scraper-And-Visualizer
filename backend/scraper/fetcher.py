"""Fetcher for college major income data from multiple sources"""
import requests
from typing import Dict, List
from .sources import ALL_SOURCES, HEADERS
from .parser import parse_job_data_csv, average_duplicate_majors


def fetch_page_html(url: str) -> str | None:
    """Fetch CSV content from a single URL"""
    try:
        resp = requests.get(url, timeout=10, headers=HEADERS)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        print(f"Unable to fetch data from {url}: {e}")
        return None


def fetch_from_multiple_sources() -> List[Dict] | None:
    """
    Attempts to fetch data from multiple sources and combines them.
    Automatically handles duplicate majors by averaging their incomes.
    """
    all_jobs = []
    
    for url in ALL_SOURCES:
        try:
            resp = requests.get(url, timeout=10, headers=HEADERS)
            resp.raise_for_status()
            print(f"✓ Successfully fetched from {url.split('/')[-1]}")
            
            # Try to parse as CSV
            jobs = parse_job_data_csv(resp.text)
            all_jobs.extend(jobs)
            
        except requests.RequestException as e:
            print(f"⚠ Failed to fetch from {url}: {e}")
            continue
    
    if not all_jobs:
        print("✗ Failed to fetch from all sources")
        return None
    
    print(f"✓ Combined data from {len(ALL_SOURCES)} sources: {len(all_jobs)} total records")
    
    # Average duplicates
    unique_jobs = average_duplicate_majors(all_jobs)
    return unique_jobs
