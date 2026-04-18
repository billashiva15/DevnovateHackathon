from backend.data_loader import save_master_dataframe


if __name__ == "__main__":
    df = save_master_dataframe()
    print("deals_master.csv created successfully")
    print("Rows:", len(df))
    print("Columns:", list(df.columns))