import streamlit as st
import numpy as np
import pandas as pd
from calorie import calculate_health_metrics

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Set page configuration
st.set_page_config(
    page_title="Aahar AI - Home",
    page_icon="🥗",
    layout="centered"
)

# Read and inject CSS from external file
try:
    with open('styles.css', 'r') as f:
        css_content = f.read()
        st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    # Fallback to inline CSS if external file not found
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .fade-in-element {
        animation: fadeIn 1.5s ease-out;
    }
    
    .side-decoration {
        position: fixed;
        top: 50%;
        transform: translateY(-50%);
        font-size: 4rem;
        opacity: 0.1;
        z-index: -1;
        animation: float 6s ease-in-out infinite;
    }
    
    .left-decoration {
        left: 20px;
        animation-delay: 0s;
    }
    
    .right-decoration {
        right: 20px;
        animation-delay: 0.5s;
    }
    
    .centered-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 2rem;
        position: relative;
    }
    
    .feature-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border: 1px solid #e0e0e0;
        color: #333;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .feature-card:hover {
        transform: translateY(-5px) scale(1.03);
        box-shadow: 0 12px 20px rgba(255, 152, 0, 0.3);
        border-color: #FF9800;
        background-color: #fff3e0;
        color: #e65100;
    }
    
    .calculator-container {
        max-width: 800px;
        margin: auto;
        padding: 20px;
    }
    
    .main-title {
        font-size: 2.5rem;
        color: #2e7d32;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #555;
        margin-bottom: 2rem;
    }
    
    .btn-primary {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1rem;
        transition: background-color 0.3s;
    }
    
    .btn-primary:hover {
        background-color: #45a049;
    }
    
    .btn-secondary {
        background-color: #f5f5f5;
        color: #333;
        border: 1px solid #ddd;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 0.9rem;
        margin-top: 1rem;
    }
    
    .btn-secondary:hover {
        background-color: #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# Define functions for each page
if st.session_state.page == 'home':
    # Landing page content
    # Add decorative elements
    st.markdown('''
    <div class="side-decoration left-decoration">🥗</div>
    <div class="side-decoration right-decoration">🥗</div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<div class="centered-content">', unsafe_allow_html=True)

    # Animated title
    st.markdown('<h1 class="main-title fade-in-element">Aahar AI</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="fade-in-element">Health Metrics Calculator</h2>', unsafe_allow_html=True)

    # Subtitle with animation
    st.markdown('<p class="subtitle fade-in-element">Calculate your BMI, BMR, and daily calorie needs based on your personal information and goals.</p>', unsafe_allow_html=True)

    st.markdown("---")

    # Features with animations
    st.markdown('<h3 class="fade-in-element">Key Features</h3>', unsafe_allow_html=True)

    # Feature grid
    feature_col1, feature_col2 = st.columns(2)

    with feature_col1:
        st.markdown('''
        <div class="feature-card fade-in-element">
        <h4>📊 BMI Calculation</h4>
        <p>Understand your Body Mass Index</p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
        <div class="feature-card fade-in-element">
        <h4>⚡ BMR Analysis</h4>
        <p>Know your Basal Metabolic Rate</p>
        </div>
        ''', unsafe_allow_html=True)

    with feature_col2:
        st.markdown('''
        <div class="feature-card fade-in-element">
        <h4>🔥 TDEE Estimation</h4>
        <p>Calculate your Total Daily Energy Expenditure</p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
        <div class="feature-card fade-in-element">
        <h4>🎯 Personalized Recommendations</h4>
        <p>Tailored calorie goals based on your objectives</p>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")

    # Call to action with animation
    st.markdown('<h3 class="fade-in-element">Ready to Start Your Journey?</h3>', unsafe_allow_html=True)

    if st.button('Calculate My Health Metrics', type='primary'):
        st.session_state.page = 'calculator'
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown('<div class="centered-content"><p>Aahar AI – Your Personal Nutrition Advisor</p></div>', unsafe_allow_html=True)

elif st.session_state.page == 'calculator':
    # Calculator page content
    st.markdown('<div class="calculator-container">', unsafe_allow_html=True)
    
    # Title
    st.title("Aahar AI – Health Metrics Calculator")
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
    if st.sidebar.button("Calculate Health Metrics", type='primary'):
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
                st.metric(label="BMR (Basal Metabolic Rate)", value=result["bmr"], delta=None)
                st.caption(f"{result['bmr']} kcal/day")
                
            with col3:
                st.metric(label="Recommended Daily Calories (TDEE)", value=result["daily_calories"], delta=None)
                st.caption(f"{result['daily_calories']} kcal/day")
            
        except ValueError as e:
            st.error(f"Error in input: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    else:
        # Default welcome message
        st.subheader("Aahar AI Health Metrics Calculator")
        st.write("Please enter your health information in the sidebar and click 'Calculate Health Metrics'")
    
    st.markdown('</div>', unsafe_allow_html=True)