from joblib import load
import pandas as pd

model = load("backend/ml/calorie_model.joblib")
label_encoder = load("backend/ml/label_encoder.joblib")

def predict_calories(food: str, quantity: float):
    food_encoded = label_encoder.transform([food])[0]
    X = pd.DataFrame([[food_encoded, quantity]], columns=["food_encoded", "quantity"])
    return float(model.predict(X)[0])
