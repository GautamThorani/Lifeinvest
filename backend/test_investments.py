import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))

with engine.connect() as conn:
    # Check investments table structure
    print("--- investments table structure ---")
    result = conn.execute(text("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns 
        WHERE table_name = 'investments'
        ORDER BY ordinal_position
    """))
    for col in result:
        print(f"  {col[0]}: {col[1]} (nullable: {col[2]})")
    
    # Check foreign key constraints
    print("\n--- Foreign Key Constraints ---")
    result = conn.execute(text("""
        SELECT
            tc.table_name, 
            kcu.column_name, 
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name 
        FROM 
            information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = 'investments'
    """))
    for fk in result:
        print(f"  {fk[0]}.{fk[1]} -> {fk[2]}.{fk[3]}")
    
    # Check check constraint
    print("\n--- Check Constraints ---")
    result = conn.execute(text("""
        SELECT constraint_name, check_clause 
        FROM information_schema.check_constraints 
        WHERE constraint_name = 'check_investment_type'
    """))
    for check in result:
        print(f"  {check[0]}: {check[1]}")
