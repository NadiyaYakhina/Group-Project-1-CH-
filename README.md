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

## Step 1: 
### Step 1.1 
- The file was loaded through downloading the assignment folder and opening the project on VScode. 
- All group members connected to the project via github. Each group member accomplished commits after completing a fraction of the assignment. This task required a pull and a push after its successful completion. 
- Lines 99-104 of code read the csv and ignored the first 3 rows of the data, indicated that data is separated by tabs (sep =\t"). 
- hape of dataset =  (rows, columns): (10222, 8)
- A missing rank (--) in this dataset means that the information for this category is not available, and is replaced in the code by NaN. Broadly speaking, this means that the word was not present for the top 5000 words on the platform.

### Step 1.2
Data dictionary: 
| Name | Data represented  | dtype | Misses |
| --- | --- | --- | --- |
| word | data analysed | text (string) | 0 |
| happiness_rank| list of words based on highest to lowest happiness average| float64 | 0 |
| happiness_average | happiness attached to word (based on 50 itereations) | float64 | 0 |
| happiness_standard_deviation | Extent of controversy when assigning happiness rank  | float64 | 0 |
| twitter_rank | Rank of frequency of word on platform | float64 | 5222 |
| google_rank | Rank of frequency of word on platform | float64 | 5222 |
| nyt_rank | Rank of frequency of word on platform | float64 | 5222 |
| lyrics_rank | Rank of frequency of word on platform | float64 | 5222 |

### Step 1.3 - Sanity checks: 
| word | happiness_rank | happiness_average | happiness_standard_deviation | twitter_rank | google_rank | nyt_rank | lyrics_rank |
:--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| friendship | 34 | 7.96 | 1.1241 | 4273.0 | 3098.0 | 3669.0 | 3980.0 |
| designers | 1544 | 6.38 | 1.4831 | NaN | NaN | 3890.0 | NaN |

Explanation:
- The two rows above show a clear distinguishment between the ranks of them by happiness, and hence, their position on the list. "Friendship" is drawn 34th for average happiness, while "designers" remains 1544. Considering "freindship" to have more positive stigma attached to it, "it makes sense" why it is higher than designers. 
- Standard deviation also shows that there was more controversy attached to applying a happiness metric to "designers" than to "friendshi"p" (1.48 vs 1.12, respectively). 
- Most postitive and most negative words do make sense, by "making sense", we imply that the positive words are ones, that a human would consider positive, and most negative ones are those, that a human would consider most negative. Hence, the model "makes sense" to a human becuase it seems to understand what a human want it to do, aligning with the humans expectations. 

## Step 2: Quantitative Exploration:

### 2.1 Distribution of happiness scores

To understand the emotional rating of the dataset, descriptive statistics were calculated (Table 1) and visualised on a histogram (Figure 4) with the distribution of happiness scores across the 10,222 unique words.

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
  
* Looking at the mean (5.38) and median (5.44), considering that the scale is 1 to 9, the data has a skew to the right or, in other words, the findings show that people find language a little more positive on average.

* The one pattern we did not expect was to see a kind of negative "tail" on the left side of the dataset, showing that even though the whole dataset in quantity is skewed to be more positive, there are more diverse words to represent negativity.

## 2.1 Disagreement: which words are “contested”?

Since the dataset also presents standart deviation for each word, one might take a look into what were the words people disagreed most about, so where the scores differed more. The scatter plot (Figure 2) maps out this comparison by taking average happiness score against the standard deviation. Therefore, points higher on the y-axis represent words with more disagreement.

![Disagreement Scatterplot](figures/happiness_vs_std_scatter.png)
Figure 2: Disagreement scatterplot

### Top 5 most contested words

| Word | Happiness Average | Standard Deviation |
| :--- | :--- | :--- |
| fucking | 4.64 | 2.93 |
| fuckin | 3.86 | 2.74 |
| fucked | 3.56 | 2.71 |
| pussy | 4.80 | 2.67 |
| whiskey | 5.72 | 2.64 |


#### Analysis of Findings
* Taking a closer look on the table above with top 5 most contested words, one can observe how all of them revolve around several sensitive categories. Applyign a more qualitative lens, words like "fucking," "fuckin," and "fucked" can be associated with profanity and taboo, therefore really vary in scores depending on the rater's sentitivity and initial associations. Moreover, words such as "pussy" may present a high disagreement due to the fact that it holds multiple and quite diverse meanings, from an animal to a offensive expletive. Lastly, the score of words might differ according to personal background and cultural baggage, therefore, such words as "whiskey" can evoke different associations depending on the cultural or even personal/family history with alchohol.
* We have decided to choose these five words, because they have the highest standart deviation (representing the most contested words) from the word list. 

## 2.3 Corpus comparison: what counts as “common language” depends on where you look

To understand the scope of the provided to us dataset, we first analyzed how many words from the 10,222-word lexicon are considered "common" (within the top 5,000 most frequent) in each individual media group.

![Corpus Coverage Bar Chart](figures/corpus_rank_coverage_bar.png)
Figure 3: How many words appear in each corpus rank?

#### Interpretation of the chart
* The bar chart shows that each corpus contains exactly 5,000. This just proves the dataset construction methodology. The fact that all bars are equal confirms that no single corpus is over- or under-represented.

* However, to understand how "common language" varies across the chosen social media channels presented in the dataset, we analyzed the overlap of the top 5,000 most frequent words from each group.

#### Word Overlap Heatmap
The heatmap below shows the raw number of shared words between each pair of channels. 

![Corpus Overlap Heatmap](figures/corpus_overlap_heatmap.png)
Figure 4: The overlap heatmap

### Analysis:
* The diagonal of dark blue squares shows exactly 5,000 words for each, confirming that data was constructed using the top 5,000 words from each source. Highest overlap can be found in Twitter and Music Lyrics as they share the most vocabulary 3,127 words. 
* In contrast, the lowest overlap can be found between Music Lyrics and the New York Times (2,241 words), showcasing a significant difference between professional news medium and songwriting.

#### Spearman Rank Correlation
To take it a step further we calculated the Spearman correlation coefficient to determine if words that are popular in one corpus tend to be popular in others as well.

| Channel Pair | Spearman Correlation |
| :--- | :--- |
| Twitter + Lyrics | 0.62 |
| Google Books + NYT | 0.60 |
| Twitter + NYT | 0.47 |
| NYT + Lyrics | 0.38 |

### Analysis:
* The strongest correlation (0.62) was found between Twitter and Lyrics, showing that social media speech patterns are closer to the vocabulary used in modern music than to other media channels. 
* In contrast, as already highlighted in the heatmap the NYT and Lyrics have the weakest correlation (0.38), shoeing how  the "common" vocabulary of news and artistic lyrics are most distinct in this dataset compared to the other media channels.

### One example
We used the provided labMT 1.0 frequency data to generate our own custom analysis. By running our script, we produced the twitter_common_nyt_missing_top20.csv to help identify what words would ranked high and in general appear in the dataset of Twitter but are not in the NYT corpora.

#### Extract from the table: Words on Twitter but missing in NYT

| word | twitter_rank | happiness_average |
| :--- | :--- | :--- |
| **rt** | 15.0 | 4.88 |
| **lol** | 42.0 | 6.84 |
| **im** | 80.0 | 5.02 |
| **twitter** | 107.0 | 5.46 |
| **haha** | 135.0 | 7.64 |
| **ur** | 159.0 | 4.96 |
| **gonna** | 166.0 | 4.86 |
| **yeah** | 192.0 | 5.90 |
| **que** | 194.0 | 4.64 |
| **ya** | 195.0 | 5.22 |

### Analysis
* A concrete example of linguistic different can be found in the word 'rt', which stands for 'retweet'. It is one of the most frequent words in the Twitter corpus bacuse it presents an operational command specific to the platform but it is entirely missing from the New York Times 5,000 ranks.

## Step 3: Qualitative exploration: close reading the lexicon as a cultural artifact

### 3.1 Word Exhibit

| category | word | happiness_average | happiness_standard_deviation | twitter_rank | google_rank | nyt_rank | lyrics_rank |
|---|---|---|---|---|---|---|---|
| very positive | laughter | 8.5 | 0.9313 | 3600.0 |  |  | 1728.0 |
| very positive | happiness | 8.44 | 0.9723 | 1853.0 | 2458.0 |  | 1230.0 |
| very positive | love | 8.42 | 1.1082 | 25.0 | 317.0 | 328.0 | 23.0 |
| very positive | happy | 8.3 | 0.9949 | 65.0 | 1372.0 | 1313.0 | 375.0 |
| very positive | laughed | 8.26 | 1.1572 | 3334.0 | 3542.0 |  | 2332.0 |
| very negative | terrorist | 1.3 | 0.9091 | 3576.0 |  | 3026.0 |  |
| very negative | suicide | 1.3 | 0.8391 | 2124.0 | 4707.0 | 3319.0 | 2107.0 |
| very negative | rape | 1.44 | 0.7866 | 3133.0 |  | 4115.0 | 2977.0 |
| very negative | terrorism | 1.48 | 0.9089 |  |  | 3192.0 |  |
| very negative | murder | 1.48 | 1.015 | 2762.0 | 3110.0 | 1541.0 | 1059.0 |
| highly contested | fucking | 4.64 | 2.926 | 448.0 |  |  | 620.0 |
| highly contested | fuckin | 3.86 | 2.7405 | 1077.0 |  |  | 688.0 |
| highly contested | fucked | 3.56 | 2.7117 | 1840.0 |  |  | 904.0 |
| highly contested | pussy | 4.8 | 2.665 | 2019.0 |  |  | 949.0 |
| highly contested | whiskey | 5.72 | 2.6422 |  |  |  | 2208.0 |
| Twitter-common, NYT-missing | rt | 4.88 | 1.0622 | 15.0 |  |  |  |
| Twitter-common, NYT-missing | lol | 6.84 | 1.7884 | 42.0 |  |  |  |
| Twitter-common, NYT-missing | im | 5.02 | 1.1156 | 80.0 | 4093.0 |  | 315.0 |
| Twitter-common, NYT-missing | twitter | 5.46 | 1.9082 | 107.0 |  |  |  |
| Twitter-common, NYT-missing | haha | 7.64 | 1.3815 | 135.0 |  |  | 3211.0 |

The qualitiative analysis is informed by a close reading of our data where we studied 50 most positive and negative words and furthermore 50 highly contested words. 

* A close reading of the words that have the highest and lowest happiness average make clear certain patterns. These patterns can help in explaining the decision-making that informed the ranking of the words. 

* Firstly, the extreme ends of the happiness average table where we see the most positive and most negative words, include words that likely contain meanings that are largely consistent across contexts. For the most positive words, these included words used to express joyous emotions (e.g. happy, joy, etc.) occasions and events that are associated with positive experiences (e.g. christmas, beach, holidays), and objects symbolic of idealized happiness (e.g. butterflies, rainbows, etc.). On the other end, words with the least happiness average score carry a common theme of “fear” (e.g. death, murder, bomb, violence, etc.).

* Moreover, words with the hisghest standard deviation highlight words containing multiple meaning, highly contested topics and the overall most importantly it brings forth the significance of context within a language. This is evident through the profanity that come up (e.g. fuck, slut, pussy). Moreover, this included topics that are poitcially charged (e.g. capitalism, socialism), and culturally loaded (e.g. church, marriage, god). Interestingly, another pattern that emerges here include famous institutions (e.g. mcdonalds & walmart) that maybe signifier of larger debates online. 

* Lastly, we briefly looked at words that are frequent in the twitter ranking but do not appear in the NYT ranks corpus which, again, points to the contextual use of language that differs from time and place. Here, this is the difference in language use by a general public on social media vs edited, professional writing from a media company which is why informal/coloquial/slang words are not ranked by NYT.

## Step 4: Critical Reflection

4.1
Data Collection:
1. Collection of 4.6 billion tweets posted by over 63 million users in 33 months
2. 5000 most frequent words from four distinct sources. Totalling up to 10,222 unique words
3. Amazon’s Mechanical Turk was used to obtain the human happiness rating. Independent users rated each word on a scale from 1 to 9
4. A “naive” algorithm calculated the weighted average of the happiness scores 
5. A tunable “stop word” filter was implemented to exclude neutral words (e.g. obtained a score near 5) to refine the instrument's focus on more emotional language 
6. The updated instrument was applied back to the dataset to identify patterns across hours, days, years, and, lastly, ambient happiness scores.

4.2
1. Frequency-based word selection
- Choice: The researchers selected words based on how often they appear across the four sources 
- Consequence: This makes it easier to cover high volumes of text; however, it can make it harder to capture the emotional impact of words that have a lower frequency but are highly potent. 
- Example: Inclusion of words like ‘the’ (4.94), and ‘of’ (4.94). These words required a separate filtering process to remove these words so they dont distort the sentiment measurement 
2. The "Bag-of-Words" Naive Algorithm
- Choice: The method calculates the average of word scores, ignoring sentence structure, grammar, and context
- Consequence: The computational process is efficient, but it’s harder to detect sarcasm, negation, or multiple meanings.
- Example: Analyzing Tiger Woods, words like “car” and “sex” were scored as positive in isolation, although in context of that specific scandal were negative
3. Crowdsourcing via Mechanical Turk.
- Choice: usage of anonymous online workers to provide the foundational happiness scores.
- Consequence: easier to scale the dataset tenfold, but it’s challenging to take into account cultural or demographic biases, as the rating reflects a “generic reader” rather than representing the global population 
- Example: In the paper, the researchers highlight how the Turk rating correlates with the student-based ANEW study, while Twitter users remain a non-representative subpopulation.
4. Implementing a center-band filter ($\Delta h_{avg} = 1$)
- Choice: Researchers excluded all words with a happiness rating of between 4 and 6. 
- Consequence: This improves the instrument's sensitivity to emotional shifts. However, it makes it more brittle because it discards about 64% of the words, substantially reducing the total coverage. 
- Example: The removal of words like ‘truck’ and ‘sleep’, which scored near 5, makes identifying emotional shifts during major events such as holidays or disasters. 
5. Equality weighting of all users
- Choice: news organisation tweets have the same weight as individual users
- Consequence: “societal-scale” level of happiness is easier to measure as a form of “crowd-sourced media”. Although this makes it harder to differentiate genuine personal emotion from the sheer volume of news reporting
- Example: Osama Bin Laden’s death was recorded as the least happy day in the time frame as a result of the rise in negative news-related words, like “dead”, “death”, and “killed”, even if many users felt positive about the event.

4.3
We would trust the hedonometer to reliably measure large-scale population happiness levels over time. The hedomenter is exceptionally skilled at identifying system-wide social synchrony, e.g. recourrring happiness peaks on holidays or substantial reductions as a consequence of major social traumas, like natural disasters, or celebrity deaths. The hedonometer operates as a sensing tool for capturing the overall mood of the digital public all around. 
The hedonometer should not be used to interpret psychological happiness parameters or societal well-being, as the model overlooks context; it’s not recommended to be used for short, isolated text, where sarcasm or negation would be overlooked. Furthermore, these limitations show how this is not representative of a truly universal human sentiment, as Twitter users are non- representative of the subpopulation and the word list is biased toward English.
To improve the instrument, a few elements can be updated. First, the incorporation of N-grams to help contextualize meanings such as “child abuse” or “not bad”, which can not be detected by a single-word approach. Second, a stronger language detection would allow non-English tweets to be ensured with appropriate sentiment scores. Third, implementing geographic and demographic metadata allows sentiment to be analyzed across different regions or groups rather than as a “generic reader”. The instrument could also be implemented with more diverse annotator pools, multi-dimensional emotional categories, and regular updates to maintain a contemporary language. Instead of measuring happiness as a quantity, the updated version should frame happiness as measuring public emotional expression within a specific cultural and technological context. 

## Credits: 
Repo & workflow lead: Sara
Data wrangler: Valerija
Quantitative analyst: Nadiya
Qualitative/close reading lead: Sadia 
Provenance and Critique lead: Merey
Editor and Figure curator: Nadiya

## Refereences: 
Dodds PS, Harris KD, Kloumann IM, Bliss CA, Danforth CM (2011) Temporal Patterns of Happiness and Information in a Global Social Network:
Hedonometrics and Twitter. PLoS ONE 6(12): e26752. doi:10.1371/journal.pone.0026752 
