# calorie_calc.py
# Medically validated nutrition calculations for Aahar AI
import numpy as np

def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return np.round(bmi, 2)


def calculate_bmr(weight_kg, height_cm, age, gender):
    gender = gender.lower().strip()

    if gender == "male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    elif gender == "female":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    else:
        # For simplicity, we can return a default or raise an error.
        # In a vectorized operation, it might be better to handle this gracefully.
        raise ValueError("Gender must be 'male' or 'female'")

    return np.round(bmr, 2)


def get_activity_multiplier(activity_level):
    activity_level = activity_level.lower().strip()

    activity_map = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very active": 1.9
    }

    return activity_map.get(activity_level, 1.2)


def adjust_calories_for_goal(calories, goal):
    goal = goal.lower().strip()

    if goal == "weight loss":
        calories -= 500   # safe medical limit
    elif goal == "weight gain":
        calories += 500   # safe medical limit
    elif goal == "maintenance":
        pass  # No change needed
    else:
        raise ValueError("Invalid goal. Choose weight loss, weight gain, or maintenance.")

    return np.round(calories, 2)


def calculate_health_metrics(weight_kg, height_cm, age, gender, activity_level, goal):
    
    bmi = calculate_bmi(weight_kg, height_cm)
    bmr = calculate_bmr(weight_kg, height_cm, age, gender)

    multiplier = get_activity_multiplier(activity_level)
    tdee = bmr * multiplier
    daily_calories = adjust_calories_for_goal(tdee, goal)

    return {
        "bmi": bmi,
        "bmr": bmr,
        "daily_calories": daily_calories
    }
