import os
import asyncio
import websockets
import requests
import pytest
from fastapi.testclient import TestClient

# BaseURL for development and testing
BASE_URL = os.getenv("BASE_URL", "localhost:8000")
if os.getenv("DEV") == "true": 
    BASE_URL = "localhost:8000"

# Function to get a JWT token
def get_access_token(username: str, password: str):
    print(f"🚀 Using BASE_URL: {BASE_URL}")  # Debugging
    url = f"http://{BASE_URL}/token"
    print(f"🌐 Attempting to connect to: {url}")  # 
    
    response = requests.post(url, data={"username": username, "password": password})
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
       raise Exception(f"Failed to get access token: {response.text} (Status: {response.status_code})")

@pytest.mark.asyncio
async def test_websocket():
    username = "testuser"
    password = "testpassword"
    
    # Get access token
    token = get_access_token(username, password)
    
    async with websockets.connect(f"ws://{BASE_URL}/ws?token={token}") as websocket:
        print("Connected to WebSocket server")

        # Send a message
        await websocket.send("Hello, WebSocket!")
        print("Sent: Hello, WebSocket!")

        # Receive initial response
        response = await websocket.recv()
        print(f"Received: {response}")

        # Limit the number of messages to receive
        try:
            for _ in range(5):  # Change this to the desired number of messages to receive
                message = await asyncio.wait_for(websocket.recv(), timeout=5)  # 5 seconds timeout
                print(f"Received: {message}")
        except asyncio.TimeoutError:
            print("No more messages received, closing connection")
        except Exception as e:
            print(f"Connection closed with error: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())
