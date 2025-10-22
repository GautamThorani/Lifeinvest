import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))

print("🏥 DATABASE HEALTH CHECK")
print("=" * 50)

with engine.connect() as conn:
    # Check table counts
    result = conn.execute(text("""
        SELECT table_name, 
               (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as column_count
        FROM information_schema.tables t
        WHERE table_schema = 'public' AND table_name != 'alembic_version'
        ORDER BY table_name
    """))
    
    print("\n📋 TABLE OVERVIEW:")
    total_tables = 0
    total_columns = 0
    for table in result:
        print(f"  {table[0]}: {table[1]} columns")
        total_tables += 1
        total_columns += table[1]
    
    print(f"\n📊 TOTALS: {total_tables} tables, {total_columns} columns")
    
    # Check empty tables
    print("\n🔍 EMPTY TABLES CHECK:")
    result = conn.execute(text("""
        SELECT table_name
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name != 'alembic_version'
        ORDER BY table_name
    """))
    
    all_empty = True
    for table in result:
        count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table[0]}"))
        count = count_result.scalar()
        status = "✅ EMPTY" if count == 0 else f"❌ {count} rows"
        print(f"  {table[0]}: {status}")
        if count > 0:
            all_empty = False
    
    print(f"\n🎯 HEALTH STATUS: {'✅ EXCELLENT' if all_empty else '⚠️  NEEDS CLEANUP'}")
    print("💡 Database is ready for Day 4 development!")
