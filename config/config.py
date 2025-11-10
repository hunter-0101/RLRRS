"""
config/config.py
----------------
Global configuration file for the personalized paper recommender project.

This file defines:
- Directory paths for data, models, and logs
- Model and tokenizer names
- arXiv API and data acquisition settings
- Hyperparameters for training (SFT & RL phases)
"""

import os
from datetime import datetime

# ---------------------------------------------------------------------
# Project Root & Paths
# ---------------------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MODEL_DIR = os.path.join(PROJECT_ROOT, "models")
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# ---------------------------------------------------------------------
# Data File Paths
# ---------------------------------------------------------------------
ARXIV_MASTER_DATA = os.path.join(DATA_DIR, "arxiv_master_data.csv")
LABELED_DATA = os.path.join(DATA_DIR, "labeled_data.csv")
PREFERENCE_DATA = os.path.join(DATA_DIR, "preference_data.csv")

# ---------------------------------------------------------------------
# Model Configuration
# ---------------------------------------------------------------------
MODEL_NAME = "distilbert-base-uncased"  # base LM for SFT and RL
TOKENIZER_NAME = MODEL_NAME

SFT_MODEL_DIR = os.path.join(MODEL_DIR, "sft_model")
RL_MODEL_DIR = os.path.join(MODEL_DIR, "policy_model")

# ---------------------------------------------------------------------
# Training Hyperparameters
# ---------------------------------------------------------------------
SFT_HPARAMS = {
    "num_epochs": 4,
    "batch_size": 8,
    "learning_rate": 2e-5,
    "weight_decay": 0.01,
    "warmup_ratio": 0.1,
    "logging_steps": 50,
    "eval_steps": 200,
}

RL_HPARAMS = {
    "num_epochs": 3,
    "batch_size": 4,
    "learning_rate": 1e-5,
    "clip_range": 0.2,  # used by PPO/DPO-like updates
}

# ---------------------------------------------------------------------
# arXiv API Configuration
# ---------------------------------------------------------------------
ARXIV_QUERY_SETTINGS = {
    "max_results": 10000,   # total papers to fetch
    "sort_by": "submittedDate",
    "sort_order": "descending",
    "categories": ["cs.AI", "cs.LG", "stat.ML"],  # can modify in constants.py too
}

# ---------------------------------------------------------------------
# Logging & Metadata
# ---------------------------------------------------------------------
RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
TRAIN_LOG_PATH = os.path.join(LOG_DIR, f"train_log_{RUN_ID}.json")
FEATURE_IMPORTANCE_PATH = os.path.join(LOG_DIR, "feature_importance.json")

# ---------------------------------------------------------------------
# Miscellaneous
# ---------------------------------------------------------------------
SEED = 42
DEVICE = "cpu"  # keeping CPU-friendly for now; change to "cuda" if available
DEBUG_MODE = False
