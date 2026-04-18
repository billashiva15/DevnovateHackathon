# from pathlib import Path
# from typing import Dict, List

# import pandas as pd

# BASE_DIR = Path(__file__).resolve().parent.parent
# RAW_DATA_DIR = BASE_DIR / "data" / "raw_data"
# PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
# PROCESSED_FILE = PROCESSED_DATA_DIR / "deals_master.csv"


# def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
#     df = df.copy()
#     df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
#     return df


# def load_accounts() -> pd.DataFrame:
#     df = pd.read_csv(RAW_DATA_DIR / "accounts.csv")
#     return clean_columns(df)


# def load_products() -> pd.DataFrame:
#     df = pd.read_csv(RAW_DATA_DIR / "products.csv")
#     return clean_columns(df)


# def load_sales_pipeline() -> pd.DataFrame:
#     df = pd.read_csv(RAW_DATA_DIR / "sales_pipeline.csv")
#     return clean_columns(df)


# def load_sales_teams() -> pd.DataFrame:
#     df = pd.read_csv(RAW_DATA_DIR / "sales_teams.csv")
#     return clean_columns(df)


# def _safe_merge(left: pd.DataFrame, right: pd.DataFrame, left_key: str, right_key: str, suffix: str) -> pd.DataFrame:
#     """
#     Merge only if both keys exist.
#     """
#     if left_key in left.columns and right_key in right.columns:
#         return left.merge(
#             right,
#             left_on=left_key,
#             right_on=right_key,
#             how="left",
#             suffixes=("", suffix),
#         )
#     return left


# def build_master_dataframe() -> pd.DataFrame:
#     accounts = load_accounts()
#     products = load_products()
#     pipeline = load_sales_pipeline()
#     teams = load_sales_teams()

#     df = pipeline.copy()

#     # Common joins for this Kaggle CRM dataset
#     # sales_pipeline.account -> accounts.account
#     df = _safe_merge(df, accounts, "account", "account", "_account")

#     # sales_pipeline.product -> products.product
#     df = _safe_merge(df, products, "product", "product", "_product")

#     # sales_pipeline.sales_agent -> sales_teams.sales_agent
#     df = _safe_merge(df, teams, "sales_agent", "sales_agent", "_team")

#     # Remove duplicate join columns if present
#     duplicate_cols = [col for col in df.columns if col.endswith("_account") or col.endswith("_product") or col.endswith("_team")]
#     # keep them for now; useful during debugging
#     # comment below line if you want to inspect all merged columns
#     # df = df.drop(columns=duplicate_cols, errors="ignore")

#     return df


# def save_master_dataframe() -> pd.DataFrame:
#     PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
#     df = build_master_dataframe()
#     df.to_csv(PROCESSED_FILE, index=False)
#     return df


# def load_master_dataframe() -> pd.DataFrame:
#     if PROCESSED_FILE.exists():
#         df = pd.read_csv(PROCESSED_FILE)
#         return clean_columns(df)

#     return save_master_dataframe()


# def get_client_records(client_name: str) -> pd.DataFrame:
#     df = load_master_dataframe()

#     if "account" not in df.columns:
#         return pd.DataFrame()

#     filtered = df[df["account"].astype(str).str.lower() == client_name.strip().lower()]
#     return filtered


# def get_latest_client_record(client_name: str) -> Dict:
#     df = get_client_records(client_name)

#     if df.empty:
#         return {}

#     date_candidates: List[str] = ["close_date", "engage_date", "created_date"]
#     date_col = next((c for c in date_candidates if c in df.columns), None)

#     if date_col:
#         df = df.copy()
#         df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
#         df = df.sort_values(by=date_col, ascending=False, na_position="last")

#     return df.iloc[0].to_dict()


# def get_client_profile(client_name: str) -> Dict:
#     record = get_latest_client_record(client_name)
#     if not record:
#         return {}

#     return {
#         "account": record.get("account", "Unknown"),
#         "sector": record.get("sector", "Unknown"),
#         "office_location": record.get("office_location", "Unknown"),
#         "revenue": record.get("revenue", "Unknown"),
#         "employees": record.get("employees", "Unknown"),
#     }

"""
backend/data_loader.py

Purpose:
    This module is responsible for loading, cleaning, merging, saving,
    and retrieving deal-related business data for the DealMind-AI project.

What this file does:
    1. Defines file paths for raw and processed data
    2. Loads multiple CSV files from the CRM dataset
    3. Standardizes column names for consistency
    4. Merges all source datasets into one master dataframe
    5. Saves the merged dataset into the processed folder
    6. Reloads processed data when available
    7. Retrieves account-specific records
    8. Extracts the latest client profile information

Why this matters:
    The AI sales agent needs structured deal context before it can make
    intelligent decisions. This file acts as the data foundation layer
    for the whole project.
"""

