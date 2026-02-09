import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import sys
import io

# 1. Fix Windows Emoji Encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 2. Load environment variables
load_dotenv()

# 3. Use the correct POSTGRES keys from your .env
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

# 4. Create Engine (Added check to ensure values aren't None)
if not all([DB_USER, DB_PASSWORD, DB_PORT]):
    print("❌ Error: Could not find database credentials in .env file!")
    sys.exit(1)

connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(connection_string)

# 1️⃣ Month with highest revenue growth
query_highest_growth = """
WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', transaction_date) AS month,
        SUM(amount) AS total_sales
    FROM fact_sales
    GROUP BY month
)
SELECT
    month,
    total_sales,
    LAG(total_sales) OVER (ORDER BY month) AS prev_month,
    -- Added ::numeric cast below to satisfy the ROUND function
    ROUND(((total_sales - LAG(total_sales) OVER (ORDER BY month)) / 
          NULLIF(LAG(total_sales) OVER (ORDER BY month), 0) * 100)::numeric, 2) AS growth_percent
FROM monthly_sales
ORDER BY growth_percent DESC NULLS LAST
LIMIT 1;
"""

# 2️⃣ Top 5 product categories by total sales
query_top_categories = """
SELECT
    product_category,
    SUM(amount) AS total_sales
FROM fact_sales
GROUP BY product_category
ORDER BY total_sales DESC
LIMIT 5;
"""

# 3️⃣ Average transaction value per category

query_avg_transaction = """
SELECT
    product_category,
    -- Cast the AVG result to numeric so ROUND can process it
    ROUND(AVG(amount)::numeric, 2) AS avg_transaction_value
FROM fact_sales
GROUP BY product_category
ORDER BY avg_transaction_value DESC;
"""




def run_query(query, description):
    print(f"\n📊 {description}")
    df = pd.read_sql(query, engine)
    print(df)
    # Optional: save to CSV
    df.to_csv(f"reports/{description.replace(' ', '_')}.csv", index=False)
    print(f"✅ Saved report: reports/{description.replace(' ', '_')}.csv")
    return df

# Make a reports folder if not exist
os.makedirs("reports", exist_ok=True)

# Run all queries
run_query(query_highest_growth, "Month with Highest Revenue Growth")
run_query(query_top_categories, "Top 5 Product Categories by Sales")
run_query(query_avg_transaction, "Average Transaction Value per Category")
