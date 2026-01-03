import pandas as pd
from sklearn.linear_model import LinearRegression
from joblib import dump
from features import prepare_features

# Load training data
df = pd.read_csv("backend/ml/meals.csv")

# Prepare features
X, y, label_encoder = prepare_features(df)

# Train Linear Regression model
model = LinearRegression()
model.fit(X, y)

# Save trained model and encoder
dump(model, "backend/ml/calorie_model.joblib")
dump(label_encoder, "backend/ml/label_encoder.joblib")

print("✅ Linear Regression model trained and saved")
