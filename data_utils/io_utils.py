# io_utils.py
"""
Provides safe input/output utilities for reading and writing CSV files.
Handles UTF-8 encoding, ensures directories exist, and avoids partial writes.
"""

import os
import pandas as pd
from tempfile import NamedTemporaryFile
import shutil


def ensure_dir(path: str):
    """Ensure that a directory exists."""
    os.makedirs(os.path.dirname(path), exist_ok=True)


def safe_write_csv(df: pd.DataFrame, path: str):
    """
    Write DataFrame safely to a CSV file.
    Uses a temporary file to avoid data corruption if process is interrupted.
    """
    ensure_dir(path)
    tmp = NamedTemporaryFile("w", delete=False, suffix=".csv", dir=os.path.dirname(path))
    try:
        df.to_csv(tmp.name, index=False, encoding="utf-8")
        shutil.move(tmp.name, path)
    finally:
        if os.path.exists(tmp.name):
            os.remove(tmp.name)


def safe_read_csv(path: str):
    """Read CSV if it exists; otherwise return an empty DataFrame."""
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path, encoding="utf-8")
