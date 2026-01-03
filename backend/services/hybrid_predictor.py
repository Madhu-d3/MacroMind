from fastapi import HTTPException
from backend.services.food_parser import extract_food_items
from backend.services.meal_service import save_meal

def hybrid_calorie_prediction(food_text: str) -> float:
    items = extract_food_items(food_text)

    if not items:
        raise HTTPException(
            status_code=400,
            detail="Could not extract any food items from input"
        )

    total_calories = sum(item["calories"] for item in items)
    return round(float(total_calories), 2)
