from pydantic import BaseModel

class PredictionRequest(BaseModel):
    input: str

class PredictionResponse(BaseModel):
    input: str
    result: str

class AsyncResponse(BaseModel):
    message: str
    prediction_id: str