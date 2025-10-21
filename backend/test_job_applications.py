import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))

with engine.connect() as conn:
    # Check job_applications table structure
    print("--- job_applications table structure ---")
    result = conn.execute(text("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns 
        WHERE table_name = 'job_applications'
        ORDER BY ordinal_position
    """))
    for col in result:
        print(f"  {col[0]}: {col[1]} (nullable: {col[2]})")
    
    # Check foreign key constraint
    print("\n--- Foreign Key Constraint ---")
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
        WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = 'job_applications'
    """))
    for fk in result:
        print(f"  {fk[0]}.{fk[1]} -> {fk[2]}.{fk[3]}")
