# arxiv_fetcher.py
"""
Fetches paper metadata from arXiv using the 'arxiv' package.
Queries selected categories and stores results into `data/arxiv_master_data.csv`.
"""

import os
import time
import arxiv
import pandas as pd
from datetime import datetime
from config.config import DATA_DIR, ARXIV_QUERY_SETTINGS, DATA_DIR
from data_utils.schema import ARXIV_COLUMNS
from data_utils.io_utils import safe_write_csv


def fetch_category(category: str, max_results: int = 200) -> pd.DataFrame:
    """
    Fetch papers for a specific arXiv category.
    Returns a pandas DataFrame with standardized columns.
    """
    print(f"🔍 Fetching papers from category: {category} (max_results={max_results})")
    search = arxiv.Search(
        query=f"cat:{category}",
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    records = []
    for result in search.results():
        records.append({
            "id": result.entry_id.split("/")[-1],
            "title": result.title.strip().replace("\n", " "),
            "authors": ", ".join([a.name for a in result.authors]),
            "abstract": result.summary.strip().replace("\n", " "),
            "categories": ", ".join(result.categories),
            "published": result.published.strftime("%Y-%m-%d"),
            "updated": result.updated.strftime("%Y-%m-%d"),
        })
        time.sleep(0.2)  # Be polite to arXiv servers

    df = pd.DataFrame(records, columns=ARXIV_COLUMNS)
    print(f"✅ Retrieved {len(df)} papers from {category}")
    return df


def fetch_all_categories(categories, max_results):
    """Fetch and concatenate results from multiple categories."""
    all_data = []
    for cat in categories:
        try:
            df = fetch_category(cat, max_results)
            all_data.append(df)
        except Exception as e:
            print(f"⚠️ Error fetching category {cat}: {e}")
    return pd.concat(all_data, ignore_index=True)


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    print("🚀 Starting arXiv data fetch...")
    df = fetch_all_categories(ARXIV_QUERY_SETTINGS["categories"], ARXIV_QUERY_SETTINGS["max_results"])
    print(f"📦 Total papers collected: {len(df)}")
    safe_write_csv(df, DATA_DIR, "arxiv_master_data.csv")
    print(f"💾 Saved to {DATA_DIR}")


if __name__ == "__main__":
    main()
