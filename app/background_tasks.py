import os
import time
import random
import redis
import json
from .models import PredictionResponse

# Get Redis connection details from environment variables
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = int(os.getenv('REDIS_PORT', 6379))

# Connect to Redis
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)

def mock_model_predict(input: str) -> dict:
    """
    Simulates a machine learning model prediction with a random delay and result.
    """
    time.sleep(random.randint(8, 15))  # Simulate processing delay
    result = str(random.randint(100, 10000))
    return {"input": input, "result": result}

async def async_predict(prediction_id: str, input_data: str) -> None:
    """
    Processes the prediction asynchronously and stores the result in Redis.
    """
    result = mock_model_predict(input_data)
    redis_client.set(prediction_id, json.dumps({"status": "completed", "result": result}))
