import re
from backend.services.food_db import FOOD_DB
from backend.services.constants import WORD_TO_NUMBER, FRACTIONS
from backend.services.fuzzy_matcher import fuzzy_match_food

def normalize_text(text: str) -> str:
    text = text.lower()

    for word, num in WORD_TO_NUMBER.items():
        text = re.sub(rf"\b{word}\b", str(num), text)

    return text


def parse_food_text(text: str):
    text = normalize_text(text)
    tokens = re.findall(r"[a-zA-Z]+|\d+\.?\d*", text)
    items = []

    for i, token in enumerate(tokens):
        food = fuzzy_match_food(token)

        if not food:
            continue

        qty = 1

        # look back for quantity
        if i > 0:
            prev = tokens[i - 1]
            if prev.replace(".", "", 1).isdigit():
                qty = float(prev)
            elif prev in FRACTIONS:
                qty = FRACTIONS[prev]

        calories_per_unit = FOOD_DB[food]["calories"]

        items.append({
            "food": food,
            "quantity": qty,
            "calories": round(qty * calories_per_unit, 2)
        })

    # remove duplicates (keep highest quantity)
    final = {}
    for item in items:
        food = item["food"]
        if food not in final or item["quantity"] > final[food]["quantity"]:
            final[food] = item

    return list(final.values())
