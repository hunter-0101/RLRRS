# schema.py
"""
Defines the expected schema (column names) for arXiv paper data.
Used for validation and standardization across modules.
"""

from typing import List

# List of expected fields for each paper entry
ARXIV_COLUMNS: List[str] = [
    "id",
    "title",
    "authors",
    "abstract",
    "categories",
    "published",
    "updated"
]

# Optional: define a minimal validation utility
def validate_columns(df, expected_cols=ARXIV_COLUMNS):
    """Ensure dataframe has all expected columns."""
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return True
