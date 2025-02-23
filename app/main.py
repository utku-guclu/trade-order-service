from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Trade Order Service"}

# Endpoint to create a new order
@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """
    Accepts a POST request with order details, creates the order in the database, and returns the created order.
    """
    return crud.create_order(db=db, order=order)

# Endpoint to retrieve a list of orders
@app.get("/orders/", response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Accepts a GET request and returns a list of orders, with optional pagination.
    """
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders