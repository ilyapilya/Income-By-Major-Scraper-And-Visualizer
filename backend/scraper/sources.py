"""Data sources for college major income data"""

BASE_URL = "https://raw.githubusercontent.com/fivethirtyeight/data/master/college-majors/recent-grads.csv"

ALTERNATE_SOURCES = [
    "https://raw.githubusercontent.com/datasets/college-majors/master/majors-list.csv",
    "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018/2018-10-16/recent-grads.csv"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CollegeIncomeScraper/1.0)"
}

ALL_SOURCES = [BASE_URL] + ALTERNATE_SOURCES
