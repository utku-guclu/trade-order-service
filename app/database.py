# Import SQLAlchemy components
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL (SQLite in this case)
SQLALCHEMY_DATABASE_URL = "sqlite:///./trade_orders.db"

# Create a database engine
# `connect_args={"check_same_thread": False}` is required for SQLite to work with FastAPI
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models
Base = declarative_base()