import streamlit as st
from calorie import calculate_health_metrics

import os
import sys

# CSS content (shared from main styles.css)
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
styles_path = os.path.join(root_dir, 'styles.css')

def load_css():
    try:
        with open(styles_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # Fallback: try relative to script path
        try:
            with open('styles.css', 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            # Return empty string if no CSS file found
            return ""

st.markdown(f'<style>{load_css()}</style>', unsafe_allow_html=True)

# Landing page content - only the landing page content with calculate health metrics button
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

# Call to action with animation - only calculate health metrics button
st.markdown('<h3 class="fade-in-element">Ready to Start Your Journey?</h3>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button('Calculate My Health Metrics', type='primary', use_container_width=True):
        st.switch_page("pages/4_Calculator.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button('Login', type='secondary', use_container_width=True):
        st.switch_page("pages/2_Login.py")
    
    if st.button('Sign Up', type='secondary', use_container_width=True):
        st.switch_page("pages/2_Signup.py")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="centered-content"><p>Aahar AI – Your Personal Nutrition Advisor</p></div>', unsafe_allow_html=True)