# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# DHAN_API_URL = "https://api.dhan.co/v2/instruments"  # Update if needed
# DHAN_API_KEY = os.getenv("DHAN_API_KEY")  # Store securely

# def fetch_dhan_instruments():
#     """Fetches the complete instrument list from Dhan API."""
#     headers = {"Authorization": f"Bearer {DHAN_API_KEY}"}
    
#     response = requests.get(DHAN_API_URL, headers=headers)
#     if response.status_code != 200:
#         raise Exception(f"Failed to fetch instruments: {response.text}")

#     return response.json()
