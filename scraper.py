import json, re, requests
from typing import Dict, List
from bs4 import BeautifulSoup as bs
from database.database import Database
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv() 

# Constants
BASE_URL = "https://raw.githubusercontent.com/fivethirtyeight/data/master/college-majors/recent-grads.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CollegeIncomeScraper/1.0)"
}

# Fetches HTML content from URL. Also fetches CSV content.
def fetch_page_html(page: int) -> str | None:
    try:
        resp = requests.get(BASE_URL, timeout=10)
        resp.raise_for_status()  # raises on 4xx/5xx
        return resp.text
    except requests.RequestException as e:
        print(f"Unable to fetch data: {e}")
        return None

# Parses income string to integer from job string
def parse_income_value(raw_str: str) -> int | None:
    if raw_str is None:
        return None
    
    # Removing whitespace, unwanted characters, and normalizing
    cleaned_str = raw_str.strip().lower().replace("$", "").replace(",", "")

    # Handle ranges like "75,000 to 99,999" - extract the first number
    if "to" in cleaned_str:
        parts = cleaned_str.split("to")
        cleaned_str = parts[0].strip()

    # Handle for "X k" or "Xk"
    match_k = re.match(r"^(\d+(?:\.\d+)?)\s*k$", cleaned_str)
    if match_k:
        return int(float(match_k.group(1)) * 1000)

    # Fallback: just digits
    digits = re.findall(r"\d+", cleaned_str)
    if digits:
        return int(digits[0])  # Take first number only

    return None

# Uses CSV content to extract Major / Income Data
def parse_job_data_csv(csv_content : str) -> list[Dict]:
    majors : List[Dict] = []
    
    lines = csv_content.strip().split('\n')
    if not lines:
        return majors
    
    # Column indices based on FiveThirtyEight dataset:
    # [2]: Major name
    # [15]: Median salary
    MAJOR_COL = 2
    MEDIAN_COL = 15
    
    # Parse data rows (skip header at line 0)
    for line in lines[1:]:
        if not line.strip():
            continue
        
        cols = line.split(',')
        if len(cols) > MEDIAN_COL:
            major = cols[MAJOR_COL].strip()
            median_salary_str = cols[MEDIAN_COL].strip()
            
            income_value = parse_income_value(median_salary_str)
            
            if major and income_value is not None:
                majors.append({
                    'major': major,
                    'income': income_value
                })
    
    return majors

# Saves joblist to JSON file: jobs.json or other if specified
def save_to_json(jobs : List[Dict], filename: str = "jobs.json") -> None:
    try:
        with open(filename, 'w') as f:
            # json.dump() saves jobs list to JSON file
            json.dump(jobs, f, indent=2)
        print(f"Successfully saved {len(jobs)} jobs to {filename}")
    except IOError as e:
        print(f"Error saving to file: {e}")


if __name__ == "__main__":
    print("Starting Major to Income Scraper...")
    
    # Step 1: Fetch CSV content
    csv_content = fetch_page_html(1)

    # Initialize jobs
    jobs = None

    # Initialize DB Pool (password loaded from .env)
    db = Database(host="localhost", user="root", database="income_major_db")

    # Step 2: Parse job data from CSV
    if csv_content is not None:
        print(f"Successfully fetched {len(csv_content)} characters of CSV")
        jobs = parse_job_data_csv(csv_content)
        print(f"Found {len(jobs)} majors")
        
        # Display first 10 results
        for i in range(min(len(jobs), 10)):
            print(jobs[i])
    else:
        print("Failed to fetch CSV data")

    # Step 3: Save to JSON
    if jobs:
        print(f"Saving {len(jobs)} majors to JSON file: jobs.json")
        save_to_json(jobs, "jobs.json")

    # Step 4: Save to MySQL DB and Display Statistics
    if jobs:
        print(f"Storing {len(jobs)} into MySQL DB")
        db.insert_majors(jobs)
        
        # Fetching statistics
        print("Fetching updated statistics...")
        stats = db.get_statistics()
        if stats:
            print(f"Total Majors: {stats['total_majors']}")
            print(f"Average Income: ${stats['avg_income']:,.2f}")
            print(f"Highest Income: ${stats['max_income']:,}")
            print(f"Lowest Income: ${stats['min_income']:,}")
        else:
            print("Failed to fetch statistics from DB")
    
    # TODO: Step 5: Use matplotlib to plot Major vs Income

    
