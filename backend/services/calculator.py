def calculate_total(items: list[dict]) -> float | None:
    if not items:
        return None
    return sum(item["calories"] for item in items)
