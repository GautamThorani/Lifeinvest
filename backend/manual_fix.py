import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))

with engine.connect() as conn:
    # Drop the old investments table if it exists
    conn.execute(text("DROP TABLE IF EXISTS investments CASCADE"))
    conn.commit()
    print("Dropped old investments table")
    
    # Create the correct investments table
    conn.execute(text("""
        CREATE TABLE investments (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID NOT NULL,
            category_id UUID NOT NULL,
            type VARCHAR(20) NOT NULL CHECK (type IN ('money', 'time', 'energy')),
            title VARCHAR(200) NOT NULL,
            description TEXT,
            amount_invested NUMERIC(10,2) NOT NULL,
            currency VARCHAR(10),
            invested_at TIMESTAMPTZ NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (category_id) REFERENCES investment_categories(id)
        )
    """))
    
    # Create index
    conn.execute(text("""
        CREATE INDEX ix_investments_user_date ON investments (user_id, invested_at)
    """))
    
    conn.commit()
    print("Created correct investments table with foreign keys")
