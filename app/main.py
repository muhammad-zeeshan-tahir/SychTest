from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, Union
import json
import os
import uuid
import redis
from fastapi.openapi.utils import get_openapi
from .models import PredictionRequest, PredictionResponse, AsyncResponse
from .background_tasks import async_predict, mock_model_predict
import logging


logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Get Redis connection details from environment variables
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = int(os.getenv('REDIS_PORT', 6379))

# Connect to Redis
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)


app = FastAPI()

# Get Redis connection details from environment variables
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = int(os.getenv('REDIS_PORT', 6379))

# Connect to Redis
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)


@app.post("/predict", response_model=Union[PredictionResponse, AsyncResponse])
async def predict(request: PredictionRequest, background_tasks: BackgroundTasks, request_info: Request):
    """
    Handles synchronous and asynchronous prediction requests based on the presence of the 'Async-Mode' header.
    """
    if request_info.headers.get('Async-Mode') == "True":
        # Asynchronous processing
        prediction_id = str(uuid.uuid4())
        redis_client.set(prediction_id, json.dumps({"status": "processing"}))
        background_tasks.add_task(async_predict, prediction_id, request.input)
        return JSONResponse(
            status_code=202,
            content={"message": "Request received. Processing asynchronously.", "prediction_id": prediction_id},
        )
    else:
        # Synchronous processing
        result = mock_model_predict(request.input)
        return PredictionResponse(**result)


@app.get("/predict/{prediction_id}")
async def get_prediction(prediction_id: str):
    """
    Retrieves the result of an asynchronous prediction based on the provided prediction ID.
    """
    prediction = redis_client.get(prediction_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction ID not found.")
    prediction_data = json.loads(prediction)
    if prediction_data["status"] == "processing":
        raise HTTPException(status_code=400, detail="Prediction is still being processed.")
    return {"prediction_id": prediction_id, "output": prediction_data["result"]}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    try:
        openapi_schema = get_openapi(
            title="FastAPI with Async-Mode",
            version="1.0.0",
            description="API for asynchronous and synchronous predictions with FastAPI",
            routes=app.routes,
        )
        # Add custom headers for /predict endpoint
        openapi_schema["paths"]["/predict"]["post"]["parameters"] = [
            {
                "name": "Async-Mode",
                "in": "header",
                "default": "False",
                "required": False,
                "schema": {"type": "string"},
                "description": "Enable asynchronous processing by setting this header to 'True'."
            }
        ]
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    except Exception as e:
        logging.error(f"Error generating OpenAPI schema: {e}")
        raise e


app.openapi = custom_openapi
