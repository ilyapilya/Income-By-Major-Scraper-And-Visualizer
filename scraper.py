import time, json, re, requests
from typing import Dict, List, Set, Tuple
from bs4 import BeautifulSoup as bs

BASE_URL = "https://www.bls.gov/ooh/home.htm"  # <- change this
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CollegeIncomeScraper/1.0)"
}

# Fetches HTML content given page URL. Returns None on failure.
def fetch_page_html(page: int) -> str | None:
    url = BASE_URL.format(page=page)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()  # raises on 4xx/5xx
        return resp.text
    except requests.RequestException as e:
        print(f"Unable to fetch page {page}: {e}")
        return None

def parse_income_value(raw_str: str) -> int | None:
    if raw_str is None:
        return None
    
    # Removing whitespace, unwanted characters, and normalizing
    cleaned_str = raw_str.strip().lower().replace("$", "").replace(",", "")

    # Handle for "X k" or "Xk"
    match_k = re.match(r"^(\d+(?:\.\d+)?)\s*k$", cleaned_str)
    if match_k:
        return int(float(match_k.group(1)) * 1000)

    # Fallback: just digits
    digits = re.findall(r"\d+", cleaned_str)
    if digits:
        return int("".join(digits))

    return None

# Uses HTML content to extract Major / Income Data
def parse_job_data(html : str) -> dict | None:
    soup = bs(html, "html.parser")
    jobs : List[Dict] = []

    # Job Containers
    job_elements = soup.find_all("div", class_="job-card")  # <- Change
    
    for elem in job_elements:
        major = elem.find('h2', class_='job-title')  # Example selector
        income = elem.find('span', class_='salary')  # Example selector
        
        if major and income:
            major_text = major.get_text(strip=True)
            income_value = parse_income_value(income.get_text(strip=True))
            
            jobs.append({
                'major': major_text,
                'income': income_value
            })
    
    return jobs

if __name__ == "__main__":
    html_content = fetch_page_html(1)
    if html_content is not None:
        jobs = parse_job_data(html_content)
        for job in jobs:
            print(job)
    else:
        print("Failed to fetch page")
