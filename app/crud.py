from sqlalchemy.orm import Session
from . import models, schemas

# Function to create a new order in the database
def create_order(db: Session, order: schemas.OrderCreate):
    # Create a SQLAlchemy model instance from the Pydantic model
    db_order = models.Order(**order.dict()) # Unpack the order object
    
    # Add the instance to the database session
    db.add(db_order)
    
    # Commit the transaction to save the order
    db.commit()
    
    # Refresh the instance to get the auto-generated ID
    db.refresh(db_order)
    
    # Return the created order
    return db_order

# Function to retrieve a list of orders from the database
def get_orders(db: Session, skip: int = 0, limit: int = 100):
    # Query the database for orders, with optional pagination
    # Returns up to 'limit' number of orders, starting from 'skip'
    return db.query(models.Order).offset(skip).limit(limit).all()