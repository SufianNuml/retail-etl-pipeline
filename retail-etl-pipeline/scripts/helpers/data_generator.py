import pandas as pd
from faker import Faker
import random
import os

fake = Faker()
ROWS = 100_000
DUPLICATES = 5_000

def generate_messy_data():
    print(f"🚀 Starting generation of {ROWS} messy records...")

    data = {
        "transaction_id": list(range(1, ROWS + 1)),
        "customer_name": [fake.name() for _ in range(ROWS)],
        # 15% null emails
        "email": [fake.email() if random.random() > 0.15 else None for _ in range(ROWS)],
        # Messy amounts: negatives + strings
        "amount": [
            random.choice([
                round(random.uniform(-100, 5000), 2),
                str(round(random.uniform(10, 500), 2))
            ])
            for _ in range(ROWS)
        ],
        "transaction_date": [fake.date_this_year() for _ in range(ROWS)],
        "product_category": random.choices(
            ["Electronics", "Clothing", "Home", "Toys", "Unknown"],
            k=ROWS
        )
    }

    df = pd.DataFrame(data)

    # Add duplicates
    duplicates = df.sample(DUPLICATES, random_state=42)
    df = pd.concat([df, duplicates], ignore_index=True)

    # Ensure directory exists
    os.makedirs("data/raw", exist_ok=True)

    output_path = "data/raw/raw_retail_data.csv"
    df.to_csv(output_path, index=False)

    print(f"✅ Success! Generated {len(df)} rows at: {output_path}")

if __name__ == "__main__":
    generate_messy_data()
