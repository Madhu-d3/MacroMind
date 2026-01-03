from fastapi import FastAPI

from backend.database import engine
from backend import models

# Routers
from backend.routers import users, meals, predict, summary, auth, stats

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MacroMind API")

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(meals.router, prefix="/meals", tags=["Meals"])
app.include_router(predict.router, prefix="/predict", tags=["Predict"])
app.include_router(summary.router, prefix="/summary", tags=["Summary"])
app.include_router(stats.router, prefix="/stats", tags=["Stats"])


@app.get("/")
def root():
    return {"message": "MacroMind API is running 🚀"}
