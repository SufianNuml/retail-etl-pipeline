import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# DB credentials
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def transform_data():
    print("🚀 STEP 3: TRANSFORM — Cleaning raw data")

    # Read raw table
    df = pd.read_sql("SELECT * FROM raw_retail_sales", engine)
    print(f"📄 Raw rows: {len(df)}")

    # Remove duplicates
    df = df.drop_duplicates(subset=["transaction_id"])

    # Fix product_category
    df["product_category"] = df["product_category"].replace("Unknown", "Other")

    # Remove invalid amounts
    df = df[df["amount"] > 0]

    # Convert transaction_date to date
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])

    print(f"✅ Clean rows after transform: {len(df)}")

    # Save clean data to new table
    df.to_sql(
        name="stg_retail_sales",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("🎉 TRANSFORM complete → data saved to stg_retail_sales")

if __name__ == "__main__":
    transform_data()
