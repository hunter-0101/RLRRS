# processing.py
"""
Processes raw arXiv metadata:
- Cleans text (titles, abstracts)
- Removes duplicates
- Merges with existing master dataset
"""

import pandas as pd
import re
from rlrrs.data_utils.io_utils import safe_read_csv, safe_write_csv
from rlrrs.data_utils.schema import validate_columns
from rlrrs.config.config import ARXIV_OUTPUT_FILE, MASTER_FILE


def clean_text(text: str) -> str:
    """Clean text by removing excess whitespace and punctuation artifacts."""
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply cleaning to title and abstract columns."""
    df["title"] = df["title"].astype(str).apply(clean_text)
    df["abstract"] = df["abstract"].astype(str).apply(clean_text)
    df.drop_duplicates(subset=["title"], inplace=True)
    return df


def merge_with_existing(new_df: pd.DataFrame):
    """Merge newly fetched data with the existing master dataset."""
    existing_df = safe_read_csv(MASTER_FILE)
    if not existing_df.empty:
        combined = pd.concat([existing_df, new_df], ignore_index=True)
        combined.drop_duplicates(subset=["title"], inplace=True)
        print(f"🧩 Merged {len(new_df)} new papers, total {len(combined)} unique papers.")
    else:
        combined = new_df
        print(f"🆕 Initialized master dataset with {len(new_df)} papers.")
    safe_write_csv(combined, MASTER_FILE)


def main():
    df = safe_read_csv(ARXIV_OUTPUT_FILE)
    validate_columns(df)
    df = preprocess_dataframe(df)
    merge_with_existing(df)
    print(f"✅ Processing complete. Master file updated: {MASTER_FILE}")


if __name__ == "__main__":
    main()
