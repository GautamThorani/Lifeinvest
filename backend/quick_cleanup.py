import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))

print("🧹 QUICK CLEANUP")
print("=" * 30)

with engine.connect() as conn:
    with conn.begin():
        # Clean all data (in correct order)
        tables = [
            'time_logs',
            'financial_investments', 
            'learning_investments',
            'job_applications',
            'investments',
            'investment_categories',
            'users'
        ]
        
        for table in tables:
            try:
                conn.execute(text(f"DELETE FROM {table}"))
                print(f"✅ Cleared {table}")
            except Exception as e:
                print(f"⚠️  Could not clear {table}: {e}")
        
        print("\n🎉 Database is now clean and ready!")

# Final check
print("\n🔍 FINAL CHECK:")
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT table_name, 
               (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as column_count,
               (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public') as table_count
        FROM information_schema.tables t
        WHERE table_schema = 'public' AND table_name != 'alembic_version'
        ORDER BY table_name
    """))
    
    print("📊 CLEAN DATABASE STATE:")
    total_tables = 0
    for table in result:
        count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table[0]}"))
        count = count_result.scalar()
        status = "✅ EMPTY" if count == 0 else f"❌ {count} rows"
        print(f"  {table[0]}: {table[1]} columns - {status}")
        total_tables += 1
    
    print(f"\n🎯 FINAL STATUS: {total_tables} tables ready for development!")
