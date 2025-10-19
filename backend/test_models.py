from models import Base, Investment
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

print("Models created successfully!")
print("Database tables can be created!")
session.close()
