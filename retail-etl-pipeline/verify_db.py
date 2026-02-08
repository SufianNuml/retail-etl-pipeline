from sqlalchemy import create_engine, text  # <-- add text

# Database connection string
engine = create_engine('postgresql://postgres:1235@localhost:5432/etl_project')

try:
    # Connect and test
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))  # <-- wrap with text()
        for row in result:
            print("✅ PostgreSQL is working! Version info:", row[0])
except Exception as e:
    print("❌ Connection failed:", e)
