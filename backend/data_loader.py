from pathlib import Path
from typing import Dict, List

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw_data"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
PROCESSED_FILE = PROCESSED_DATA_DIR / "deals_master.csv"


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


def load_accounts() -> pd.DataFrame:
    df = pd.read_csv(RAW_DATA_DIR / "accounts.csv")
    return clean_columns(df)


def load_products() -> pd.DataFrame:
    df = pd.read_csv(RAW_DATA_DIR / "products.csv")
    return clean_columns(df)


def load_sales_pipeline() -> pd.DataFrame:
    df = pd.read_csv(RAW_DATA_DIR / "sales_pipeline.csv")
    return clean_columns(df)


def load_sales_teams() -> pd.DataFrame:
    df = pd.read_csv(RAW_DATA_DIR / "sales_teams.csv")
    return clean_columns(df)


def _safe_merge(left: pd.DataFrame, right: pd.DataFrame, left_key: str, right_key: str, suffix: str) -> pd.DataFrame:
    """
    Merge only if both keys exist.
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
    accounts = load_accounts()
    products = load_products()
    pipeline = load_sales_pipeline()
    teams = load_sales_teams()

    df = pipeline.copy()

    # Common joins for this Kaggle CRM dataset
    # sales_pipeline.account -> accounts.account
    df = _safe_merge(df, accounts, "account", "account", "_account")

    # sales_pipeline.product -> products.product
    df = _safe_merge(df, products, "product", "product", "_product")

    # sales_pipeline.sales_agent -> sales_teams.sales_agent
    df = _safe_merge(df, teams, "sales_agent", "sales_agent", "_team")

    # Remove duplicate join columns if present
    duplicate_cols = [col for col in df.columns if col.endswith("_account") or col.endswith("_product") or col.endswith("_team")]
    # keep them for now; useful during debugging
    # comment below line if you want to inspect all merged columns
    # df = df.drop(columns=duplicate_cols, errors="ignore")

    return df


def save_master_dataframe() -> pd.DataFrame:
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df = build_master_dataframe()
    df.to_csv(PROCESSED_FILE, index=False)
    return df


def load_master_dataframe() -> pd.DataFrame:
    if PROCESSED_FILE.exists():
        df = pd.read_csv(PROCESSED_FILE)
        return clean_columns(df)

    return save_master_dataframe()


def get_client_records(client_name: str) -> pd.DataFrame:
    df = load_master_dataframe()

    if "account" not in df.columns:
        return pd.DataFrame()

    filtered = df[df["account"].astype(str).str.lower() == client_name.strip().lower()]
    return filtered


def get_latest_client_record(client_name: str) -> Dict:
    df = get_client_records(client_name)

    if df.empty:
        return {}

    date_candidates: List[str] = ["close_date", "engage_date", "created_date"]
    date_col = next((c for c in date_candidates if c in df.columns), None)

    if date_col:
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.sort_values(by=date_col, ascending=False, na_position="last")

    return df.iloc[0].to_dict()


def get_client_profile(client_name: str) -> Dict:
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