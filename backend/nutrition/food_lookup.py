import pandas as pd
from pathlib import Path

# Load food master CSV
BASE_DIR = Path(__file__).resolve().parent
FOOD_CSV = BASE_DIR / "food_master.csv"

df = pd.read_csv(FOOD_CSV)

def lookup_food(food_name: str):
    food_name = food_name.lower().strip()

    match = df[df["food_name"] == food_name]

    if match.empty:
        return None

    row = match.iloc[0]

    return {
        "food": food_name,
        "unit": row["unit"],
        "calories": float(row["calories"]),
        "protein": float(row["protein"]),
        "carbs": float(row["carbs"]),
        "fat": float(row["fat"])
    }
