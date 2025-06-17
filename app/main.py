#!/usr/bin/env python3
"""
Main Flask application cho migration toolkit
"""
import logging
from app.factory import create_app

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    ) 