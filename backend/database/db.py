import pymysql
import os
from typing import List, Dict, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Database:
    def __init__(self, host: str = "localhost", user: str = "root", 
                 password: Optional[str] = None, database: str = "income_major_db"):
        # If password not provided, load from .env
        if password is None:
            password = os.getenv("MY_SQL_PASSWORD", "root")
        """Initialize database connection parameters."""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
    
    def connect(self):
        """Establish connection to MySQL database."""
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return conn
        except pymysql.Error as e:
            print(f"Database connection error: {e}")
            return None
    
    def insert_majors(self, jobs: List[Dict]) -> bool:
        """Insert major/income data into database."""
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            query = """
                INSERT INTO income_by_major (major, income, timestamp)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE income=%s, timestamp=%s
            """
            
            for job in jobs:
                cursor.execute(query, (
                    job['major'],
                    job['income'],
                    datetime.now(),
                    job['income'],
                    datetime.now()
                ))
            
            conn.commit()
            print(f"✓ Successfully inserted {len(jobs)} majors into database")
            return True
        
        except pymysql.Error as e:
            print(f"✗ Insert error: {e}")
            conn.rollback()
            return False
        
        finally:
            cursor.close()
            conn.close()
    
    def get_all_majors(self) -> Optional[List[Dict]]:
        """Retrieve all majors sorted by income (highest first)."""
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT id, major, income, timestamp FROM income_by_major ORDER BY income DESC"
            cursor.execute(query)
            results = cursor.fetchall()
            print(f"✓ Retrieved {len(results)} majors from database")
            return results
        
        except pymysql.Error as e:
            print(f"✗ Query error: {e}")
            return None
        
        finally:
            cursor.close()
            conn.close()
    
    def get_top_n_majors(self, n: int = 10) -> Optional[List[Dict]]:
        """Retrieve top N majors by income."""
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = f"SELECT id, major, income, timestamp FROM income_by_major ORDER BY income DESC LIMIT {n}"
            cursor.execute(query)
            results = cursor.fetchall()
            print(f"✓ Retrieved top {n} majors from database")
            return results
        
        except pymysql.Error as e:
            print(f"✗ Query error: {e}")
            return None
        
        finally:
            cursor.close()
            conn.close()
    
    def get_majors_by_income_range(self, min_income: int, max_income: int) -> Optional[List[Dict]]:
        """Retrieve majors within income range."""
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = """
                SELECT id, major, income, timestamp FROM income_by_major 
                WHERE income BETWEEN %s AND %s 
                ORDER BY income DESC
            """
            cursor.execute(query, (min_income, max_income))
            results = cursor.fetchall()
            print(f"✓ Retrieved {len(results)} majors in range ${min_income}-${max_income}")
            return results
        
        except pymysql.Error as e:
            print(f"✗ Query error: {e}")
            return None
        
        finally:
            cursor.close()
            conn.close()
    
    def get_major_by_name(self, major_name: str) -> Optional[Dict]:
        """Retrieve a specific major by name."""
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT id, major, income, timestamp FROM income_by_major WHERE major = %s"
            cursor.execute(query, (major_name,))
            result = cursor.fetchone()
            
            if result:
                print(f"✓ Found major: {result['major']} (${result['income']})")
            else:
                print(f"✗ Major '{major_name}' not found")
            
            return result
        
        except pymysql.Error as e:
            print(f"✗ Query error: {e}")
            return None
        
        finally:
            cursor.close()
            conn.close()
    
    def get_statistics(self) -> Optional[Dict]:
        """Retrieve income statistics from database."""
        conn = self.connect()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = """
                SELECT 
                    COUNT(*) as total_majors,
                    AVG(income) as avg_income,
                    MIN(income) as min_income,
                    MAX(income) as max_income
                FROM income_by_major
            """
            cursor.execute(query)
            result = cursor.fetchone()
            print(f"✓ Statistics retrieved: {result['total_majors']} majors")
            return result
        
        except pymysql.Error as e:
            print(f"✗ Query error: {e}")
            return None
        
        finally:
            cursor.close()
            conn.close()
    
    def delete_all_majors(self) -> bool:
        """Clear all data from the table (for testing/reset)."""
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            query = "DELETE FROM income_by_major"
            cursor.execute(query)
            conn.commit()
            print(f"✓ Cleared all majors from database")
            return True
        
        except pymysql.Error as e:
            print(f"✗ Delete error: {e}")
            conn.rollback()
            return False
        
        finally:
            cursor.close()
            conn.close()
