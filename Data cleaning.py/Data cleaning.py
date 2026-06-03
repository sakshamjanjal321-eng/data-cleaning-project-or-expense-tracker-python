"""
Data Cleaning Project
=====================
A complete, reusable data cleaning pipeline using Python & Pandas.
Handles: nulls, duplicates, wrong formats, inconsistent columns, outliers.

Usage:
    python data_cleaning.py

Input:  raw_data.csv  (place in same folder)
Output: clean_data.csv
"""

import pandas as pd
import numpy as np
import os

# ──────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────
INPUT_FILE  = "raw_data.csv"
OUTPUT_FILE = "clean_data.csv"

# Columns expected to be numeric (adjust to your dataset)
NUMERIC_COLS = ["age", "salary", "score"]

# Columns expected to be dates (adjust to your dataset)
DATE_COLS = ["date_joined", "last_active"]

# Columns that must not be null (rows dropped if missing)
REQUIRED_COLS = ["id", "name"]


# ──────────────────────────────────────────
# STEP 1 — LOAD & PROFILE
# ──────────────────────────────────────────
def load_and_profile(filepath: str) -> pd.DataFrame:
    """Load CSV and print a quick data quality report."""
    if not os.path.exists(filepath):
        # Generate a small demo dataset if no file provided
        print(f"[INFO] '{filepath}' not found — generating demo dataset.\n")
        df = generate_demo_data()
    else:
        df = pd.read_csv(filepath)

    print("=" * 50)
    print("DATA PROFILE — BEFORE CLEANING")
    print("=" * 50)
    print(f"Shape          : {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"Duplicates     : {df.duplicated().sum()} rows")
    print(f"\nNull counts:\n{df.isnull().sum()}")
    print(f"\nDtypes:\n{df.dtypes}")
    print("=" * 50 + "\n")
    return df


# ──────────────────────────────────────────
# STEP 2 — STANDARDIZE COLUMN NAMES
# ──────────────────────────────────────────
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns to lowercase snake_case."""
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[\s\-/]+", "_", regex=True)
        .str.replace(r"[^\w]", "", regex=True)
    )
    print("[✓] Column names standardized to snake_case")
    return df


# ──────────────────────────────────────────
# STEP 3 — REMOVE DUPLICATES
# ──────────────────────────────────────────
def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Drop exact duplicate rows."""
    before = len(df)
    df = df.drop_duplicates()
    dropped = before - len(df)
    print(f"[✓] Duplicates removed: {dropped} rows dropped")
    return df


# ──────────────────────────────────────────
# STEP 4 — HANDLE MISSING VALUES
# ──────────────────────────────────────────
def handle_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Drop rows where required columns are null
    - Fill numeric nulls with median
    - Fill text nulls with 'Unknown'
    """
    # Drop rows missing required fields
    before = len(df)
    required = [c for c in REQUIRED_COLS if c in df.columns]
    df = df.dropna(subset=required)
    print(f"[✓] Rows dropped (missing required fields): {before - len(df)}")

    # Fill numeric columns with median
    num_cols = [c for c in NUMERIC_COLS if c in df.columns]
    for col in num_cols:
        median_val = df[col].median()
        nulls = df[col].isnull().sum()
        df[col] = df[col].fillna(median_val)
        if nulls:
            print(f"[✓] '{col}' — filled {nulls} nulls with median ({median_val:.2f})")

    # Fill text columns with 'Unknown'
    text_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in text_cols:
        nulls = df[col].isnull().sum()
        df[col] = df[col].fillna("Unknown")
        if nulls:
            print(f"[✓] '{col}' — filled {nulls} nulls with 'Unknown'")

    return df


# ──────────────────────────────────────────
# STEP 5 — FIX DATA TYPES
# ──────────────────────────────────────────
def fix_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convert columns to correct types."""
    # Numeric columns
    num_cols = [c for c in NUMERIC_COLS if c in df.columns]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        print(f"[✓] '{col}' converted to numeric")

    # Date columns
    date_cols = [c for c in DATE_COLS if c in df.columns]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
        print(f"[✓] '{col}' converted to datetime")

    return df


# ──────────────────────────────────────────
# STEP 6 — STANDARDIZE TEXT VALUES
# ──────────────────────────────────────────
def standardize_text(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace and fix casing on string columns."""
    text_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in text_cols:
        df[col] = df[col].str.strip().str.title()
    print(f"[✓] Text columns standardized (strip + title case): {list(text_cols)}")
    return df


# ──────────────────────────────────────────
# STEP 7 — REMOVE OUTLIERS (IQR method)
# ──────────────────────────────────────────
def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Cap extreme values in numeric columns using IQR."""
    num_cols = [c for c in NUMERIC_COLS if c in df.columns]
    for col in num_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = ((df[col] < lower) | (df[col] > upper)).sum()
        df[col] = df[col].clip(lower=lower, upper=upper)
        if outliers:
            print(f"[✓] '{col}' — {outliers} outliers capped (IQR method)")
    return df


# ──────────────────────────────────────────
# STEP 8 — FINAL REPORT & SAVE
# ──────────────────────────────────────────
def save_and_report(df: pd.DataFrame, filepath: str):
    """Print final profile and save clean CSV."""
    print("\n" + "=" * 50)
    print("DATA PROFILE — AFTER CLEANING")
    print("=" * 50)
    print(f"Shape          : {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"Remaining nulls:\n{df.isnull().sum()}")
    print("=" * 50)

    df.to_csv(filepath, index=False)
    print(f"\n[✓] Clean data saved to '{filepath}'\n")


# ──────────────────────────────────────────
# DEMO DATA GENERATOR
# ──────────────────────────────────────────
def generate_demo_data() -> pd.DataFrame:
    """Create a small messy demo dataset for testing."""
    data = {
        "ID":          [1, 2, 2, 3, 4, 5, 6, None, 8],
        "Name":        ["alice", "BOB", "BOB", "  Charlie ", "diana", None, "eve", "frank", "Grace"],
        "Age":         [25, 999, 999, 30, None, 22, 28, 35, 29],
        "Salary":      [50000, 60000, 60000, None, 75000, 48000, 52000, 200000, 58000],
        "Score":       [88, 72, 72, 95, 60, None, 77, 85, 91],
        "Date Joined": ["01/01/2023", "2023-02-15", "2023-02-15", "15-03-2023",
                        "2023/04/20", "May 5 2023", "2023-06-10", "2023-07-01", "2023-08-22"],
        "Department":  ["HR", "IT", "IT", "Finance", "hr", "IT", None, "Finance", "HR"],
    }
    return pd.DataFrame(data)


# ──────────────────────────────────────────
# MAIN PIPELINE
# ──────────────────────────────────────────
def run_pipeline():
    df = load_and_profile(INPUT_FILE)
    df = clean_column_names(df)
    df = remove_duplicates(df)
    df = fix_data_types(df)
    df = handle_nulls(df)
    df = standardize_text(df)
    df = remove_outliers(df)
    save_and_report(df, OUTPUT_FILE)


if __name__ == "__main__":
    run_pipeline()