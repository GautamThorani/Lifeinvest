import os
import uuid
from sqlalchemy import create_engine, text
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))

def test_constraints():
    with engine.connect() as conn:
        # Use individual transactions for each test
        test_user_id = uuid.uuid4()
        test_category_id = uuid.uuid4()
        
        # Setup: Create test user and category
        with conn.begin():
            conn.execute(text("""
                INSERT INTO users (id, email, password_hash, full_name) 
                VALUES (:id, 'test@example.com', 'hash123', 'Test User')
            """), {"id": test_user_id})
            print(" Created test user")
            
            conn.execute(text("""
                INSERT INTO investment_categories (id, user_id, name, type, color) 
                VALUES (:id, :user_id, 'Learning', 'time', '#FF5733')
            """), {"id": test_category_id, "user_id": test_user_id})
            print(" Created test category")
        
        # Test 1: Insert valid investment
        with conn.begin():
            try:
                conn.execute(text("""
                    INSERT INTO investments 
                    (id, user_id, category_id, type, title, amount_invested, currency, invested_at)
                    VALUES 
                    (:id, :user_id, :category_id, 'time', 'Learn Docker', 8.0, 'hours', :invested_at)
                """), {
                    "id": uuid.uuid4(),
                    "user_id": test_user_id,
                    "category_id": test_category_id,
                    "invested_at": datetime.now(timezone.utc)
                })
                print(" Test 1 PASSED: Valid investment inserted")
            except Exception as e:
                print(f" Test 1 FAILED: {e}")
        
        # Test 2: Try invalid type (should fail)
        try:
            with conn.begin():
                conn.execute(text("""
                    INSERT INTO investments 
                    (id, user_id, category_id, type, title, amount_invested, currency, invested_at)
                    VALUES 
                    (:id, :user_id, :category_id, 'invalid_type', 'Bad Investment', 10.0, 'USD', :invested_at)
                """), {
                    "id": uuid.uuid4(),
                    "user_id": test_user_id,
                    "category_id": test_category_id,
                    "invested_at": datetime.now(timezone.utc)
                })
                print(" Test 2 FAILED: Invalid type was accepted (should have failed)")
        except Exception as e:
            print(" Test 2 PASSED: Invalid type correctly rejected")
        
        # Test 3: Try without user_id (should fail)
        try:
            with conn.begin():
                conn.execute(text("""
                    INSERT INTO investments 
                    (id, category_id, type, title, amount_invested, currency, invested_at)
                    VALUES 
                    (:id, :category_id, 'money', 'No User', 100.0, 'USD', :invested_at)
                """), {
                    "id": uuid.uuid4(),
                    "category_id": test_category_id,
                    "invested_at": datetime.now(timezone.utc)
                })
                print(" Test 3 FAILED: Investment without user_id was accepted")
        except Exception as e:
            print(" Test 3 PASSED: Investment without user_id correctly rejected")
        
        # Show the inserted data
        with conn.begin():
            result = conn.execute(text("""
                SELECT i.title, i.type, i.amount_invested, i.currency, c.name as category
                FROM investments i
                JOIN investment_categories c ON i.category_id = c.id
                WHERE i.user_id = :user_id
            """), {"user_id": test_user_id})
            
            print("\n Inserted Investments:")
            investments = list(result)
            if investments:
                for row in investments:
                    print(f"  - {row[0]}: {row[1]} investment of {row[2]} {row[3]} in {row[4]}")
            else:
                print("  No investments found (this is expected after constraint tests)")
        
        # Cleanup
        with conn.begin():
            conn.execute(text("DELETE FROM investments WHERE user_id = :user_id"), {"user_id": test_user_id})
            conn.execute(text("DELETE FROM investment_categories WHERE user_id = :user_id"), {"user_id": test_user_id})
            conn.execute(text("DELETE FROM users WHERE id = :user_id"), {"user_id": test_user_id})
            print(" Test data cleaned up")

if __name__ == "__main__":
    test_constraints()
