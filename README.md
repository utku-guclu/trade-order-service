# Trade Order Service

This is a simple backend service that exposes REST APIs for managing trade orders. The service is built using **FastAPI** (Python) and supports **WebSocket** for real-time order status updates. It is containerized using **Docker** and deployed on an **AWS EC2** instance with a **CI/CD pipeline** using **GitHub Actions**.

## Features
- **REST APIs**:
  - `POST /orders/`: Submit a new trade order.
  - `GET /orders/`: Retrieve a list of submitted orders.
- **WebSocket**:
  - Real-time notifications for new orders.
- **Authentication**:
  - JWT-based authentication for protected routes.
- **Database**:
  - Uses **SQLite** for simplicity (can be switched to **PostgreSQL**).
- **CI/CD**:
  - Automated testing, building, and deployment using **GitHub Actions**.

## Setup

### Prerequisites
- Python 3.9+
- Docker
- Docker Compose (optional)
- AWS EC2 instance (for deployment)

### Local Development
1. Clone the repository:
   ```bash
   git clone https://github.com/utku-guclu/trade-order-service.git
   cd trade-order-service
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```
4. Access the API documentation:
   ```bash
   Swagger UI: http://127.0.0.1:8000/docs
   Redoc UI: http://127.0.0.1:8000/redoc
   ```

### Docker
1. Build the Docker image:
   ```bash
   docker build -t trade-order-service .
   ```
2. Run the Docker container:
   ```bash
   docker run -d -p 80:80 --name trade-order-service trade-order-service
   ```

### Deployment
1. Set up an AWS EC2 instance with Docker installed.
2. Push the Docker image to Docker Hub:
   ```bash
   docker tag trade-order-service <your-dockerhub-username>/trade-order-service
   docker push <your-dockerhub-username>/trade-order-service
   ```
3. Deploy the application to the EC2 instance using the provided GitHub Actions workflow.

## Testing
Run the tests using pytest:
```bash
pytest
```

## API Endpoints
- Root: GET '/'
  - Returns a welcome message.
- Create Order: POST '/orders/'
  - Accepts trade order details (e.g., symbol, price, quantity, order type).
- List Orders: GET /orders/
  - Retrieves a list of submitted orders.
- Protected Route: GET /protected
  - Requires a valid JWT token.
- WebSocket: ws://<host>/ws
  - Real-tim notifications for new orders.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
