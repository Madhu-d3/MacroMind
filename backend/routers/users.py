from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user, get_db
from backend import models

router = APIRouter()


class ProfileUpdate(BaseModel):
    weight_kg: int | None = None
    height_cm: int | None = None
    daily_calorie_goal: int | None = None


@router.get("/me")
def get_me(current_user: models.User = Depends(get_current_user)):
    return {
        "user_id": current_user.user_id,
        "name": current_user.name,
        "weight_kg": current_user.weight_kg,
        "height_cm": current_user.height_cm,
        "daily_calorie_goal": current_user.daily_calorie_goal,
    }


@router.put("/me")
def update_me(
    payload: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return {"message": "Profile updated"}
