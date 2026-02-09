import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

def build_daily_category_sales():
    print("📊 Building agg_daily_category_sales")

    query = """
        SELECT
            transaction_date,
            product_category,
            SUM(amount) AS total_sales,
            COUNT(*) AS total_transactions,
            ROUND(AVG(amount)::numeric, 2) AS avg_transaction_value
        FROM fact_sales
        GROUP BY transaction_date, product_category
        ORDER BY transaction_date
    """

    df = pd.read_sql(query, engine)
    df.to_sql(
        "agg_daily_category_sales",
        engine,
        if_exists="replace",
        index=False
    )

    print(f"✅ agg_daily_category_sales rows: {len(df)}")


if __name__ == "__main__":
    build_daily_category_sales()
