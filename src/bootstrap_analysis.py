from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#1 paths 

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

data_path = PROJECT_DIR / "data" / "processed" / "scored_nyt_headlines.csv"
output_dir = PROJECT_DIR / "figures"
output_dir.mkdir(parents=True, exist_ok=True)

print("Loading data from:", data_path)

#2 dataset
df = pd.read_csv(data_path)


#3 Create year-month column

df["year_month"] = df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2)

#4 monthly averages
monthly_means = df.groupby("year_month")["happiness_score"].mean()

#5 finding median
median_value = monthly_means.median()
normal_month = (monthly_means - median_value).abs().idxmin()

print("\nMedian happiness:", median_value)
print("Chosen representative month:", normal_month)

#6 choosing outlier month (determined from time-series)
outlier_month = "2021-01"  

print("Outlier month:", outlier_month)

#7 checking sample sizes
outlier_scores = df[df["year_month"] == outlier_month]["happiness_score"].dropna().values
normal_scores = df[df["year_month"] == normal_month]["happiness_score"].dropna().values

print("\nSample sizes:")
print("Outlier:", len(outlier_scores))
print("Median-Representative:", len(normal_scores))

# Safety check
if len(outlier_scores) == 0 or len(normal_scores) == 0:
    raise ValueError("One of the months has no data. Check month names.")

#8 bootstrap function
def bootstrap_means(data, n_bootstrap=1000):
    means = []
    n = len(data)

    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=n, replace=True)
        means.append(np.mean(sample))

    return np.array(means)

#9 running bootstrap
boot_outlier = bootstrap_means(outlier_scores)
boot_normal = bootstrap_means(normal_scores)

#10 confidence intervals
def ci(data):
    return np.percentile(data, 2.5), np.percentile(data, 97.5)

outlier_ci = ci(boot_outlier)
normal_ci = ci(boot_normal)

print("\n95% Confidence Intervals:")
print("Outlier:", outlier_ci)
print("Median-Representative:", normal_ci)

#11 plot results
plt.figure(figsize=(9, 5))

plt.hist(boot_outlier, bins=30, alpha=0.6, label=f"Outlier ({outlier_month})")
plt.hist(boot_normal, bins=30, alpha=0.6, label=f"Median-Representative ({normal_month})")

plt.axvline(outlier_ci[0], color="blue", linestyle="--")
plt.axvline(outlier_ci[1], color="blue", linestyle="--")

plt.axvline(normal_ci[0], color="orange", linestyle=":")
plt.axvline(normal_ci[1], color="orange", linestyle=":")

plt.title("Bootstrap Comparison of Monthly Happiness")
plt.xlabel("Mean happiness score")
plt.ylabel("Frequency")
plt.legend()

#12 saving figures
output_file = output_dir / "bootstrap_comparison.png"
plt.savefig(output_file, dpi=300, bbox_inches="tight")

print("\nSaved figure to:", output_file)

plt.show()