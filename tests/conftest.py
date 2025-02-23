import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal

# Fixture to override the database with a test database
@pytest.fixture(scope="module")
def test_db():
    """
    Creates and drops the test database tables before and after tests.
    """
    # Create all tables in the test database
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after tests are done
    Base.metadata.drop_all(bind=engine)

# Fixture to provide a test client
@pytest.fixture(scope="module")
def client(test_db):
    """
    Provides a FastAPI TestClient for making API requests.
    """
    with TestClient(app) as test_client:
        yield test_client

# Fixture to provide a database session
@pytest.fixture(scope="module")
def db_session():
    """
    Provides a database session for testing database operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()