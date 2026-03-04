# Seminars 3 & 4 — Hedonometer (Project Folder)

This folder provides an **example project structure** (and an instructor/demo script) for the Seminars 3 & 4 group project using the **labMT 1.0** dataset (Data Set S1 from the Hedonometer paper).

It includes:
- the labMT 1.0 dataset file (`data/raw/Data_Set_S1.txt`)
- a runnable demo analysis script (`src/hedonometer_labmt_demo.py`) that produces a *typical* set of outputs aligned to the assignment
- course documents in `docs/` (original paper + paper companion + assignment + project quickstart), provided as **.pdf**

## Folder layout (course convention)

- `src/` — Python scripts you run
- `data/raw/` — input data (treat as read-only)
- `figures/` — PNG plots (embed these in your GitHub README)
- `tables/` — CSV tables/summaries (optional to embed, but useful for analysis)
- `docs/` — assignment + paper companion + quickstart handout

## Setup + run (from the project root)

### 1) Create a virtual environment

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
```

**Windows (PowerShell)**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
```

### 2) Install dependencies
```bash
python3 -m pip install -r requirements.txt
```

### 3) Run the demo analysis
```bash
python3 src/run_analysis.py
```

### What gets generated?
After running, look in:
- `figures/` — PNG plots
- `tables/` — CSV summary tables

## Our Exploration

## Step 2: Quantitative Exploration:

### 2.1 Distribution of happiness scores

To understand the emotional baseline of the dataset, descriptive statistics were calculated (Table 1) and visualised on a histogram (Figure 4) with the distribution of happiness scores across the 10,222 unique words.

The summary of statistics:
| Metric | Value |
| :--- | :--- |
| **Count** | 10,222 words |
| **Mean** | 5.38 |
| **Median** | 5.44 |
| **Standart Dev** | 1.08 |
| **5th Percentile** | 3.18 |
| **95th Percentile** | 7.08 |
|Table 1: Hapiness average summary statistics |

![Happiness Histogram](figures/happiness_average_hist.png)
Figure 4: Distribution of average happiness scores across the labMT 1.0 dataset.

### Analysis:
  
Looking at the mean (5.38) and median (5.44), considering that the scale is 1 to 9 (with a neutral score of 5), the data has a skew to the right or, in other words, the findings show that people find language a little more positive.

The one pattern we did not expect was to see that takinf the closer look on the right side of the histogram, one can see a kind of negative "tail" in the dataset, showing that even if the whole dataset in quantity is skewed to be more positive, there are more diverse words to represent negativity.

