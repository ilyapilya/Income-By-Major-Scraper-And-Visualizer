"""Backend configuration"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""
    
    # Database settings
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("MY_SQL_PASSWORD", "root")
    DB_NAME = os.getenv("DB_NAME", "income_major_db")
    
    # Flask settings
    DEBUG = os.getenv("DEBUG", "True") == "True"
    TESTING = os.getenv("TESTING", "False") == "True"
    
    # API settings
    API_HOST = os.getenv("API_HOST", "127.0.0.1")
    API_PORT = int(os.getenv("API_PORT", 5000))


# Export configuration
config = Config()
