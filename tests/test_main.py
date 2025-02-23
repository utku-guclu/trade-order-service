import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def access_token():
    # Step 1: Get a token
    response = client.post("/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    return response.json()["access_token"]

def test_protected_route(access_token):
    # Step 2: Use the token to access the protected route
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
    
    # Update the expected response to include the 'exp' field
    assert response.json() == {
        "message": "This is a protected route",
        "user": {
            "sub": "testuser",
            "exp": response.json()["user"]["exp"] 
        }
    }

def test_protected_route_without_token():
    # Try to access the protected route without a token
    response = client.get("/protected")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}