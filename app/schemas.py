from pydantic import BaseModel, ConfigDict

class OrderCreate(BaseModel):
    symbol: str
    price: float
    quantity: int
    order_type: str

class Order(OrderCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)  
 