import pandas as pd
import os

# 1. Load the Lexicon
# Points to the file in your specific group project folder
lexicon_path = 'project/Group-Project-1-CH-/data/raw/Data_Set_S1.txt'
lexicon_df = pd.read_csv(lexicon_path, sep='\t', skiprows=3)

# Create a fast lookup dictionary: {word: happiness_average}
hedo_dict = dict(zip(lexicon_df['word'], lexicon_df['happiness_average']))

def calculate_happiness(token_string):
    """
    Calculates the average happiness of a document and identifies OOV words.
    Uses basic .lower() and .split() for tokenization.
    """
    if not isinstance(token_string, str):
        return None, [], 0
    
    # Preprocessing: strictly lowercase and split by whitespace
    tokens = token_string.lower().split()
    
    matched_scores = []
    oov_words = []
    
    for word in tokens:
        if word in hedo_dict:
            matched_scores.append(hedo_dict[word])
        else:
            oov_words.append(word)
    
    # Formula: H_d = sum of scores / count of matched words
    if matched_scores:
        avg_h = sum(matched_scores) / len(matched_scores)
    else:
        avg_h = None
        
    return avg_h, oov_words, len(matched_scores)

# 2. Process your existing Tokenized Data
input_file = 'project/Group-Project-1-CH-/data/raw/tokenized_data_set.csv'
df = pd.read_csv(input_file)

# Apply the scoring function
results = df['tokenized_words'].apply(calculate_happiness)

# Expand the results into new columns
df['happiness_score'], df['oov_words'], df['match_count'] = zip(*results)

# 3. Save the Processed Results
output_dir = 'project/Group-Project-1-CH-/data/processed'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

df.to_csv(f'{output_dir}/scored_nyt_headlines.csv', index=False)

# 4. Generate the OOV Frequency Table for your README
all_oov = [word for sublist in df['oov_words'] for word in sublist]
oov_freq = pd.Series(all_oov).value_counts().reset_index()
oov_freq.columns = ['Word', 'Frequency']

# Save to your tables folder
tables_dir = 'project/Group-Project-1-CH-/tables'
if not os.path.exists(tables_dir):
    os.makedirs(tables_dir)
oov_freq.to_csv(f'{tables_dir}/oov_frequency.csv', index=False)

print("Scoring complete! Results saved in Group-Project-1-CH-/data/processed/")
print(f"Top 5 Unmatched (OOV) words: \n{oov_freq.head(5)}")