from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from backend.database import SessionLocal
from backend.auth.dependencies import get_current_user
from backend import models
from pydantic import BaseModel
from datetime import date, timedelta


router = APIRouter()


# ---------- DB Dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Schemas ----------
class CalorieOverride(BaseModel):
    calories: float


class MealUpdate(BaseModel):
    food_text: str
    calories: float | None = None  # optional override


# ---------- Override Calories ----------
@router.patch("/{meal_id}/override")
def override_meal_calories(
    meal_id: int,
    payload: CalorieOverride,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    meal = (
        db.query(models.Meal)
        .filter(
            models.Meal.meal_id == meal_id,
            models.Meal.user_id == current_user.user_id
        )
        .first()
    )

    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    meal.overridden_calories = payload.calories
    db.commit()
    db.refresh(meal)

    return {
        "meal_id": meal.meal_id,
        "predicted_calories": meal.predicted_calories,
        "overridden_calories": meal.overridden_calories,
        "final_calories": meal.overridden_calories
    }


# ---------- Meal History ----------
@router.get("/history")
def meal_history(
    user_id: int = Query(...),
    limit: int = Query(10, le=50),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    meals = (
        db.query(models.Meal)
        .filter(models.Meal.user_id == user_id)
        .order_by(models.Meal.logged_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )

    return {
        "user_id": user_id,
        "count": len(meals),
        "limit": limit,
        "offset": offset,
        "meals": [
            {
                "meal_id": meal.meal_id,
                "food_text": meal.food_text,
                "calories": (
                    meal.overridden_calories
                    if meal.overridden_calories is not None
                    else meal.predicted_calories
                ),
                "logged_at": meal.logged_at
            }
            for meal in meals
        ]
    }


# ---------- Edit Meal ----------
@router.put("/{meal_id}")
def update_meal(
    meal_id: int,
    payload: MealUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    meal = (
        db.query(models.Meal)
        .filter(
            models.Meal.meal_id == meal_id,
            models.Meal.user_id == current_user.user_id
        )
        .first()
    )

    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    meal.food_text = payload.food_text

    # Optional calorie override
    if payload.calories is not None:
        meal.overridden_calories = payload.calories

    db.commit()
    db.refresh(meal)

    return {
        "message": "Meal updated successfully",
        "meal_id": meal.meal_id
    }


# ---------- Delete Meal ----------
@router.delete("/{meal_id}")
def delete_meal(
    meal_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    meal = (
        db.query(models.Meal)
        .filter(
            models.Meal.meal_id == meal_id,
            models.Meal.user_id == current_user.user_id
        )
        .first()
    )

    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    db.delete(meal)
    db.commit()

    return {
        "message": "Meal deleted successfully",
        "meal_id": meal_id
    }


# ---------- Daily Deficit / Surplus ----------
@router.get("/summary/deficit")
def calorie_deficit_or_surplus(
    user_id: int = Query(...),
    day: date = Query(default=date.today()),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    consumed = (
        db.query(
            func.coalesce(
                func.sum(
                    func.coalesce(
                        models.Meal.overridden_calories,
                        models.Meal.predicted_calories
                    )
                ),
                0
            )
        )
        .filter(
            models.Meal.user_id == user_id,
            cast(models.Meal.logged_at, Date) == day
        )
        .scalar()
    )

    goal = user.daily_calorie_goal
    difference = round(goal - consumed, 2)

    status = (
        "deficit" if difference > 0
        else "surplus" if difference < 0
        else "balanced"
    )

    return {
        "user_id": user_id,
        "date": day,
        "goal_calories": goal,
        "consumed_calories": round(consumed, 2),
        "difference": abs(difference),
        "status": status
    }

# ---------- Weekly summary endpoint ----------

@router.get("/summary/weekly")
def weekly_summary(
    user_id: int,
    db: Session = Depends(get_db)
):
    today = date.today()
    week_start = today - timedelta(days=6)

    rows = (
        db.query(
            cast(models.Meal.logged_at, Date).label("day"),
            func.coalesce(
                func.sum(
                    func.coalesce(
                        models.Meal.overridden_calories,
                        models.Meal.predicted_calories
                    )
                ),
                0
            ).label("calories")
        )
        .filter(
            models.Meal.user_id == user_id,
            cast(models.Meal.logged_at, Date) >= week_start
        )
        .group_by("day")
        .order_by("day")
        .all()
    )

    return {
        "user_id": user_id,
        "week_start": week_start,
        "week_end": today,
        "days": [
            {"date": str(r.day), "calories": round(r.calories, 2)}
            for r in rows
        ]
    }

