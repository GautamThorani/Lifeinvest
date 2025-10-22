import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))

with engine.connect() as conn:
    print("=== COMPLETE DATABASE VERIFICATION ===")
    
    # Check all tables
    result = conn.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """))
    
    tables = []
    for table in result:
        tables.append(table[0])
    
    print("📊 All Tables:")
    for table in sorted(tables):
        print(f"  ✅ {table}")
    
    expected_tables = ['users', 'investment_categories', 'investments', 'job_applications', 'learning_investments', 'time_logs', 'financial_investments']
    
    if all(table in tables for table in expected_tables):
        print(f"🎉 SUCCESS: All {len(expected_tables)} expected tables exist!")
    else:
        missing = [table for table in expected_tables if table not in tables]
        print(f"❌ MISSING: {missing}")
    
    # Check row counts (should be 0 after cleanup)
    print("\n📈 Table Row Counts (should be 0):")
    for table in sorted(tables):
        if table != 'alembic_version':
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.scalar()
            status = "✅" if count == 0 else f"❌ ({count} rows)"
            print(f"  {table}: {status}")
    
    # Check foreign keys
    print("\n🔗 Foreign Key Relationships:")
    result = conn.execute(text("""
        SELECT
            tc.table_name as child_table,
            kcu.column_name as child_column, 
            ccu.table_name as parent_table,
            ccu.column_name as parent_column
        FROM 
            information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
        ORDER BY child_table, child_column
    """))
    
    fk_count = 0
    for fk in result:
        print(f"  {fk[0]}.{fk[1]} → {fk[2]}.{fk[3]}")
        fk_count += 1
    
    print(f"\nTotal foreign key relationships: {fk_count}")
    
    # Final status
    if all(table in tables for table in expected_tables):
        print("\n🎊 DAY 3 COMPLETED SUCCESSFULLY! 🎊")
        print("All specialized investment tables are ready!")
    else:
        print("\n⚠️  Some issues need to be resolved")
