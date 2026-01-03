from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey , Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    height_cm = Column(Integer)
    weight_kg = Column(Float)
    daily_calorie_goal = Column(Integer, default=2000)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    password_hash = Column(String)
    is_active = Column(Boolean, default=True)
    
    meals = relationship("Meal", back_populates="user")


# backend/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base

class Meal(Base):
    __tablename__ = "meals"

    meal_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))

    food_text = Column(String)
    normalized_json = Column(JSON)

    predicted_calories = Column(Float)               # ML output
    overridden_calories = Column(Float, nullable=True)  # user override

    logged_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="meals")

    @property
    def final_calories(self):
        return (
            self.overridden_calories
            if self.overridden_calories is not None
            else self.predicted_calories
        )
