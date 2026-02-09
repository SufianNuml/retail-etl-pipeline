import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

def check_row_counts():
    print("\n🔍 Checking row counts...")

    queries = {
        "stg_retail_sales": "SELECT COUNT(*) AS cnt FROM stg_retail_sales",
        "fact_sales": "SELECT COUNT(*) AS cnt FROM fact_sales",
        "agg_daily_category_sales": "SELECT COUNT(*) AS cnt FROM agg_daily_category_sales"
    }

    for table, query in queries.items():
        df = pd.read_sql(query, engine)
        print(f"✅ {table}: {df['cnt'][0]} rows")

def check_nulls():
    print("\n🔍 Checking NULL values in fact_sales...")

    query = """
        SELECT
            COUNT(*) FILTER (WHERE transaction_id IS NULL) AS null_transaction_id,
            COUNT(*) FILTER (WHERE amount IS NULL) AS null_amount,
            COUNT(*) FILTER (WHERE transaction_date IS NULL) AS null_date
        FROM fact_sales
    """
    df = pd.read_sql(query, engine)

    if df.iloc[0].sum() == 0:
        print("✅ No critical NULL values found")
    else:
        print("❌ NULL values detected!")
        print(df)

def check_negative_amounts():
    print("\n🔍 Checking negative transaction amounts...")

    query = """
        SELECT COUNT(*) AS negative_count
        FROM fact_sales
        WHERE amount < 0
    """
    df = pd.read_sql(query, engine)

    if df["negative_count"][0] == 0:
        print("✅ No negative amounts found")
    else:
        print(f"❌ Found {df['negative_count'][0]} negative transactions")

def check_duplicates():
    print("\n🔍 Checking duplicate transactions...")

    query = """
        SELECT COUNT(*) - COUNT(DISTINCT transaction_id) AS duplicate_count
        FROM fact_sales
    """
    df = pd.read_sql(query, engine)

    if df["duplicate_count"][0] == 0:
        print("✅ No duplicate transactions found")
    else:
        print(f"❌ Found {df['duplicate_count'][0]} duplicate transactions")

def run_quality_checks():
    print("🚦 STEP 5: DATA QUALITY CHECKS STARTED")
    check_row_counts()
    check_nulls()
    check_negative_amounts()
    check_duplicates()
    print("\n🎉 DATA QUALITY CHECKS COMPLETED")

if __name__ == "__main__":
    run_quality_checks()
