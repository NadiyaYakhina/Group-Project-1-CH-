import pandas as pd

# Load your data
df = pd.read_csv('data/processed/scored_nyt_headlines.csv')

# Remove rows where happiness_score might be missing (like line 4 in your screenshot)
df = df.dropna(subset=['happiness_score'])

print("--- TOP 5 HAPPIEST HEADLINES ---")
print(df.nlargest(5, 'happiness_score')[['tokenized_words', 'happiness_score']])

print("\n--- TOP 5 SADDEST HEADLINES ---")
print(df.nsmallest(5, 'happiness_score')[['tokenized_words', 'happiness_score']])

import pandas as pd
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv('data/processed/scored_nyt_headlines.csv')
df = df.dropna(subset=['happiness_score'])

# Get top 5 and bottom 5
top_5 = df.nlargest(5, 'happiness_score')[['tokenized_words', 'happiness_score']].copy()
top_5['Category'] = 'Happiest'
bottom_5 = df.nsmallest(5, 'happiness_score')[['tokenized_words', 'happiness_score']].copy()
bottom_5['Category'] = 'Saddest'

# Combine and format
plot_df = pd.concat([top_5, bottom_5])

# Create the figure
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('tight')
ax.axis('off')

# Render table
table = ax.table(cellText=plot_df.values, colLabels=plot_df.columns, cellLoc='left', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 2.5) # Stretch for readability

# Add color (Green for high, Red for low)
for i in range(len(plot_df)):
    color = "#d4edda" if i < 5 else "#f8d7da"
    for j in range(len(plot_df.columns)):
        table[(i + 1, j)].set_facecolor(color)

plt.title("Sanity Check: Top 5 Happiest vs. Saddest Headlines", fontsize=14)
plt.savefig('sanity_check_table.png', bbox_inches='tight', dpi=300)