import streamlit as st
import re
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

# Import utils
from utils import reset_password, validate_password_strength

st.markdown('<h2 class="auth-title">Reset Your Password</h2>', unsafe_allow_html=True)

# Get parameters from URL
query_params = st.query_params
token = query_params.get('token', [''])[0]
identifier = query_params.get('id', [''])[0]

if not token or not identifier:
    st.error("Invalid reset link. Please use the link sent to your email or phone.")
    if st.button("Back to Login"):
        st.switch_page("pages/2_Login.py")
    st.stop()

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

with st.form(key='reset_password_form'):
    st.markdown(f"<p><strong>User:</strong> {identifier}</p>", unsafe_allow_html=True)
    
    new_password = st.text_input("New Password", type="password", placeholder="Enter your new password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your new password")
    
    # Show password strength in real-time
    if new_password:
        strength, feedback = check_password_strength(new_password)
        strength_labels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
        strength_colors = ["#ff4444", "#ff8800", "#ffbb33", "#00C851", "#007E33"]
        
        st.progress(strength/5)
        st.markdown(f"<p style='color:{strength_colors[strength]};font-weight:bold'>Password Strength: {strength_labels[strength]}</p>", 
                   unsafe_allow_html=True)
        
        if feedback:
            st.markdown("**Missing requirements:** " + ", ".join(feedback))
    
    st.info("""Password must contain:
    • At least 8 characters
    • One uppercase letter
    • One lowercase letter
    • One number
    • One special character (!@#$%^&*(),.?:{}|<>)""")
    
    reset_submit = st.form_submit_button("Reset Password", type='primary')
    
    if reset_submit:
        errors = []
        
        if not new_password:
            errors.append("New password is required")
        if not confirm_password:
            errors.append("Please confirm your password")
        if new_password != confirm_password:
            errors.append("Passwords do not match")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            # Reset password
            success, message = reset_password(identifier, token, new_password)
            if success:
                st.success(message)
                st.success("You can now login with your new password.")
                if st.button("Go to Login"):
                    st.switch_page("pages/2_Login.py")
            else:
                st.error(message)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("Back to Login", type='secondary', use_container_width=True):
    st.switch_page("pages/2_Login.py")