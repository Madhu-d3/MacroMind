from sqlalchemy.orm import Session
from backend import models
from backend.database import SessionLocal

def save_meal(
    user_id: int,
    food_text: str,
    items: list,
    total_calories: float
):
    db: Session = SessionLocal()
    try:
        meal = models.Meal(
            user_id=user_id,
            food_text=food_text,
            normalized_json=items,
            total_calories=total_calories
        )
        db.add(meal)
        db.commit()
        db.refresh(meal)
        return meal
    finally:
        db.close()
