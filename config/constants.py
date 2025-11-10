"""
config/constants.py
-------------------
Project constants for keywords, category lists, and baseline parameters.
These are human-editable definitions that describe what the user initially finds "interesting."
"""

# ---------------------------------------------------------------------
# Baseline Keyword Definitions
# ---------------------------------------------------------------------
# You can refine these over time based on your interests.
INTEREST_KEYWORDS = [
    # Core ML/AI interest themes
    "representation", "optimization", "geometry", "reasoning", "symbolic",
    "interpretability", "causality", "meta-learning", "generalization",
    "transformer", "large language model", "fine-tuning", "embeddings",
    "reinforcement", "abstraction", "structure", "modularity", "alignment",
    "mathematical", "theoretical", "cognitive", "conceptual",
]

# ---------------------------------------------------------------------
# arXiv Categories to Fetch
# ---------------------------------------------------------------------
# You can extend or restrict these to target specific domains.
ARXIV_CATEGORIES = [
    "cs.AI",      # Artificial Intelligence
    "cs.LG",      # Machine Learning
    "stat.ML",    # Statistics - Machine Learning
    "cs.CL",      # Computation and Language
    "cs.NE",      # Neural and Evolutionary Computing
    "math.ST",    # Statistics Theory
]

# ---------------------------------------------------------------------
# Baseline Parameters
# ---------------------------------------------------------------------
TOP_K_BASELINE_SELECTION = 500    # number of top keyword-matched papers to label initially
BASELINE_MIN_KEYWORD_MATCH = 0.15 # min ratio of keywords that must appear for selection
BASELINE_USE_TFIDF = True         # toggle between simple match or TF-IDF scoring

# ---------------------------------------------------------------------
# Labeling Interface Settings
# ---------------------------------------------------------------------
LABEL_SCALE = list(range(1, 11))  # interest scale (1–10)
LABEL_BATCH_SIZE = 20             # number of papers per labeling session

# ---------------------------------------------------------------------
# Evaluation Thresholds
# ---------------------------------------------------------------------
# for interpreting model performance
RMSE_THRESHOLD = 1.5
SPEARMAN_THRESHOLD = 0.6

# ---------------------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------------------
MAX_LOG_FILE_SIZE_MB = 5
KEEP_PREVIOUS_LOGS = True
