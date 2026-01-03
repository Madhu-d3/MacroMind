from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from datetime import datetime, timedelta
from backend.database import SessionLocal
from backend.auth.dependencies import get_current_user

from backend import models

router = APIRouter(
    prefix="/stats",
    tags=["Stats"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/daily")
def daily_calories(
    days: int = Query(7, le=30),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    start_date = datetime.utcnow() - timedelta(days=days)

    results = (
        db.query(
            cast(models.Meal.logged_at, Date).label("date"),
            func.sum(models.Meal.total_calories).label("total_calories")
        )
        .filter(
            models.Meal.user_id == current_user.user_id,
            models.Meal.logged_at >= start_date
        )
        .group_by(cast(models.Meal.logged_at, Date))
        .order_by(cast(models.Meal.logged_at, Date))
        .all()
    )

    return [
        {
            "date": r.date.isoformat(),
            "total_calories": round(r.total_calories, 2)
        }
        for r in results
    ]

@router.get("/weekly")
def weekly_calories(
    weeks: int = Query(4, le=12),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    start_date = datetime.utcnow() - timedelta(weeks=weeks)

    results = (
        db.query(
            func.date_trunc("week", models.Meal.logged_at).label("week"),
            func.sum(models.Meal.total_calories).label("total_calories")
        )
        .filter(
            models.Meal.user_id == current_user.user_id,
            models.Meal.logged_at >= start_date
        )
        .group_by(func.date_trunc("week", models.Meal.logged_at))
        .order_by(func.date_trunc("week", models.Meal.logged_at))
        .all()
    )

    return [
        {
            "week_start": r.week.date().isoformat(),
            "total_calories": round(r.total_calories, 2)
        }
        for r in results
    ]

@router.get("/deficit")
def daily_deficit(
    days: int = Query(7, le=30),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    goal = current_user.daily_calorie_goal
    start_date = datetime.utcnow() - timedelta(days=days)

    results = (
        db.query(
            cast(models.Meal.logged_at, Date).label("date"),
            func.sum(models.Meal.total_calories).label("consumed")
        )
        .filter(
            models.Meal.user_id == current_user.user_id,
            models.Meal.logged_at >= start_date
        )
        .group_by(cast(models.Meal.logged_at, Date))
        .order_by(cast(models.Meal.logged_at, Date))
        .all()
    )

    return [
        {
            "date": r.date.isoformat(),
            "goal": goal,
            "consumed": round(r.consumed, 2),
            "deficit": round(goal - r.consumed, 2)
        }
        for r in results
    ]
