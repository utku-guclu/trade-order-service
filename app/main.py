# Import FastAPI
from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

# Define a root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Trade Order Service"}