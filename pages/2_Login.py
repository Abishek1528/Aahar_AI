import streamlit as st
import json
import os
from utils import login_user, validate_login

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


# Login page content


st.markdown('<h2 class="auth-title">Login to Your Account</h2>', unsafe_allow_html=True)

# Check session validity
from utils import is_current_session_valid

if not is_current_session_valid():
    # Session expired or not authenticated
    pass  # Continue to show login form

with st.form(key='login_form'):
    identifier = st.text_input("Email or Phone Number", placeholder="Enter your email or phone number")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    login_submit = st.form_submit_button("Login", type='primary')
    
    if login_submit:
        if identifier.strip() == "" or password.strip() == "":
            st.error("Please fill in all fields")
        else:
            success, message = login_user(identifier, password)
            if success:
                st.success(message)
                st.switch_page("pages/4_Calculator.py")
            else:
                st.error(message)

# Password recovery section
st.markdown("---")
st.markdown("<h4>Password Recovery</h4>", unsafe_allow_html=True)

with st.expander("Forgot your password?"):
    recovery_identifier = st.text_input("Enter your email or phone number for recovery")
    if st.button("Send Recovery Link"):
        if recovery_identifier.strip():
            from utils import initiate_password_reset
            success, result = initiate_password_reset(recovery_identifier)
            if success:
                st.success("Recovery instructions sent! Please check your email or messages.")
                st.info("Note: In a real application, this would send an email/SMS with a recovery link.")
            else:
                st.error(result)
        else:
            st.error("Please enter your email or phone number")

st.markdown("<br>", unsafe_allow_html=True)
if st.button("Don't have an account? Sign Up", type='secondary', use_container_width=True):
    st.switch_page("pages/2_Signup.py")

st.markdown('</div>', unsafe_allow_html=True)