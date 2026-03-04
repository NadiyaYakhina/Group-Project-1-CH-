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

## Commit Task 1 (1.1, 1.2, 1.3) 02/03/26
The file was loaded through downloading the assignment folder and opening the project on vscode. All group members connected to the project via github. Each group member accomplished commits after completing a fraction of the assignment. This task required a pull and a push after its successful completion. Lines 99-104 of code read the csv and ignored the first 3 rows of the data, indicated that data is separated by tabs (sep =\t"). 
Shape of dataset =  (rows, columns): (10222, 8)
A missing rank (--) in this dataset means that the information for this category is not available, and is replaced in the code by NaN. 

Data dictionary: 
| Name | Data represented  | dtype | Notes on missingness |
| --- | --- | --- | --- |
| word | data analysed | text | no misses |
| happiness_rank| position closer/further to "happiness" coordinate| float | no misses |
| happiness_average | average of __| float | no misses |
| happiness_standard_deviation | standard deviation of word from 0 | float | no misses |
| twitter_rank 
| google_rank
| nyt_rank
| lyrics_rank
| --- | --- | --- | --- | 

Sanity checks: 
| --- | --- | --- | --- | --- | --- | --- | --- | --- |  
| word | happiness_rank | happiness_average | happiness_standard_deviation | twitter_rank | google_rank | nyt_rank | lyrics_rank |
| 33 | friendship | 34 | 7.96 | 1.1241 | 4273.0 | 3098.0 | 3669.0 | 3980.0 |
|1543 | designers | 1544 | 6.38 | 1.4831 | NaN | NaN | 3890.0 | NaN |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |  

The two rows above show a clear distinguishment between the ranks of them by happiness, and hence, their position on the list. Friendship is drawn "34" for average happiness, while "designers" remains 1544. Considering freinship to have more positive stigma attached to it, "it makes sense" why it is higher than designers. Standard deviation also shows that friendship is positionned higher on the "happiness" deviation than designers. 
Most postitive and most negative words do make sense, by "making sense" I mean that the positive words are ones, that a human would consider positive, and most negative ones are those, that a human would consider most negative. Hence, the model "makes sense" to a human becuase it seems to understand what a human want it to do, aligning with the humans expectations. 
