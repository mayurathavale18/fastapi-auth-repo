import os
import pymysql, psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database credentials
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "fastapi_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Mayur%407")
DB_NAME = os.getenv("DB_NAME", "fastapi_auth")

# SQLAlchemy Database URL
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


# Setup SQLAlchemy Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables ensured.")
    except Exception as e:
        print(f"Error creating database: {e}")