import streamlit as st
import json
import os
import re
from utils import signup_user

# Initialize session state if not already done
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

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

# Signup page 

st.markdown('<h2 class="auth-title">Create New Account</h2>', unsafe_allow_html=True)

# Password strength indicator
def check_password_strength(password):
    strength = 0
    feedback = []
    
    if len(password) >= 8:
        strength += 1
    else:
        feedback.append("At least 8 characters")
    
    if re.search(r'[A-Z]', password):
        strength += 1
    else:
        feedback.append("Uppercase letter")
    
    if re.search(r'[a-z]', password):
        strength += 1
    else:
        feedback.append("Lowercase letter")
    
    if re.search(r'\d', password):
        strength += 1
    else:
        feedback.append("Number")
    
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        strength += 1
    else:
        feedback.append("Special character")
    
    return strength, feedback

with st.form(key='signup_form'):
    name = st.text_input("Full Name", placeholder="Enter your full name", max_chars=50)
    age = st.number_input("Age", min_value=13, max_value=120, value=18, step=1, 
                         help="Must be between 13 and 120 years old")
    
    contact_col1, contact_col2 = st.columns([3,1])
    with contact_col1:
        contact = st.text_input("Phone Number", placeholder="Enter 10-digit phone number", max_chars=10)
    with contact_col2:
        st.markdown("<br>Format: 1234567890", unsafe_allow_html=True)
    
    email = st.text_input("Email Address", placeholder="Enter your email", max_chars=100)
    
    # Password with strength indicator
    password = st.text_input("Password", type="password", placeholder="Create a strong password")
    
    # Show password strength in real-time
    if password:
        strength, feedback = check_password_strength(password)
        strength_labels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
        strength_colors = ["#ff4444", "#ff8800", "#ffbb33", "#00C851", "#007E33"]
        strength_index = 4 if strength > 4 else strength
        
        st.progress(int(strength * 20))
        st.markdown(f"<p style='color:{strength_colors[strength_index]};font-weight:bold'>Password Strength: {strength_labels[strength_index]}</p>", 
                   unsafe_allow_html=True)
        
        if feedback:
            st.markdown("**Missing requirements:** " + ", ".join(feedback))
    
    st.info("""Password must contain:
    • At least 8 characters
    • One uppercase letter
    • One lowercase letter
    • One number
    • One special character (!@#$%^&*(),.?:{}|<>)""")
    
    signup_submit = st.form_submit_button("Create Account", type='primary')
    
    if signup_submit:
        # Additional client-side validation
        errors = []
        if not name.strip():
            errors.append("Name is required")
        if not contact.strip():
            errors.append("Phone number is required")
        if not email.strip():
            errors.append("Email is required")
        if not password.strip():
            errors.append("Password is required")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            success, message = signup_user(name, age, contact, email, password)
            if success:
                st.success(message)
                st.info("Redirecting to login page...")
                st.switch_page("pages/2_Login.py")
            else:
                # Split multiple errors and display them nicely
                error_messages = message.split('; ') if '; ' in message else [message]
                for error_msg in error_messages:
                    st.error(error_msg)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("Already have an account? Login", type='secondary', use_container_width=True):
    st.switch_page("pages/2_Login.py")

st.markdown('</div>', unsafe_allow_html=True)
