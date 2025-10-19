import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

try:
    engine = create_engine(os.getenv('DATABASE_URL'))
    conn = engine.connect()
    
    result = conn.execute(text("SELECT version();"))
    db_version = result.fetchone()
    
    print('Database connection successful!')
    print(f'PostgreSQL version: {db_version[0]}')
    
    conn.close()
    
except Exception as e:
    print(f'Connection failed: {e}')
