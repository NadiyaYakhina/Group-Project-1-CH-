import requests
import pandas as pd
import time
import os

# --- 1. Setup ---
API_KEY = '' # replace with your actual API key from the NYT Developer Portal
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

# --- 2. Tokenization and Cleaning --- //We reccomend to run this separetly from above
'''
// For data cleaning and tokenization, we followed the methodology outlined in the original paper by Dodds:
1. Data Extraction: Parsed Year, Month, Day to analyze happiness trends across 
   different timescales (e.g., yearly or monthly cycles).
2. Punctuation: Stripped all symbols (including smart quotes) to normalize 
   possessives (e.g., "sheinbaum's" -> "sheinbaums").
3. Case: Lowercased all words to match the case-insensitive labMT word list[cite: 1631].
4. Numbers: Removed digits to focus on semantic words with emotional weight.
5. No stemming: Kept full word forms (like 'heres' vs 'here') because different 
   inflections have different happiness scores.
6. Stop words: Filtered neutral words to increase the sensitivity of the 
   hedonometric instrument.

// Why we didnt just use 'tokenize' function?
We avoided standard library tokenizers (like NLTK's word_tokenize) because they 
are 'too smart' for this study's needs. They often split 
contractions (don't -> do + n't) or keep punctuation as separate tokens, which 
would make it harder to match words directly to the labMT 1.0 dataset.'''


import pandas as pd
import re
import string
import nltk
from nltk.corpus import stopwords
import os


# Ensure stop words are ready
nltk.download('stopwords', quiet=True)

def replicate_tokenization():

    '''Finding the paths were a bit tricky, so we added this to 
    make sure it works regardless of where the script is run from'''

    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, '..', 'data', 'raw', 'Data_Set_Inference.csv')
    output_path = os.path.join(base_dir, '..', 'data', 'raw', 'tokenized_data_set.csv')

    if not os.path.exists(input_path):
        print(f"ERROR: File not found at: {input_path}")
        return


    df = pd.read_csv(input_path)
    
    # Handle date extraction (hours, days, months), 'errors=coerce' prevents the script from crashing if a date is messy
    df['pub_date'] = pd.to_datetime(df['pub_date'], errors='coerce', utc=True)
    df = df.dropna(subset=['pub_date']) # Remove rows with broken dates
    
    df['year'] = df['pub_date'].dt.year
    df['month'] = df['pub_date'].dt.month
    df['day'] = df['pub_date'].dt.day
    
    #We decided to define cleaning logic (we here kind of try to replicate labMT 1.0 Methodology)
    stop_words = set(stopwords.words('english'))

    def clean_hedonometric_text(text):
        if not isinstance(text, str):
            return ""
        
        #Remove numbers to avoid noise
        text = re.sub(r'\d+', '', text)
        
        # Remove ALL punctuation/symbols (also with smart quotes and possessives) // we struggled that one for a long time...
        text = re.sub(r"[^\w\s]", "", text)
        
        # Lowercase and split (Paper by Dodds et al. used case-insensitive pattern matching) 
        words = text.lower().split()
        
        #Filter stop words
        tokens = [w for w in words if w not in stop_words]
        
        return " ".join(tokens)

    #Column check //do not mind this, just catching potential naming issues
    target_col = 'headline' if 'headline' in df.columns else 'heading'
    
    #Process and save finally!!
    df['tokenized_words'] = df[target_col].apply(clean_hedonometric_text)
    
    final_df = df[['year', 'month', 'day', 'tokenized_words']]
    final_df.to_csv(output_path, index=False)
    
    print(f"SUCCESS! Created: {output_path}")
    print(final_df.head())

if __name__ == "__main__":
    replicate_tokenization()