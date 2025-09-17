import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Expect an env var like:
# SUPABASE_DB_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/postgres?sslmode=require
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")
if not SUPABASE_DB_URL:
    raise RuntimeError("SUPABASE_DB_URL not set. Create a .env file (see .env.example).")

engine = create_engine(SUPABASE_DB_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency: yield a DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
