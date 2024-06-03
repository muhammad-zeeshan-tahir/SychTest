# SYch FastAPI Prediction Server with Redis and Swagger

This project is a simple web application server built with FastAPI to simulate machine learning model predictions. It supports both synchronous and asynchronous prediction processing using Redis for in-memory storage. Additionally, it includes Swagger documentation for the API.

## Setup

### Prerequisites
- Docker
- Docker Compose
- Python 3.9+
- Redis

### Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd project
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the server:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8080
    ```

### Using Docker

1. Build the Docker image:
    ```bash
    docker-compose build
    ```

2. Run the Docker container:
    ```bash
    docker-compose up
    ```

## API Endpoints

### Synchronous Prediction

- **Endpoint:** `/predict`
- **Method:** `POST`
- **Request Body:** 
    ```json
    {
        "input": "Sample input data for the model"
    }
    ```
- **Response:** 
    ```json
    {
        "input": "Sample input data for the model",
        "result": "1234"
    }
    ```

### Asynchronous Prediction

- **Endpoint:** `/predict`
- **Method:** `POST`
- **Request Headers:**
    ```
    Async-Mode: true
    ```
- **Request Body:**
    ```json
    {
        "input": "Sample input data for the model"
    }
    ```
- **Response:**
    ```json
    {
        "message": "Request received. Processing asynchronously.",
        "prediction_id": "abc123"
    }
    ```

### Retrieve Prediction Result

- **Endpoint:** `/predict/{prediction_id}`
- **Method:** `GET`
- **Response:** 
    - **If still processing:**
        ```json
        {
            "error": "Prediction is still being processed."
        }
        ```
    - **If prediction ID is not found:**
        ```json
        {
            "error": "Prediction ID not found."
        }
        ```
    - **If result is available:**
        ```json
        {
            "prediction_id": "abc123",
            "output": {
                "input": "Sample input data for the model",
                "result": "5678"
            }
        }
        ```

## Swagger Documentation

- Access the automatically generated Swagger documentation at: `http://localhost:8080/docs`

## Additional Information

- **Type Hints:** Utilized throughout the code for clarity.
- **Documentation:** Inline comments and this README provide insights into the implementation and usage.
- **Docker:** The Dockerfile is optimized for creating a small and efficient image. Docker Compose is used to manage the application and Redis container.

