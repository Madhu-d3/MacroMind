import re
from backend.nutrition.food_lookup import lookup_food

def parse_meal_text(text: str):
    """
    Input: '2 idlis and 1 cup rice'
    Output: list of parsed food items
    """

    text = text.lower()
    text = text.replace("and", ",")

    parts = text.split(",")

    parsed_items = []

    for part in parts:
        part = part.strip()

        # Extract quantity (default = 1)
        qty_match = re.search(r"\d+", part)
        qty = int(qty_match.group()) if qty_match else 1

        # Remove numbers and units
        food_name = re.sub(r"\d+|cup|cups|piece|pieces", "", part).strip()

        food_data = lookup_food(food_name)

        if food_data:
            food_data["quantity"] = qty
            food_data["total_calories"] = qty * food_data["calories"]
            parsed_items.append(food_data)

    return parsed_items
