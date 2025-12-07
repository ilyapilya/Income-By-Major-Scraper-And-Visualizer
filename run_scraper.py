#!/usr/bin/env python
"""Wrapper script to run the scraper workflow"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    from backend.main import main
    success = main()
    sys.exit(0 if success else 1)
