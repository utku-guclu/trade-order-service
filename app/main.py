# Import FastAPI
from fastapi import FastAPI

# Import the database engine and Base from database.py
from .database import engine, Base

# Import the Order model
from .models import Order  

# Create all database tables
Base.metadata.create_all(bind=engine)

# Create an instance of the FastAPI class
app = FastAPI()

# Define a root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Trade Order Service"}