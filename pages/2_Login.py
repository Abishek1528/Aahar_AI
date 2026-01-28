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

with st.form(key='login_form'):
    username_or_phone = st.text_input("Name or Phone Number", placeholder="Enter your name or phone number")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    login_submit = st.form_submit_button("Login")
    
    if login_submit:
        if username_or_phone.strip() == "" or password.strip() == "":
            st.error("Please fill in all fields")
        else:
            user = validate_login(username_or_phone, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.current_user = user
                st.success("Login successful!")
                st.switch_page("pages/4_Calculator.py")
            else:
                st.error("Invalid credentials. Please try again.")

st.markdown("<br>", unsafe_allow_html=True)
if st.button("Don't have an account? Sign Up", type='secondary', use_container_width=True):
    st.switch_page("pages/2_Signup.py")

st.markdown('</div>', unsafe_allow_html=True)