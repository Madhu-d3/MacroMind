from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from backend.database import SessionLocal
from backend import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/daily")
def daily_summary(
    user_id: int = Query(...),
    day: date = Query(...),
    db: Session = Depends(get_db)
):
    meals = (
        db.query(models.Meal)
        .filter(models.Meal.user_id == user_id)
        .filter(models.Meal.logged_at.cast(date) == day)
        .all()
    )

    total_calories = sum(meal.total_calories for meal in meals)

    return {
        "user_id": user_id,
        "date": day,
        "total_calories": total_calories,
        "meal_count": len(meals),
        "meals": [
            {
                "meal_id": meal.meal_id,
                "food_text": meal.food_text,
                "calories": meal.total_calories,
                "logged_at": meal.logged_at
            }
            for meal in meals
        ]
    }
