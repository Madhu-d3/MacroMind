import streamlit as st
from api import (
    get_profile,
    update_profile,
    predict_meal,
    save_meal
)


# ---------- Profile section ----------
def profile_section():
    st.subheader("👤 Profile")

    # Fetch profile once per session unless explicitly refreshed
    if "profile" not in st.session_state or st.session_state.get("profile_force_refresh"):
        st.session_state["profile"] = get_profile(st.session_state.token) or {}
        st.session_state["profile_force_refresh"] = False

    profile = st.session_state["profile"]

    # Use session_state-backed inputs so values persist while user is on the page
    if "profile_weight" not in st.session_state:
        st.session_state.profile_weight = profile.get("weight_kg") or 60.0
    if "profile_height" not in st.session_state:
        st.session_state.profile_height = profile.get("height_cm") or 165
    if "profile_goal" not in st.session_state:
        st.session_state.profile_goal = profile.get("daily_calorie_goal") or 2000

    weight = st.number_input(
        "Weight (kg)",
        value=st.session_state.profile_weight,
        key="profile_weight"
    )

    height = st.number_input(
        "Height (cm)",
        value=st.session_state.profile_height,
        key="profile_height"
    )

    goal = st.number_input(
        "Daily calorie goal",
        value=st.session_state.profile_goal,
        key="profile_goal"
    )

    if st.button("Save Profile"):
        # Update backend
        res = update_profile(
            st.session_state.token,
            {
                "weight_kg": weight,
                "height_cm": height,
                "daily_calorie_goal": goal
            }
        )

        # If backend returns JSON or 200, update local cache and rerun
        st.session_state.profile = {
            "weight_kg": weight,
            "height_cm": height,
            "daily_calorie_goal": goal
        }
        st.success("Profile updated")
        # # Force refresh next time we fetch profile from server if needed
        # st.session_state.profile_force_refresh = True
        st.rerun()



# ---------- Meal logging blocks ----------
def meal_block(title, meal_type):
    st.markdown(f"### 🍽 {title}")

    # Each block keeps its own keys to avoid clashes across meals
    food_key = f"{meal_type}_food"
    predicted_key = f"{meal_type}_predicted"
    override_key = f"{meal_type}_override"

    if food_key not in st.session_state:
        st.session_state[food_key] = ""

    food = st.text_input(
        f"What did you eat?",
        value=st.session_state.get(food_key, ""),
        key=food_key
    )

    # Predict step
    if st.button("Predict", key=f"{meal_type}_predict") and food:
        res = predict_meal(st.session_state.token, food)

        # Defensive handling of prediction response
        if isinstance(res, dict) and res.get("predicted_calories") is not None:
            try:
                st.session_state[predicted_key] = int(res["predicted_calories"])
            except Exception:
                st.error("Prediction returned unexpected value.")
                st.session_state[predicted_key] = None
        else:
            err = res.get("error") if isinstance(res, dict) else str(res)
            st.error(f"Prediction failed: {err}")
            st.session_state[predicted_key] = None

    predicted = st.session_state.get(predicted_key)

    if predicted is not None:
        # Use a session-backed override so the number_input retains value across reruns
        if override_key not in st.session_state:
            st.session_state[override_key] = predicted

        override = st.number_input(
            "Calories",
            min_value=0,
            value=st.session_state.get(override_key, predicted),
            key=override_key
        )

        if st.button("Save", key=f"{meal_type}_save"):
            payload = {
                "food_text": food,
                "meal_type": meal_type,
                # send predicted and override so backend can decide final_calories
                "predicted_calories": predicted,
                "overridden_calories": override
            }
            res = save_meal(st.session_state.token, payload)
            if isinstance(res, dict) and res.get("error"):
                st.error(f"Save failed: {res.get('error')}")
            else:
                st.success(f"{title} logged")
                # clear persisted values for this block
                st.session_state.pop(predicted_key, None)
                st.session_state.pop(override_key, None)
                # optionally clear the food field
                st.session_state[food_key] = ""
                # rerun to refresh UI / stats
                st.rerun()



def daily_log_section():
    st.subheader("📅 Daily Meal Log")

    # Breakfast, Lunch, Dinner, single Snacks box
    meal_block("Breakfast", "breakfast")
    st.divider()
    meal_block("Lunch", "lunch")
    st.divider()
    meal_block("Dinner", "dinner")
    st.divider()
    meal_block("Snacks", "snack")