from pathlib import Path
from typing import Dict, List

import pandas as pd


# -------------------------------------------------------------------
# Project Paths
# -------------------------------------------------------------------
# BASE_DIR points to the root folder of the project.
# Example:
#   project/
#       backend/
#       data/
#       frontend/
#
# If this file is inside backend/, then parent.parent reaches project root.
BASE_DIR = Path(__file__).resolve().parent.parent

# Folder containing raw CSV files
RAW_DATA_DIR = BASE_DIR / "data" / "raw_data"

# Folder where processed files will be stored
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

# Final merged master dataset file
PROCESSED_FILE = PROCESSED_DATA_DIR / "deals_master.csv"


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize dataframe column names.

    Args:
        df (pd.DataFrame): Input dataframe whose columns need cleaning.

    Returns:
        pd.DataFrame: A copy of the dataframe with cleaned column names.

    Cleaning rules:
        - Remove leading and trailing spaces
        - Convert all names to lowercase
        - Replace spaces with underscores

    Example:
        "Sales Agent" -> "sales_agent"
        " Office Location " -> "office_location"

    Why this is useful:
        CSV files from different sources often contain inconsistent naming.
        Standardized column names make merging and querying much easier.
    """
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


def load_accounts() -> pd.DataFrame:
    """
    Load the accounts dataset.

    Returns:
        pd.DataFrame: Cleaned accounts dataframe.

    Expected file:
        data/raw_data/accounts.csv
    """
    df = pd.read_csv(RAW_DATA_DIR / "accounts.csv")
    return clean_columns(df)


def load_products() -> pd.DataFrame:
    """
    Load the products dataset.

    Returns:
        pd.DataFrame: Cleaned products dataframe.

    Expected file:
        data/raw_data/products.csv
    """
    df = pd.read_csv(RAW_DATA_DIR / "products.csv")
    return clean_columns(df)


def load_sales_pipeline() -> pd.DataFrame:
    """
    Load the sales pipeline dataset.

    Returns:
        pd.DataFrame: Cleaned sales pipeline dataframe.

    Expected file:
        data/raw_data/sales_pipeline.csv

    Why it matters:
        This is usually the core transactional dataset containing
        account, product, sales stage, deal value, and agent information.
    """
    df = pd.read_csv(RAW_DATA_DIR / "sales_pipeline.csv")
    return clean_columns(df)


def load_sales_teams() -> pd.DataFrame:
    """
    Load the sales teams dataset.

    Returns:
        pd.DataFrame: Cleaned sales teams dataframe.

    Expected file:
        data/raw_data/sales_teams.csv
    """
    df = pd.read_csv(RAW_DATA_DIR / "sales_teams.csv")
    return clean_columns(df)


def _safe_merge(
    left: pd.DataFrame,
    right: pd.DataFrame,
    left_key: str,
    right_key: str,
    suffix: str
) -> pd.DataFrame:
    """
    Safely merge two dataframes only if both join keys exist.

    Args:
        left (pd.DataFrame): Left dataframe.
        right (pd.DataFrame): Right dataframe.
        left_key (str): Join column name in the left dataframe.
        right_key (str): Join column name in the right dataframe.
        suffix (str): Suffix to apply to overlapping column names.

    Returns:
        pd.DataFrame: Merged dataframe if keys exist, otherwise the original left dataframe.

    Why this function exists:
        During development or dataset changes, some files may not contain
        the expected columns. This function prevents the program from crashing
        and makes the merge step more robust.

    Example:
        Merge pipeline.account with accounts.account
    """
    if left_key in left.columns and right_key in right.columns:
        return left.merge(
            right,
            left_on=left_key,
            right_on=right_key,
            how="left",
            suffixes=("", suffix),
        )

    return left


def build_master_dataframe() -> pd.DataFrame:
    """
    Build the full master dataframe by merging all source datasets.

    Returns:
        pd.DataFrame: A combined dataframe containing deal, account,
        product, and sales team information.

    Merge flow:
        1. Start with sales_pipeline as the base dataframe
        2. Merge accounts on account
        3. Merge products on product
        4. Merge sales_teams on sales_agent

    Why this matters:
        The agent should not rely on scattered data files.
        A single master dataframe makes downstream querying much easier.

    Notes:
        Duplicate columns created during merge are preserved for debugging.
        You can drop them later if needed.
    """
    accounts = load_accounts()
    products = load_products()
    pipeline = load_sales_pipeline()
    teams = load_sales_teams()

    # Start from the main sales pipeline table
    df = pipeline.copy()

    # ------------------------------------------------------------
    # Common joins for the CRM dataset
    # ------------------------------------------------------------

    # Merge account-related information
    # sales_pipeline.account -> accounts.account
    df = _safe_merge(df, accounts, "account", "account", "_account")

    # Merge product-related information
    # sales_pipeline.product -> products.product
    df = _safe_merge(df, products, "product", "product", "_product")

    # Merge sales-agent / team-related information
    # sales_pipeline.sales_agent -> sales_teams.sales_agent
    df = _safe_merge(df, teams, "sales_agent", "sales_agent", "_team")

    # ------------------------------------------------------------
    # Detect duplicate columns created by joins
    # ------------------------------------------------------------
    duplicate_cols = [
        col
        for col in df.columns
        if col.endswith("_account") or col.endswith("_product") or col.endswith("_team")
    ]

    # Keeping duplicate columns for now is helpful during debugging,
    # because it allows us to inspect what came from each merge source.
    #
    # If needed later, uncomment the following line:
    # df = df.drop(columns=duplicate_cols, errors="ignore")

    return df


def save_master_dataframe() -> pd.DataFrame:
    """
    Build and save the merged master dataframe to disk.

    Returns:
        pd.DataFrame: The saved master dataframe.

    Process:
        1. Create processed directory if it does not exist
        2. Build the master dataframe
        3. Save it as deals_master.csv

    Why this matters:
        Instead of merging raw files every time, the project can reuse
        the already processed master file for faster access.
    """
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    df = build_master_dataframe()
    df.to_csv(PROCESSED_FILE, index=False)

    return df


def load_master_dataframe() -> pd.DataFrame:
    """
    Load the processed master dataframe if it already exists.
    Otherwise, generate and save it first.

    Returns:
        pd.DataFrame: Cleaned master dataframe.

    Logic:
        - If deals_master.csv exists, read it directly
        - Otherwise, create it using save_master_dataframe()

    Why this is useful:
        This function makes the workflow efficient and automatic.
        The user does not need to manually rebuild the dataset every time.
    """
    if PROCESSED_FILE.exists():
        df = pd.read_csv(PROCESSED_FILE)
        return clean_columns(df)

    return save_master_dataframe()


def get_client_records(client_name: str) -> pd.DataFrame:
    """
    Retrieve all records related to a specific client/account.

    Args:
        client_name (str): Name of the client account to search for.

    Returns:
        pd.DataFrame: Filtered dataframe containing all matching records.

    Matching behavior:
        - Case insensitive
        - Ignores extra surrounding spaces

    Example:
        Input: "Acme Corp"
        Output: All rows where account == "Acme Corp"
    """
    df = load_master_dataframe()

    # If account column is missing, return empty dataframe safely
    if "account" not in df.columns:
        return pd.DataFrame()

    filtered = df[df["account"].astype(str).str.lower() == client_name.strip().lower()]
    return filtered


def get_latest_client_record(client_name: str) -> Dict:
    """
    Retrieve the most recent record for a given client.

    Args:
        client_name (str): Name of the client account.

    Returns:
        Dict: Latest client record as a dictionary.
              Returns empty dictionary if no records are found.

    Date priority:
        The function looks for one of these date columns:
            - close_date
            - engage_date
            - created_date

        It uses the first available one to sort records in descending order.

    Why this matters:
        In a CRM setting, one client may have multiple interactions or deals.
        Usually the most recent one is the most relevant for decision making.
    """
    df = get_client_records(client_name)

    if df.empty:
        return {}

    # Possible date columns ranked by priority
    date_candidates: List[str] = ["close_date", "engage_date", "created_date"]

    # Select the first date column that exists in the dataframe
    date_col = next((c for c in date_candidates if c in df.columns), None)

    if date_col:
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.sort_values(by=date_col, ascending=False, na_position="last")

    return df.iloc[0].to_dict()


def get_client_profile(client_name: str) -> Dict:
    """
    Extract a simplified client profile from the latest client record.

    Args:
        client_name (str): Name of the client account.

    Returns:
        Dict: Client profile containing only the most important fields:
            - account
            - sector
            - office_location
            - revenue
            - employees

    Why this matters:
        The agent does not always need the full CRM row.
        A concise profile is enough for prompt construction and personalization.
    """
    record = get_latest_client_record(client_name)

    if not record:
        return {}

    return {
        "account": record.get("account", "Unknown"),
        "sector": record.get("sector", "Unknown"),
        "office_location": record.get("office_location", "Unknown"),
        "revenue": record.get("revenue", "Unknown"),
        "employees": record.get("employees", "Unknown"),
    }