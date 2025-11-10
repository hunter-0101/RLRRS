# RL-based-Research-Recommendation-System
## Phase 0 — Setup & Initialization
**Goal:** Set up environment, structure, and basic configs.
**Checklist:**
- [x] **Create project folder** structure as specified (`personalized_paper_recommender/`).
- [x] **Set up virtual environment** and install dependencies: `pip install torch transformers datasets trl pandas scikit-learn streamlit tqdm arxiv shap`
- [ ] **Create and edit** `requirements.txt` with all dependencies.
- [x] **Write** `config/config.py`
    - Define paths, model name (`distilbert-base-uncased`), API settings, and hyperparameters.
- [x] **Write** `config/constants.py`
    - Define `INTEREST_KEYWORDS`, categories to fetch, and initial parameters (e.g., top_k = 500).

**Output:** Working environment + basic config scaffolding.
## Phase 1 — Data Acquisition & Baseline
**Goal:** Collect paper data and label first batch.
### Step 1. Data Fetching
- [ ] **Create** `data_collector/arxiv_fetcher.py`
	- [ ] Use the `arxiv` package to query categories like `"cs.AI", "cs.LG", "stat.ML"`.
	- [ ] Collect metadata: `id`, `title`, `authors`, `abstract`, `categories`.
	- [ ] Save into `data/arxiv_master_data.csv`.
- [ ] **Test script** with small query (`max_results=20`) before full run.
### Step 2. Data Processing Utilities
- [ ] **Write** `data_utils/schema.py` → defines expected columns.
- [ ] **Write** `data_utils/io_utils.py` → handles safe CSV read/write.
- [ ] **Write** `data_utils/processing.py` → merges new data, cleans text, deduplicates titles.
### Step 3. Baseline Model
- [ ] **Write** `baseline/keyword_filter.py`
	- [ ] Implement scoring by keyword match ratio or TF-IDF cosine similarity.
- [ ] **Write** `baseline/baseline_runner.py`
	- [ ] Apply baseline to all titles and produce a `rule_score` column.
	- [ ] Select top 500 for labeling.
### Step 4. Manual Labeling
- [ ] **Write** `labeling/labeling_cli.py`
	- [ ] CLI app that displays title + abstract, records rating (1–10).
	- [ ] Append labeled entries to `data/labeled_data.csv`.
**Output:** `arxiv_master_data.csv` (~10k rows) + `labeled_data.csv` (~300 rows with ratings).
## Phase 2 — Supervised Fine-Tuning
**Goal:** Train a DistilBERT regression model that predicts interest scores.
### Step 1. Prepare Data
- [ ] **In** `data_utils/processing.py`, add function to create a Hugging Face `Dataset` from `labeled_data.csv`.
- [ ] Split into train/validation (80/20).
### Step 2. Model Fine-Tuning
- [ ] **Write** `models/sft_trainer.py`
	- [ ] Load `distilbert-base-uncased` from Hugging Face.
	- [ ] Use `DistilBertForSequenceClassification` with `num_labels=1`.
	- [ ] Implement regression training (`MSELoss`).
	- [ ] Save best checkpoint to `models/sft_model/`.
- [ ] **Write** `models/evaluate_model.py`
	- [ ] Compute RMSE and Spearman correlation.
### Step 3. Test Predictions
- [ ] Use trained SFT model to predict interest scores for all unlabeled papers.
- [ ] Verify that top predictions look reasonable.

**Output:** A functioning SFT model (`models/sft_model/`) + evaluation results.
## Phase 3 — RLHF / DPO Fine-Tuning
**Goal:** Improve personalization using reinforcement feedback.
### Step 1. Set Up Preference Data
- [ ] **Extend** labeling interface to allow **pairwise ratings** (A > B).
	- [ ] E.g., show two titles, you pick which one's more interesting.
- [ ] Save preferences as pairs in `data/preference_data.csv`.
### Step 2. Implement DPO Training
- [ ] **Write** `models/rl_trainer.py`
	- [ ] Use Hugging Face TRL's `DPOTrainer`.
	- [ ] Initialize with:
		- `policy_model = load_sft_model()`
		- `ref_model = frozen_sft_model()`
	- [ ] Train on pairwise data from `preference_data.csv`.
	- [ ] Save final model as `models/policy_model/`.
### Step 3. Validate Model Quality
- [ ] Use `models/evaluate_model.py` to compare SFT vs. DPO predictions.
- [ ] Manually inspect top 10 DPO recommendations.
**Output:** Personalized policy model (`models/policy_model/`) that better reflects subjective taste.
## Phase 4 — Deployment & Continuous Learning
**Goal:** Automate daily recommendations and periodic retraining.
### Step 1. Daily Recommendation Pipeline
- [ ] **Write** `pipeline/daily_recommender.py`
	- [ ] Fetch new arXiv papers.
	- [ ] Score each using `policy_model`.
	- [ ] Output top 10 titles (CLI or simple Streamlit app).
### Step 2. Retraining Script
- [ ] **Write** `pipeline/retrainer.py`
	- [ ] Merge newly labeled data.
	- [ ] Re-run `sft_trainer.py` and `rl_trainer.py`.
	- [ ] Optionally schedule via `cron` or `Windows Task Scheduler`.
### Step 3. Logging & Explainability
- [ ] **Write** `logs/feature_analysis.py`
	- [ ] Use SHAP or attention weights to log top influential keywords.
	- [ ] Save as `logs/feature_importance.json`.
**Output:** Fully functioning recommender that updates itself and logs insights.
## Phase 5 — Refinement & Maintenance
**Goal:** Polish usability, modularity, and documentation.
**Checklist:**
- [ ] Add a `README.md` explaining setup and usage.
- [ ] Document each function with docstrings.
- [ ] Write `main.py` as project entry point:
	- [ ] `python main.py collect` → fetch new data
	- [ ] `python main.py label` → start labeling
	- [ ] `python main.py train` → train SFT
	- [ ] `python main.py recommend` → get top 10 papers
- [ ] Clean up code style with `black` and `flake8`.
- [ ] (Optional) Containerize using `Dockerfile`.
**Output:** A reusable, modular, production-ready personal recommender system.
## Optional Stretch Goals (Post-MVP)
- [ ] Add semantic embedding search using `sentence-transformers`.
- [ ] Implement a **hybrid model**: rule-based + learned model ensemble.
- [ ] Add a **memory-based cold-start module** that uses your initial keyword vectors.
- [ ] Deploy simple Streamlit dashboard for daily recommendations.
