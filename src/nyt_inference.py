#1: import required libraries
from pathlib import Path
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# load dataset

# Path relative to script
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "../data/processed/scored_nyt_headlines.csv")

df = pd.read_csv(file_path)

#3: inspect dataset
print("\nFirst 5 rows of the dataset:")
print(df.head())

print("\nColumn names:")
print(df.columns)

print("\nDataset information:")
print(df.info())

print("\nBasic statistics:")
print(df.describe())

print("\nDataset shape (rows, columns):")
print(df.shape)

print("\nMissing values per column:")
print(df.isnull().sum())

#4: create date column

print("\nCreating date column from year, month, and day:")

df["date"] = pd.to_datetime(df[["year", "month", "day"]])

print(df[["year", "month", "day", "date"]].head())

#5: create overall time-series visualisation, happiness

## 5.1 calculating monthly averages

df = df[df["year"] >= 2015]
df["year_month"] = df["date"].dt.to_period("M")
monthly_avg = df.groupby("year_month")["happiness_score"].mean().reset_index()
monthly_avg["year_month"] = monthly_avg["year_month"].dt.to_timestamp()
monthly_avg = monthly_avg[(monthly_avg["year_month"] >= "2015-01-01") &
                          (monthly_avg["year_month"] <= "2025-12-31")]

### inspection
print("\nMonthly averages (first 5 rows):")
print(monthly_avg.head())
print("Monthly averages (last 5 rows):")
print(monthly_avg.tail())

### save table
tables_path = os.path.join(script_dir, "../tables/nyt_monthly_happiness_avg.csv")
monthly_avg.to_csv(tables_path, index=False)
print(f"\nMonthly averages saved as CSV to: {tables_path}")

## 5.2 time-series plot

plt.figure(figsize=(12,6))
plt.plot(monthly_avg["year_month"], monthly_avg["happiness_score"], marker="o", linestyle="-")
plt.xlim(pd.Timestamp("2015-01-01"), pd.Timestamp("2025-12-31"))
plt.ylim(5.3, 5.65)
plt.xlabel("Time (2015–2025)")
plt.ylabel("Average Happiness Score")
plt.title("Average Monthly Happiness Score (2015–2025)")
plt.tight_layout()

### save figure
figures_path = os.path.join(script_dir, "../figures/nyt_monthly_happiness_trend.png")
plt.savefig(figures_path)
print(f"Figure saved to: {figures_path}")

print("\nSummary statistics of monthly average happiness scores:")
print(monthly_avg["happiness_score"].describe())

## 5.3 calculating yearly averages

df = df[df["year"] >= 2015]
yearly_avg = df.groupby("year")["happiness_score"].mean().reset_index()
yearly_avg = yearly_avg[(yearly_avg["year"] >= 2015) &
                        (yearly_avg["year"] <= 2025)]

### inspection
print("\nYearly averages:")
print(yearly_avg)

### save table
tables_path = os.path.join(script_dir, "../tables/nyt_yearly_happiness_avg.csv")
yearly_avg.to_csv(tables_path, index=False)
print(f"\nYearly averages saved as CSV to: {tables_path}")

## 5.4 time-series plot (aggregated by year)

plt.figure(figsize=(10,5))

plt.plot(yearly_avg["year"], yearly_avg["happiness_score"],
         marker="o", linestyle="-")

plt.xlim(2015, 2025)
plt.xticks(range(2015, 2026))
plt.xlabel("Year")
plt.ylabel("Average Happiness Score")
plt.title("Average Yearly Happiness Score (2015–2025)")

plt.tight_layout()

### save figure
figures_path = os.path.join(script_dir, "../figures/nyt_yearly_happiness_trend.png")
plt.savefig(figures_path)
print(f"Figure saved to: {figures_path}")

# summary stats
print("\nSummary statistics of yearly average happiness scores:")
print(yearly_avg["happiness_score"].describe())

#6: overall time-series visualisation, match_count

