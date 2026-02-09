import sys
import io

# This fix must be inside load.py because it is the one printing the emoji
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database connection details (from .env)
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

# Safety check (very important for beginners)
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("❌ Database environment variables are missing")

# Create SQLAlchemy engine
engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def load_raw_data():
    print(" STEP 2: LOAD — Raw data to PostgreSQL")

    # Path to raw CSV
    csv_path = "data/raw_retail_data.csv"

    # Read CSV
    df = pd.read_csv(csv_path)
    print(f"📄 Rows read from CSV: {len(df)}")

    # Load data into PostgreSQL (RAW layer)
    df.to_sql(
        name="raw_retail_sales",
        con=engine,
        if_exists="replace",   # overwrite for now (safe for learning)
        index=False
    )

    print("✅ Raw data loaded successfully into table: raw_retail_sales")

if __name__ == "__main__":
    load_raw_data()
