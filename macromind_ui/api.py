import requests
from config import API_URL

def signup(name, password):
    return requests.post(
        f"{API_URL}/auth/signup",
        params={"name": name, "password": password}
    )

def login(name, password):
    return requests.post(
        f"{API_URL}/auth/login",
        json={"name": name, "password": password}
    )

def auth_headers(token):
    return {"Authorization": f"Bearer {token}"} if token else {}

def get_profile(token):
    res = requests.get(
        f"{API_URL}/users/me",
        headers=auth_headers(token)
    )
    try:
        return res.json()
    except Exception:
        return {}

def update_profile(token, payload):
    res = requests.put(
        f"{API_URL}/users/me",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json=payload
    )

    if res.status_code != 200:
        raise Exception(res.text)

    return res.json()


def predict_meal(token, food_text):
    res = requests.post(
        f"{API_URL}/meals/predict",
        headers=auth_headers(token),
        json={"food_text": food_text}
    )
    try:
        return res.json()
    except Exception:
        # return a stable error dict for UI to interpret
        return {"error": res.text or "Prediction failed", "status_code": res.status_code}

def save_meal(token, payload):
    res = requests.post(
        f"{API_URL}/meals",
        headers=auth_headers(token),
        json=payload
    )
    try:
        return res.json()
    except Exception:
        return {"error": res.text or "Save failed", "status_code": res.status_code}