## 6.1: total match count by month
df_filtered = df[(df["year"] >= 2015) & (df["year"] <= 2025)]
df_filtered["year_month"] = df_filtered["date"].dt.to_period("M")
monthly_match = df_filtered.groupby("year_month")["match_count"].sum().reset_index()
monthly_match["year_month"] = monthly_match["year_month"].dt.to_timestamp()

print("\nMonthly total match_count (first 5 rows):")
print(monthly_match.head())

## 6.2: plot: words matched over time 
plt.figure(figsize=(12,6))
plt.plot(monthly_match["year_month"], monthly_match["match_count"], marker="o", linestyle="-", color="green")
plt.xlim(pd.Timestamp("2015-01-01"), pd.Timestamp("2025-12-31"))
plt.xlabel("Time (2015–2025)")
plt.ylabel("Total Matched Words")
plt.title("Total Match Count of Words Overtime (2015–2025)")

figures_path = os.path.join(script_dir, "../figures/nyt_monthly_match_count_trend.png")
plt.savefig(figures_path)
print(f"Figure saved to: {figures_path}")

#7: number of titles over time

## 7.1: total number of headlines per month

df_filtered = df[(df["year"] >= 2015) & (df["year"] <= 2025)]
df_filtered["year_month"] = df_filtered["date"].dt.to_period("M")
monthly_count = df_filtered.groupby("year_month").size().reset_index(name="headline_count")
monthly_count["year_month"] = monthly_count["year_month"].dt.to_timestamp()

print("\nMonthly headline counts (first 5 rows):")
print(monthly_count.head())

tables_path = os.path.join(script_dir, "../tables/nyt_monthly_headline_count.csv")
monthly_count.to_csv(tables_path, index=False)
print(f"Monthly headline counts saved as CSV to: {tables_path}")

max_row = monthly_count.loc[monthly_count["headline_count"].idxmax()]
print(f"Maximum headlines: {max_row['headline_count']} in {max_row['year_month'].strftime('%Y-%m')}")
min_row = monthly_count.loc[monthly_count["headline_count"].idxmin()]
print(f"Minimum headlines: {min_row['headline_count']} in {min_row['year_month'].strftime('%Y-%m')}")

## 7.2: plot: total number of headlines over time

plt.figure(figsize=(12,6))
plt.plot(monthly_count["year_month"], monthly_count["headline_count"], marker="o", linestyle="-", color="purple")
plt.xlim(pd.Timestamp("2015-01-01"), pd.Timestamp("2025-12-31"))
plt.ylim(3000,7500)
plt.xlabel("Time (2015–2025)")
plt.ylabel("Number of Headlines")
plt.title("Number of Headlines Per Month (2015–2025)")
plt.tight_layout()

figures_path = os.path.join(script_dir, "../figures/nyt_monthly_headline_count_trend.png")
plt.savefig(figures_path)
print(f"Figure saved to: {figures_path}")

#8: monthly trends

df_filtered = df[(df["year"] >= 2016) & (df["year"] <= 2025)]
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month

monthly_happiness = df.groupby(["year","month"])["happiness_score"].mean().reset_index()

pivot_happiness = monthly_happiness.pivot(index="month", columns="year", values="happiness_score")

print("\nPivot table (months x years) - first few rows:")
print(pivot_happiness.head())

plt.figure(figsize=(12,6))

for year in pivot_happiness.columns:
    plt.plot(pivot_happiness.index, pivot_happiness[year], marker='o', label=str(year))

plt.xticks(range(1,13), ["Jan","Feb","Mar","Apr","May","Jun",
                         "Jul","Aug","Sep","Oct","Nov","Dec"])

plt.xlabel("Month")
plt.ylabel("Average Happiness Score")
plt.title("Monthly Happiness Trends by Year (2016–2025)")
plt.ylim(5.3,5.65)  # Happiness score range
plt.legend(title="Year")
plt.grid(alpha=0.3)
plt.tight_layout()

figures_path = os.path.join(script_dir, "../figures/nyt_monthly_happiness_trends_by_year.png")
plt.savefig(figures_path)
print(f"Figure saved to: {figures_path}")

## monthly averages (across years)

