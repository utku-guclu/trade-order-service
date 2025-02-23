import os
import logging
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from dotenv import load_dotenv  # Import load_dotenv
from . import crud, models, schemas
from secrets import token_hex
from .database import SessionLocal, engine


# Load environment variables from .env file
load_dotenv()

# Access the secret key and algorithm from environment variables
SECRET_KEY = token_hex(32)
ALGORITHM = "HS256"

# Token expiration time (e.g., 30 minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Store connected WebSocket clients
connected_clients = []

# Function to create a JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Decoded token payload: {payload}")
        return payload
    except JWTError as e:
        logger.error(f"Invalid token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

# Token endpoint
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # In a real application, you would validate the username and password here
    user = {"sub": form_data.username}  # "sub" is the subject (usually the user ID)
    access_token = create_access_token(data=user)
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route
@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    logger.info(f"Accessing protected route with user: {current_user}")
    return {"message": "This is a protected route", "user": current_user}

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):  # Use Query for WebSocket token
    await websocket.accept()
    
    # Validate the token
    try:
        user = await get_current_user(token)
        connected_clients.append(websocket)
        logger.info(f"Client connected: {user['sub']}")

        while True:
            data = await websocket.receive_text()
            # Echo the received message back to the client
            await websocket.send_text(f"Message received: {data}")

            # Broadcast the received message to all connected clients
            for client in connected_clients:
                if client != websocket:  # Don't send back to the sender
                    await client.send_text(f"New message: {data}")
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Connection closed with error: {e}")
        await websocket.close(code=1008, reason="Invalid token")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Trade Order Service"}

# Endpoint to create a new order
@app.post("/orders/", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    new_order = crud.create_order(db=db, order=order)
    # Notify all connected clients about the new order
    for client in connected_clients:
        await client.send_text(f"New order created: {new_order}")
    return new_order

# Endpoint to retrieve a list of orders
@app.get("/orders/", response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders
