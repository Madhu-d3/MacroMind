from sklearn.preprocessing import LabelEncoder
import pandas as pd

def prepare_features(df: pd.DataFrame):
    le = LabelEncoder()
    df["food_encoded"] = le.fit_transform(df["food"])

    X = df[["food_encoded", "quantity"]]
    y = df["calories"]

    return X, y, le