df_filtered = df[(df["year"] >= 2015) & (df["year"] <= 2025)]
df_filtered["month"] = df_filtered["date"].dt.month
monthly_mean = df_filtered.groupby("month")["happiness_score"].mean().reset_index()
print("\nAverage happiness per month:")
print(monthly_mean)

plt.figure(figsize=(10,6))

plt.plot(
    monthly_mean["month"],
    monthly_mean["happiness_score"],
    marker="o",
    linewidth=2
)

plt.xticks(
    range(1,13),
    ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
)

plt.xlabel("Month")
plt.ylabel("Average Happiness Score")
plt.title("Average Monthly Happiness Pattern (2015–2025)")

plt.ylim(5.45, 5.6)

plt.grid(alpha=0.3)

plt.tight_layout()

figures_path = os.path.join(script_dir, "../figures/nyt_average_monthly_happiness_pattern.png")
plt.savefig(figures_path)
print(f"Figure saved to: {figures_path}")

#9: happiness distribution

plt.figure(figsize=(10,6))

plt.hist(df["happiness_score"], bins=30, color="skyblue", edgecolor="black")

plt.xlabel("Happiness Score")
plt.ylabel("Number of Headlines")
plt.title("Distribution of Happiness Scores in the Corpus")

plt.xlim(0,10)

plt.grid(alpha=0.3)
plt.tight_layout()

figures_path = os.path.join(script_dir, "../figures/nyt_happiness_score_distribution.png")
plt.savefig(figures_path)
print(f"Figure saved to: {figures_path}")

#10: trends in match count

no_match_df = df[df["match_count"] == 0]

print("\nRows with match_count = 0:")
print(no_match_df.shape)

no_match_df["year_month"] = no_match_df["date"].dt.to_period("M")

monthly_no_match = no_match_df.groupby("year_month").size().reset_index(name="no_match_count")

monthly_no_match["year_month"] = monthly_no_match["year_month"].dt.to_timestamp()

print("\nMonthly rows with match_count = 0:")
print(monthly_no_match.head())

plt.figure(figsize=(12,6))

plt.plot(
    monthly_no_match["year_month"],
    monthly_no_match["no_match_count"],
    marker="o",
    color="red"
)

plt.xlabel("Time (2015–2025)")
plt.ylabel("Number of Headlines with match_count = 0")
plt.title("Headlines Without Lexicon Matches Over Time")

plt.xlim(pd.Timestamp("2015-01-01"), pd.Timestamp("2025-12-31"))

plt.xticks(rotation=45)
plt.grid(alpha=0.3)

plt.tight_layout()

figures_path = os.path.join(script_dir, "../figures/nyt_no_match_trend.png")
plt.savefig(figures_path)
print(f"Figure saved to: {figures_path}")

#11: most positive and most negative headlines

most_positive = df.sort_values(by="happiness_score", ascending=False).head(15)

print("\nTop 15 Most Positive Headlines:")
print(most_positive[["date", "happiness_score", "tokenized_words", "match_count"]])

most_negative = df.sort_values(by="happiness_score", ascending=True).head(15)

print("\nTop 15 Most Negative Headlines:")
print(most_negative[["date", "happiness_score", "tokenized_words", "match_count"]])

positive_path = os.path.join(script_dir, "../tables/nyt_top_15_positive_headlines.csv")
negative_path = os.path.join(script_dir, "../tables/nyt_top_15_negative_headlines.csv")

most_positive.to_csv(positive_path, index=False)
most_negative.to_csv(negative_path, index=False)

print("\nTables saved:")
print(positive_path)
print(negative_path)

#12: random sample: Match count 0

no_match_df = df[df["match_count"] == 0]

random_no_match = no_match_df.groupby("year").sample(n=1, random_state=42)

random_no_match = random_no_match.sort_values("year")

print("\nRandom headline with match_count = 0 for each year:")
print(random_no_match[["year", "date", "tokenized_words", "match_count"]])

table_path = os.path.join(script_dir, "../tables/nyt_random_zero_match_headlines_by_year.csv")

random_no_match.to_csv(table_path, index=False)

print(f"\nTable saved to: {table_path}")