from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.hybrid_predictor import hybrid_calorie_prediction

router = APIRouter()

class PredictRequest(BaseModel):
    food_text: str

@router.post("/predict")
def predict_meal(payload: PredictRequest):
    calories = hybrid_calorie_prediction(payload.food_text)

    return {
        "predicted_calories": calories
    }
