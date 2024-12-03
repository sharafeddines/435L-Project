# E-Commerce API Project

Welcome to the **E-Commerce API Project** repository! This project serves as the backend for an online shopping platform, providing modular services for managing customers, inventory, sales, and reviews. It is designed with scalability, maintainability, and security in mind.

---

## Key Features

### 1. **Customer Service**
- User registration and secure authentication.
- Wallet management with real-time balance updates.
- Profile updates and admin role-based access.

### 2. **Inventory Service**
- Add, update, and delete products.
- Real-time stock tracking.
- Search and filter inventory by category, price, and availability.

### 3. **Sales Service**
- Purchase transaction handling with sales history.
- Real-time inventory updates during transactions.
- Detailed sales analytics and reports.

### 4. **Review Service**
- Submit, edit, and delete product reviews.
- Moderation tools for administrators.
- Ensure reviews are tied to verified purchases.

---

## System Architecture

- **Frameworks**: Flask for lightweight and modular APIs.
- **Database**: SQLite for efficient data storage.
- **Deployment**: Docker containers for all services and the database.
- **Security**: JWT-based authentication, input validation, and rate-limiting.

---

## Running the Project

### Prerequisites
- Install [Docker](https://www.docker.com/products/docker-desktop).
- Clone this repository:
  ```bash
  git clone https://github.com/sharafeddines/435L-Project.git
  cd 435L-Project
### Step 1: Build and Run Docker Containers
1. Build and start all services using Docker Compose:
    ```bash
    docker-compose up --build -d
    ```
2. Verify the containers are running:
    ```bash
    docker ps
    ```
### Step 2: Access API Endpoints
- Customer Service: http://localhost:5001
- Inventory Service: http://localhost:5002
- Sales Service: http://localhost:5003
- Review Service: http://localhost:5004
- Database: http://localhost:1433

## Postman Collection
A Postman collection is provided in Appendix A of the documentation to simplify API testing. Import it into Postman to access predefined requests for all services.

## Deployment Notes
- Docker Compose orchestrates services and the database.
- All services are isolated using a custom Docker network.
- Configuration files for each service are included in their respective directories.

## Authors
- Sharafeddine Sharafeddine
- Omar Kandil
