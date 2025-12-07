"""Parser for college major income data"""
import re
import json
from typing import Dict, List


def parse_income_value(raw_str: str) -> int | None:
    """Parses income string to integer"""
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


def parse_job_data_csv(csv_content: str) -> list[Dict]:
    """Parse CSV content and extract Major/Income data"""
    majors: List[Dict] = []
    
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


def average_duplicate_majors(jobs: List[Dict]) -> List[Dict]:
    """
    Takes a list of jobs and averages income for duplicate majors.
    Returns a new list with unique majors and averaged income.
    """
    major_incomes: Dict[str, List[int]] = {}
    
    # Group incomes by major name
    for job in jobs:
        major = job['major'].strip().upper()  # Normalize
        income = job['income']
        
        if major not in major_incomes:
            major_incomes[major] = []
        major_incomes[major].append(income)
    
    # Calculate average income for each major
    averaged_jobs = []
    for major, incomes in major_incomes.items():
        avg_income = sum(incomes) / len(incomes)
        averaged_jobs.append({
            'major': major,
            'income': int(round(avg_income)),
            'count': len(incomes)  # Track how many sources were averaged
        })
    
    print(f"✓ Averaged {len(jobs)} jobs to {len(averaged_jobs)} unique majors")
    return averaged_jobs


def save_to_json(jobs: List[Dict], filename: str = "jobs.json") -> None:
    """Save jobs list to JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(jobs, f, indent=2)
        print(f"Successfully saved {len(jobs)} jobs to {filename}")
    except IOError as e:
        print(f"Error saving to file: {e}")
