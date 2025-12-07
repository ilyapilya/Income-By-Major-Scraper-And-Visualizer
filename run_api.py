#!/usr/bin/env python
"""Wrapper script to run the Flask API"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.api import create_app
from backend.config import config

if __name__ == '__main__':
    app = create_app()
    app.run(debug=config.DEBUG, host=config.API_HOST, port=config.API_PORT, use_reloader=False)
