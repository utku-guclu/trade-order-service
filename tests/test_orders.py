from app import schemas

# Test creating an order
def test_create_order(client, db_session):
    # Define test data
    order_data = {
        "symbol": "AAPL",
        "price": 150.0,
        "quantity": 10,
        "order_type": "buy"
    }

    # Send a POST request to create an order
    response = client.post("/orders/", json=order_data)

    # Assert the response status code and data
    assert response.status_code == 200
    assert response.json()["symbol"] == "AAPL"
    assert response.json()["price"] == 150.0
    assert response.json()["quantity"] == 10
    assert response.json()["order_type"] == "buy"
    assert "id" in response.json()

# Test retrieving orders
def test_get_orders(client, db_session):
    # Send a GET request to retrieve orders
    response = client.get("/orders/")

    # Assert the response status code and data
    assert response.status_code == 200
    assert isinstance(response.json(), list)