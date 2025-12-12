# FastAPI Auth API

A robust authentication API built with FastAPI, SQLAlchemy (async), and PostgreSQL.

## Features

- User Registration
- User Login (JWT Authentication)
- Protected Routes
- Async Database Operations
- Dockerized Environment

## Prerequisites

- Docker & Docker Compose

## Getting Started

1.  **Clone the repository**
2.  **Start the services**

    ```bash
    sudo docker compose up --build
    ```

    The API will be available at `http://localhost:8000`.

## API Documentation

Once the application is running, you can access the interactive API documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Running Tests

To run the test suite inside the Docker environment:

```bash
sudo docker compose run --rm tests
```
