import os
import uuid
from sqlalchemy import create_engine, text
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))

def test_full_chain():
    with engine.connect() as conn:
        # Create test data
        test_user_id = uuid.uuid4()
        test_category_id = uuid.uuid4()
        test_investment_id = uuid.uuid4()
        test_job_app_id = uuid.uuid4()
        test_learning_id = uuid.uuid4()
        
        with conn.begin():
            # 1. Create user
            conn.execute(text("""
                INSERT INTO users (id, email, password_hash, full_name) 
                VALUES (:id, 'test@example.com', 'hash123', 'Test User')
            """), {"id": test_user_id})
            print("1. Created test user")
            
            # 2. Create category
            conn.execute(text("""
                INSERT INTO investment_categories (id, user_id, name, type, color) 
                VALUES (:id, :user_id, 'Career Development', 'time', '#3366FF')
            """), {"id": test_category_id, "user_id": test_user_id})
            print("2. Created test category")
            
            # 3. Create investment
            conn.execute(text("""
                INSERT INTO investments 
                (id, user_id, category_id, type, title, amount_invested, currency, invested_at)
                VALUES 
                (:id, :user_id, :category_id, 'time', 'Job Application Prep', 10.0, 'hours', :invested_at)
            """), {
                "id": test_investment_id,
                "user_id": test_user_id,
                "category_id": test_category_id,
                "invested_at": datetime.now(timezone.utc)
            })
            print("3. Created investment")
            
            # 4. Create job application linked to investment
            conn.execute(text("""
                INSERT INTO job_applications 
                (id, investment_id, company_name, position, application_stage, applied_at)
                VALUES 
                (:id, :investment_id, 'Canonical', 'Software Engineer', 'applied', :applied_at)
            """), {
                "id": test_job_app_id,
                "investment_id": test_investment_id,
                "applied_at": datetime.now(timezone.utc)
            })
            print("4. Created job application linked to investment")
            
            # 5. Create another investment for learning
            learning_investment_id = uuid.uuid4()
            conn.execute(text("""
                INSERT INTO investments 
                (id, user_id, category_id, type, title, amount_invested, currency, invested_at)
                VALUES 
                (:id, :user_id, :category_id, 'time', 'Learn FastAPI', 20.0, 'hours', :invested_at)
            """), {
                "id": learning_investment_id,
                "user_id": test_user_id,
                "category_id": test_category_id,
                "invested_at": datetime.now(timezone.utc)
            })
            
            # 6. Create learning investment linked to investment
            conn.execute(text("""
                INSERT INTO learning_investments 
                (id, investment_id, platform, course_name, skills_learned, completion_percentage)
                VALUES 
                (:id, :investment_id, 'YouTube', 'FastAPI Tutorial', ARRAY['python', 'fastapi', 'api'], 85.5)
            """), {
                "id": test_learning_id,
                "investment_id": learning_investment_id
            })
            print("5. Created learning investment with skills array")
        
        # Query the data to verify relationships
        with conn.begin():
            print("\n Query Results:")
            
            # Get job applications with investment info
            result = conn.execute(text("""
                SELECT j.company_name, j.position, i.title, i.amount_invested
                FROM job_applications j
                JOIN investments i ON j.investment_id = i.id
                WHERE j.id = :job_id
            """), {"job_id": test_job_app_id})
            
            for row in result:
                print(f"  Job: {row[0]} - {row[1]}")
                print(f"    Investment: {row[2]} ({row[3]} hours)")
            
            # Get learning investments with skills
            result = conn.execute(text("""
                SELECT l.course_name, l.platform, l.skills_learned, l.completion_percentage
                FROM learning_investments l
                JOIN investments i ON l.investment_id = i.id
                WHERE l.id = :learning_id
            """), {"learning_id": test_learning_id})
            
            for row in result:
                print(f"  Learning: {row[0]} on {row[1]}")
                print(f"    Skills: {row[2]}")
                print(f"    Completion: {row[3]}%")
        
        # Cleanup
        with conn.begin():
            conn.execute(text("DELETE FROM job_applications WHERE id = :id"), {"id": test_job_app_id})
            conn.execute(text("DELETE FROM learning_investments WHERE id = :id"), {"id": test_learning_id})
            conn.execute(text("DELETE FROM investments WHERE user_id = :user_id"), {"user_id": test_user_id})
            conn.execute(text("DELETE FROM investment_categories WHERE user_id = :user_id"), {"user_id": test_user_id})
            conn.execute(text("DELETE FROM users WHERE id = :user_id"), {"user_id": test_user_id})
            print("Test data cleaned up")

if __name__ == "__main__":
    test_full_chain()
