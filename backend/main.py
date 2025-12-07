"""Main entry point for backend scraper workflow"""
import sys
import json
from pathlib import Path

# Add parent directory to path for relative imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.scraper import fetch_from_multiple_sources
from backend.database import Database
from backend.config import config


def main():
    """Main workflow: fetch -> deduplicate -> save -> insert to DB"""
    
    print("=" * 60)
    print("Income By Major Scraper - Starting Workflow")
    print("=" * 60)
    
    # Step 1: Fetch and parse data from multiple sources
    print("\n[1/3] Fetching and parsing data from multiple sources...")
    try:
        unique_jobs = fetch_from_multiple_sources()
        if not unique_jobs:
            print("✗ No data returned from sources")
            return False
        print(f"✓ Fetched and deduplicated to {len(unique_jobs)} unique majors")
    except Exception as e:
        print(f"✗ Failed to fetch data: {e}")
        return False
    
    # Step 2: Save to JSON
    print("\n[2/3] Saving results to JSON...")
    try:
        output_file = Path(__file__).parent.parent / "jobs.json"
        with open(output_file, 'w') as f:
            json.dump(unique_jobs, f, indent=2)
        print(f"✓ Saved to {output_file}")
    except Exception as e:
        print(f"✗ Failed to save JSON: {e}")
        return False
    
    # Step 3: Insert into database
    print("\n[3/3] Inserting data into database...")
    try:
        db = Database(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        db.insert_majors(unique_jobs)
        print(f"✓ Inserted {len(unique_jobs)} majors into database")
        
        # Display statistics
        stats = db.get_statistics()
        if stats:
            print("\n" + "=" * 60)
            print("Database Statistics:")
            print("=" * 60)
            print(f"Total majors: {stats['total_majors']}")
            print(f"Average income: ${stats['avg_income']:,.2f}")
            print(f"Minimum income: ${stats['min_income']:,}")
            print(f"Maximum income: ${stats['max_income']:,}")
            print("=" * 60)
        
        return True
    except Exception as e:
        print(f"✗ Failed to insert into database: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
