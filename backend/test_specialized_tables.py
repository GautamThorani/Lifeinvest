import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))

with engine.connect() as conn:
    # Check all tables in database
    print("=== All Tables in Database ===")
    result = conn.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """))
    for table in result:
        print(f"  - {table[0]}")
    
    print("\n=== Learning Investments Table ===")
    result = conn.execute(text("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns 
        WHERE table_name = 'learning_investments'
        ORDER BY ordinal_position
    """))
    for col in result:
        print(f"  {col[0]}: {col[1]} (nullable: {col[2]})")
    
    print("\n=== Job Applications Table ===")
    result = conn.execute(text("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns 
        WHERE table_name = 'job_applications'
        ORDER BY ordinal_position
    """))
    for col in result:
        print(f"  {col[0]}: {col[1]} (nullable: {col[2]})")
