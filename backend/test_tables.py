import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))

with engine.connect() as conn:
    # Check if users table exists
    result = conn.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name IN ('users', 'investment_categories')
    """))
    
    tables = [row[0] for row in result]
    print("Tables found in database:", tables)
    
    # Check table structures
    for table in tables:
        print(f"\n--- {table} table structure ---")
        result = conn.execute(text(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{table}'
            ORDER BY ordinal_position
        """))
        for col in result:
            print(f"  {col[0]}: {col[1]}")
