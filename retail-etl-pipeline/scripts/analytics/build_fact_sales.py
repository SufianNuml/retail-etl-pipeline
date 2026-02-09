import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

def build_fact_sales():
    print("🔥 Building fact_sales")

    query = """
        SELECT DISTINCT
            s.transaction_id,
            s.transaction_date,
            s.amount,
            c.email AS customer_email,
            p.product_category
        FROM stg_retail_sales s
        JOIN dim_customer c ON s.email = c.email
        JOIN dim_product_category p ON s.product_category = p.product_category
    """

    df = pd.read_sql(query, engine)
    df["load_date"] = pd.Timestamp.now()

    df.to_sql("fact_sales", engine, if_exists="replace", index=False)
    print(f"✅ fact_sales rows: {len(df)}")


if __name__ == "__main__":
    build_fact_sales()
