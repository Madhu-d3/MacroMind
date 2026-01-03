from rapidfuzz import process, fuzz
from backend.services.food_db import FOOD_DB

FOOD_NAMES = list(FOOD_DB.keys())

def fuzzy_match_food(word: str, threshold: int = 80):
    match, score, _ = process.extractOne(
        word,
        FOOD_NAMES,
        scorer=fuzz.WRatio
    )

    if score >= threshold:
        return match

    return None
