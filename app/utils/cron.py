from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import math
import io  # Import StringIO

load_dotenv()

# URLs for fetching instruments from Dhan
COMPACT_URL = os.getenv("COMPACT_URL")
DETAILED_URL = os.getenv("DETAILED_URL")

# File paths for storing instrument lists
DATA_DIR = "data"
COMPACT_FILE_PATH = os.path.join(DATA_DIR, "instruments_compact.csv")
DETAILED_FILE_PATH = os.path.join(DATA_DIR, "instruments_detailed.csv")

def sanitize_data(value):
    """Sanitize individual data values."""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):  
            return None  # Convert NaN or Infinity to None
    elif isinstance(value, str):
        if value.strip() == "":  # Check for empty strings
            return None  
    return value  # Return as is if it's valid

def sanitize_and_process_data(csv_file_path):
    """Load, sanitize, and process CSV data."""
    if not os.path.exists(csv_file_path):  
        print(f"[WARNING] File {csv_file_path} does not exist.")
        return []  

    df = pd.read_csv(csv_file_path, dtype=str)  # Read everything as string to avoid auto-casting issues

    # Replace empty strings and invalid floats with None
    df = df.applymap(sanitize_data)

    # Convert back to appropriate types (float, int where needed)
    for column in df.columns:
        if df[column].str.replace('.', '', 1).str.isnumeric().all():  # If numeric
            df[column] = pd.to_numeric(df[column])  # Convert to int/float

    sanitized_data = df.to_dict(orient="records")  # Convert back to list of dictionaries
    return sanitized_data

def fetch_and_store_instruments():
    """Downloads the latest instrument list from Dhan, sanitizes it, and saves it locally."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)  # Ensure 'data' directory exists

        # Download the CSV files
        for url, path in [(COMPACT_URL, COMPACT_FILE_PATH), (DETAILED_URL, DETAILED_FILE_PATH)]:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"[CRON] {path} updated at {datetime.now()}")
            else:
                print(f"[CRON] Failed to fetch {url}: {response.status_code}")

    except Exception as e:
        print(f"[CRON] Error in fetching instruments: {e}")

# APScheduler Setup
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_store_instruments, "interval", hours=24)  # Runs every 24h
scheduler.start()

# Call the function immediately to fetch and store instruments on app start
fetch_and_store_instruments()
