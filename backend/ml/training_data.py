import pandas as pd

# Synthetic starter dataset (you will replace this later with real DB data)
data = [
    {"food": "idli", "quantity": 1, "calories": 60},
    {"food": "idli", "quantity": 2, "calories": 120},
    {"food": "dosa", "quantity": 1, "calories": 130},
    {"food": "rice", "quantity": 1, "calories": 200},
    {"food": "rice", "quantity": 0.5, "calories": 100},
    {"food": "chapati", "quantity": 2, "calories": 240},
    {"food": "banana", "quantity": 1, "calories": 100},
    {"food": "idli", "quantity": 3, "calories": 180},
    {"food": "idli", "quantity": 4, "calories": 240},
    {"food": "idli", "quantity": 5, "calories": 300},

]

df = pd.DataFrame(data)
df.to_csv("backend/ml/meals.csv", index=False)
