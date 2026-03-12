import requests
import pandas as pd
import time
import os

# --- 1. Setup ---
# Use the 'Key' from your screenshot, NOT the 'Secret'
API_KEY = '7bSR2Vj1Dtzd1lBxjANFtRfGou7cmA38WP0eaFaV6Gil6kyR' # replace with your actual API key from the NYT Developer Portal
ARCHIVE_URL = "https://api.nytimes.com/svc/archive/v1"
OUTPUT_FILE = "data/raw/Data_Set_Inference.csv"

def fetch_month(year, month):
    """Fetches all article metadata for a specific year and month."""
    url = f"{ARCHIVE_URL}/{year}/{month}.json?api-key={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        print(f"Rate limit hit for {year}-{month}. Waiting...")
        time.sleep(12) # Back off if rate limited
        return fetch_month(year, month)
    else:
        print(f"Failed to fetch {year}-{month}: {response.status_code}")
        return None

def main():
    # Ensure the data/raw directory exists per assignment requirements 
    os.makedirs("data/raw", exist_ok=True)
    
    all_headlines = []
    
    # Loop through the years 2015 to 2025
    for year in range(2015, 2026):
        for month in range(1, 13):
            # Skip future months (we are currently in March 2026)
            if year == 2026 and month > 3:
                break
                
            print(f"Downloading {year}-{month:02d}...")
            data = fetch_month(year, month)
            
            if data and 'response' in data:
                articles = data['response']['docs']
                for doc in articles:
                    # Extracting headline and date
                    headline = doc.get('headline', {}).get('main')
                    date = doc.get('pub_date')
                    
                    if headline:
                        all_headlines.append({
                            "year": year,
                            "month": month,
                            "pub_date": date,
                            "headline": headline
                        })
            
            # Important: NYT rate limits are strict. Sleep between months.
            time.sleep(6) 

    # Save to CSV for the processed phase of your project
    df = pd.DataFrame(all_headlines)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Done! Saved {len(df)} rows to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()