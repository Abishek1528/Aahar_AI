import streamlit as st
import json
import os
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

with st.form(key='signup_form'):
    name = st.text_input("Full Name", placeholder="Enter your full name")
    age = st.number_input("Age", min_value=1, max_value=120, value=18, step=1)
    contact = st.text_input("Contact Number", placeholder="Enter your phone number")
    email = st.text_input("Email Address", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Create a password")
    signup_submit = st.form_submit_button("Sign Up")
    
    if signup_submit:
        if name.strip() == "" or contact.strip() == "" or email.strip() == "" or password.strip() == "":
            st.error("Please fill in all fields")
        else:
            success, message = signup_user(name, age, contact, email, password)
            if success:
                st.success(message)
                st.switch_page("pages/2_Login.py")
            else:
                st.error(message)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("Already have an account? Login", type='secondary', use_container_width=True):
    st.switch_page("pages/2_Login.py")

st.markdown('</div>', unsafe_allow_html=True)