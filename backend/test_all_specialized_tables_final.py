import os
import uuid
from sqlalchemy import create_engine, text
from datetime import datetime, timezone, date
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))

def cleanup_test_data(conn, user_id):
    """Clean up test data in correct order"""
    with conn.begin():
        # Cleanup in reverse order of creation (child tables first)
        conn.execute(text("DELETE FROM time_logs WHERE investment_id IN (SELECT id FROM investments WHERE user_id = :user_id)"), {"user_id": user_id})
        conn.execute(text("DELETE FROM financial_investments WHERE investment_id IN (SELECT id FROM investments WHERE user_id = :user_id)"), {"user_id": user_id})
        conn.execute(text("DELETE FROM learning_investments WHERE investment_id IN (SELECT id FROM investments WHERE user_id = :user_id)"), {"user_id": user_id})
        conn.execute(text("DELETE FROM job_applications WHERE investment_id IN (SELECT id FROM investments WHERE user_id = :user_id)"), {"user_id": user_id})
        conn.execute(text("DELETE FROM investments WHERE user_id = :user_id"), {"user_id": user_id})
        conn.execute(text("DELETE FROM investment_categories WHERE user_id = :user_id"), {"user_id": user_id})
        conn.execute(text("DELETE FROM users WHERE id = :user_id"), {"user_id": user_id})

def test_all_tables():
    with engine.connect() as conn:
        # Create test data with unique identifiers
        test_user_id = uuid.uuid4()
        test_category_id = uuid.uuid4()
        unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        
        # First, clean up any existing test data for this user (if any)
        cleanup_test_data(conn, test_user_id)
        print("✅ Cleaned up any existing test data")
        
        with conn.begin():
            # Setup: Create user and category
            conn.execute(text("""
                INSERT INTO users (id, email, password_hash, full_name) 
                VALUES (:id, :email, 'hash123', 'Test User')
            """), {"id": test_user_id, "email": unique_email})
            
            conn.execute(text("""
                INSERT INTO investment_categories (id, user_id, name, type, color) 
                VALUES (:id, :user_id, 'Mixed Investments', 'mixed', '#33CC33')
            """), {"id": test_category_id, "user_id": test_user_id})
            
            print("✅ Setup: User and category created")
        
        # Test 1: Time Logs with granular tracking
        with conn.begin():
            time_investment_id = uuid.uuid4()
            conn.execute(text("""
                INSERT INTO investments 
                (id, user_id, category_id, type, title, amount_invested, currency, invested_at)
                VALUES 
                (:id, :user_id, :category_id, 'time', 'Project Development', 15.0, 'hours', :invested_at)
            """), {
                "id": time_investment_id,
                "user_id": test_user_id,
                "category_id": test_category_id,
                "invested_at": datetime.now(timezone.utc)
            })
            
            # Add multiple time logs for the same investment
            for i in range(3):
                conn.execute(text("""
                    INSERT INTO time_logs 
                    (id, investment_id, logged_date, time_spent_minutes, description, productivity_rating)
                    VALUES 
                    (:id, :investment_id, :logged_date, :minutes, :desc, :rating)
                """), {
                    "id": uuid.uuid4(),
                    "investment_id": time_investment_id,
                    "logged_date": date(2024, 10, 18 + i),
                    "minutes": 120 + (i * 30),
                    "desc": f"Day {i+1} of project work",
                    "rating": 7 + i
                })
            
            print("✅ Time Logs: Multiple time entries for one investment")
        
        # Test 2: Financial Investment
        with conn.begin():
            financial_investment_id = uuid.uuid4()
            conn.execute(text("""
                INSERT INTO investments 
                (id, user_id, category_id, type, title, amount_invested, currency, invested_at)
                VALUES 
                (:id, :user_id, :category_id, 'money', 'Stock Investment', 1000.00, 'USD', :invested_at)
            """), {
                "id": financial_investment_id,
                "user_id": test_user_id,
                "category_id": test_category_id,
                "invested_at": datetime.now(timezone.utc)
            })
            
            conn.execute(text("""
                INSERT INTO financial_investments 
                (id, investment_id, investment_type, asset_name, ticker_symbol, quantity, purchase_price, current_value)
                VALUES 
                (:id, :investment_id, 'stock', 'Apple Inc.', 'AAPL', 5.0000, 180.50, 185.25)
            """), {
                "id": uuid.uuid4(),
                "investment_id": financial_investment_id
            })
            
            print("✅ Financial Investment: Stock purchase recorded")
        
        # Query and display all data
        with conn.begin():
            print("\n📊 ALL SPECIALIZED INVESTMENTS:")
            
            # Time Logs
            print("\n⏰ Time Logs:")
            result = conn.execute(text("""
                SELECT i.title, COUNT(t.id) as log_count, SUM(t.time_spent_minutes) as total_minutes
                FROM investments i
                JOIN time_logs t ON i.id = t.investment_id
                WHERE i.user_id = :user_id AND i.type = 'time'
                GROUP BY i.title
            """), {"user_id": test_user_id})
            
            for row in result:
                total_hours = row[2] / 60
                print(f"  {row[0]}: {row[1]} logs, {total_hours:.1f} total hours")
            
            # Financial Investments
            print("\n💰 Financial Investments:")
            result = conn.execute(text("""
                SELECT i.title, f.asset_name, f.ticker_symbol, f.quantity, f.purchase_price, f.current_value
                FROM investments i
                JOIN financial_investments f ON i.id = f.investment_id
                WHERE i.user_id = :user_id
            """), {"user_id": test_user_id})
            
            for row in result:
                # Convert Decimal to float for calculation
                quantity = float(row[3])
                purchase_price = float(row[4]) if row[4] else 0
                current_value = float(row[5]) if row[5] else 0
                profit = (current_value - purchase_price) * quantity
                
                print(f"  {row[0]}: {row[3]} shares of {row[1]} ({row[2]})")
                print(f"    Purchase: ${purchase_price:.2f}, Current: ${current_value:.2f}, Profit: ${profit:.2f}")
            
            # All investment types count
            print("\n📈 Investment Type Summary:")
            result = conn.execute(text("""
                SELECT type, COUNT(*) as count
                FROM investments
                WHERE user_id = :user_id
                GROUP BY type
            """), {"user_id": test_user_id})
            
            for row in result:
                print(f"  {row[0]}: {row[1]} investments")
        
        # Cleanup using the proper function
        cleanup_test_data(conn, test_user_id)
        print("✅ All test data cleaned up")

if __name__ == "__main__":
    test_all_tables()
