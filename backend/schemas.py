from pydantic import BaseModel, Field, validator


class LoginRequest(BaseModel):
    name: str
    password: str

class UserCreate(BaseModel):
    name: str
    height_cm: int
    weight_kg: float


class MealCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    food_text: str = Field(..., min_length=3)

    @validator("food_text")
    def food_text_not_empty(cls, v):
        if not v.strip():
            raise ValueError("food_text cannot be empty")
        return v
    
class PredictionRequest(BaseModel):
    food_text: str = Field(..., min_length=3)


