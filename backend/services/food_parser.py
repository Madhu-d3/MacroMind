import re
from typing import List, Dict

# Calories per single unit
KNOWN_FOODS = {
    "idli": 60,
    "dosa": 133,
    "chapati": 120,
    "rice": 200
}


def normalize_food(word: str) -> str:
    """
    Normalize plural foods to singular.
    """
    if word.endswith("s"):
        return word[:-1]
    return word


def extract_food_items(text: str) -> List[Dict]:
    """
    Extract food items with quantities from free text.

    Example:
    "2 idlis and 1 dosa" →
    [
        {"food": "idli", "quantity": 2, "calories": 120},
        {"food": "dosa", "quantity": 1, "calories": 133}
    ]
    """

    text = text.lower()
    results = []
    used_foods = set()

    # Pattern: "2 idlis", "1 dosa"
    pattern = r"(\d+)\s*(\w+)"

    matches = re.findall(pattern, text)

    for qty, raw_food in matches:
        food = normalize_food(raw_food)

        if food in KNOWN_FOODS:
            quantity = int(qty)
            calories = quantity * KNOWN_FOODS[food]

            results.append({
                "food": food,
                "quantity": quantity,
                "calories": calories
            })
            used_foods.add(food)

    # Handle foods without explicit quantity → assume 1
    for food, cal in KNOWN_FOODS.items():
        if food in text and food not in used_foods:
            results.append({
                "food": food,
                "quantity": 1,
                "calories": cal
            })

    return results
