import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

def build_dim_customer():
    print("🔹 Building dim_customer")

    query = """
        SELECT DISTINCT
            customer_name,
            email
        FROM stg_retail_sales
    """

    df = pd.read_sql(query, engine)

    df["email_domain"] = df["email"].str.split("@").str[1]
    df["created_at"] = pd.Timestamp.now()

    df.to_sql("dim_customer", engine, if_exists="replace", index=False)
    print(f"✅ dim_customer rows: {len(df)}")


def build_dim_product_category():
    print("🔹 Building dim_product_category")

    query = """
        SELECT DISTINCT
            product_category
        FROM stg_retail_sales
    """

    df = pd.read_sql(query, engine)
    df["is_unknown"] = df["product_category"].str.lower() == "unknown"

    df.to_sql("dim_product_category", engine, if_exists="replace", index=False)
    print(f"✅ dim_product_category rows: {len(df)}")


if __name__ == "__main__":
    build_dim_customer()
    build_dim_product_category()
