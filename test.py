from calorie import calculate_health_metrics

result = calculate_health_metrics(
    weight_kg=70,
    height_cm=175,
    age=23,
    gender="male",
    activity_level="moderate",
    goal="weight gain"
)

print("BMI:", result["bmi"])
print("BMR:", result["bmr"])
print("Daily Calories:", result["daily_calories"])
