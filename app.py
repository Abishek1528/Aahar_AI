import streamlit as st
import numpy as np
import pandas as pd
from calorie import calculate_health_metrics

# Set page configuration
st.set_page_config(
    page_title="🥗 Aahar AI – Health Metrics Calculator",
    
    layout="wide"
)

# Title
st.title("🥗 Aahar AI – Health Metrics Calculator")
st.markdown("---")

# Sidebar for user inputs
st.sidebar.header("Enter Your Health Information")

# Input fields
weight_kg = st.sidebar.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=64.0, step=0.1)
height_cm = st.sidebar.number_input("Height (cm)", min_value=50.0, max_value=300.0, value=180.0, step=0.1)
age = st.sidebar.number_input("Age", min_value=1, max_value=120, value=19, step=1)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
activity_level = st.sidebar.selectbox(
    "Activity Level",
    ["Sedentary", "Light", "Moderate", "Active", "Very Active"]
)
goal = st.sidebar.selectbox(
    "Diet Goal",
    ["Weight Loss", "Maintenance", "Weight Gain"]
)

# Convert to lowercase for the function
gender_lower = gender.lower()
activity_lower = activity_level.lower()
goal_lower = goal.lower()

# Calculate metrics when button is clicked
if st.sidebar.button("Calculate Health Metrics"):
    try:
        # Call the calculation function
        result = calculate_health_metrics(
            weight_kg=weight_kg,
            height_cm=height_cm,
            age=age,
            gender=gender_lower,
            activity_level=activity_lower,
            goal=goal_lower
        )
        
        # Display results
        st.subheader("Your Health Metrics")

        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="BMI (Body Mass Index)", value=result["bmi"])
            # Interpret BMI
            if result["bmi"] < 18.5:
                st.caption("Underweight")
            elif 18.5 <= result["bmi"] < 25:
                st.caption("Normal weight")
            elif 25 <= result["bmi"] < 30:
                st.caption("Overweight")
            else:
                st.caption("Obese")
                
        with col2:
            st.metric(label="BMR (Basal Metabolic Rate)", value=f"{result['bmr']} kcal/day")
        
            
        with col3:
            st.metric(label="Recommended Daily Calories (TDEE)", value=f"{result['daily_calories']} kcal/day")

        
    except ValueError as e:
        st.error(f"Error in input: {str(e)}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

else:
    # Default welcome message
    st.subheader("Aahar AI Health Metrics Calculator")
    st.write("Please enter your health information in the sidebar and click 'Calculate Health Metrics'")