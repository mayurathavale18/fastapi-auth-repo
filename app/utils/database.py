# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from dotenv import load_dotenv
# import pymysql
# import os

# load_dotenv()

# DB_USER= os.getenv("DB_USER", "fastapi_user")
# DB_PASSWORD= os.getenv("DB_PASSWORD", "Mayur%407")
# DB_HOST= os.getenv("DB_HOST", "localhost")
# DB_NAME= os.getenv("DB_NAME", "user_auth")


# def get_db_connection():
#     return pymysql.connect(
#         host=DB_HOST,
#         user=DB_USER,
#         password=DB_PASSWORD,
#         database=DB_NAME,
#         cursorclass=pymysql.cursors.DictCursor
#     )

import os
from dotenv import load_dotenv
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Database credentials
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "fastapi_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Mayur%407")
DB_NAME = os.getenv("DB_NAME", "user_auth")

# SQLAlchemy Database URL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Setup SQLAlchemy Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def init_db():
    from app.models.user import User  # Import models
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables ensured.")