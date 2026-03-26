import pandas as pd
import ast
import os

# 1. Setup paths relative to your 'coding-humanities' folder
input_path = 'data/processed/scored_nyt_headlines.csv'

# Quick check to ensure the file exists before running
if not os.path.exists(input_path):
    print(f"Error: Could not find {input_path}")
    print(f"Current directory is: {os.getcwd()}")
else:
    # 2. Load the processed data
    df = pd.read_csv(input_path)

    # 3. Convert 'oov_words' column from string representation back to actual Python lists
    # This handles the "['word']" issue in CSVs
    df['oov_words'] = df['oov_words'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])

    # 4. Flatten all OOV words into one single list
    all_oov_words = [word for sublist in df['oov_words'] for word in sublist]

    # 5. Create the frequency table
    oov_counts = pd.Series(all_oov_words).value_counts().reset_index()
    oov_counts.columns = ['OOV Word', 'Total Frequency']

    # 6. Calculate the Grand Totals
    total_oov_occurrences = oov_counts['Total Frequency'].sum()
    unique_oov_count = len(oov_counts)

    # 7. PRINT TO TERMINAL
    print("\n" + "="*50)
    print("       OUT-OF-VOCABULARY (OOV) ANALYSIS")
    print("="*50)
    
    print(f"\nTOTAL OOV WORD OCCURRENCES: {total_oov_occurrences}")
    print(f"TOTAL UNIQUE OOV WORDS:     {unique_oov_count}")
    
    print("\nTOP 15 MOST FREQUENT OOV WORDS:")
    # Using to_string(index=False) for a clean terminal look
    print(oov_counts.head(15).to_string(index=False))
    
    print("\n" + "="*50)

    # 8. Optional: Save the frequency list for your report
    output_table_path = 'tables/oov_frequency_summary.csv'
    os.makedirs('tables', exist_ok=True)
    oov_counts.to_csv(output_table_path, index=False)
    print(f"Full frequency table saved to: {output_table_path}")

    import pandas as pd
import ast
import os

# 1. Setup path
input_path = 'data/processed/scored_nyt_headlines.csv'

if not os.path.exists(input_path):
    print(f"Error: Could not find {input_path}")
else:
    df = pd.read_csv(input_path)

    # 2. Process OOV Words (convert from string to list and flatten)
    df['oov_words_list'] = df['oov_words'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
    all_oov_tokens = [word for sublist in df['oov_words_list'] for word in sublist]
    
    # 3. Process ALL Words (Tokens)
    # We split the 'tokenized_words' column by whitespace to count every word present
    all_headlines_tokens = [word for sublist in df['tokenized_words'].dropna().str.split() for word in sublist]

    # 4. Calculate Statistics
    total_token_count = len(all_headlines_tokens)
    total_oov_count = len(all_oov_tokens)
    
    # Calculate percentage (OOV Rate)
    if total_token_count > 0:
        oov_percentage = (total_oov_count / total_token_count) * 100
    else:
        oov_percentage = 0

    # 5. Create Frequency Table for display
    oov_counts = pd.Series(all_oov_tokens).value_counts().reset_index()
    oov_counts.columns = ['OOV Word', 'Frequency']

    # 6. PRINT RESULTS TO TERMINAL
    print("\n" + "="*50)
    print("       FINAL DATA COVERAGE REPORT")
    print("="*50)
    
    print(f"TOTAL TOKENS IN DATASET:    {total_token_count:,}")
    print(f"TOTAL OOV WORD TOKENS:      {total_oov_count:,}")
    print(f"OOV PERCENTAGE (Rate):      {oov_percentage:.2f}%")
    print(f"DICTIONARY COVERAGE:        {100 - oov_percentage:.2f}%")
    
    print("\n" + "-"*50)
    print("TOP 10 MOST COMMON OOV WORDS:")
    print(oov_counts.head(10).to_string(index=False))
    print("="*50 + "\n")
