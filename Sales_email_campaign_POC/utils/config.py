"""
Configuration - 100% Free Local Setup
- Google Gemini (no credit card)
- DynamoDB Local (Docker)
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Google Gemini API (Free)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = "gemini-1.5-flash"

# DynamoDB Local
DYNAMODB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT", "http://localhost:8000")
AWS_REGION = "us-east-1"

# Directories
DATA_DIR = "data"
SESSIONS_DIR = "sessions"

# Email Settings
EMAIL_TARGET_WORD_COUNT = 144
EMAIL_MIN_WORDS = 100
EMAIL_MAX_WORDS = 200

# Create directories
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SESSIONS_DIR, exist_ok=True)
