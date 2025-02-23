# Import SQLAlchemy components
from sqlalchemy import Column, Integer, String, Float
from .database import Base

# Define the Order model
class Order(Base):
    __tablename__ = "orders"  # Name of the table in the database

    # Columns in the table
    id = Column(Integer, primary_key=True, index=True)  # Primary key
    symbol = Column(String, index=True)  # Stock symbol (e.g., "AAPL")
    price = Column(Float)  # Price of the trade
    quantity = Column(Integer)  # Quantity of the trade
    order_type = Column(String)  # Type of order (e.g., "buy" or "sell")