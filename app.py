import streamlit as st
import os
import json

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Set page configuration
st.set_page_config(
    page_title="Aahar AI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ensure users.json exists
def initialize_users_file():
    users_file = os.path.join(os.path.dirname(__file__), 'users.json')
    if not os.path.exists(users_file):
        with open(users_file, 'w') as f:
            json.dump({}, f)
        print("Created users.json file")

# Initialize the users file
initialize_users_file()

from utils import is_current_session_valid
from utils import mongo_in_use, mongo_health, ensure_user_indexes

if mongo_in_use():
    ensure_user_indexes()
    ok, msg = mongo_health()
    if not ok:
        st.error(f"MongoDB connection error: {msg}")
        st.stop()

# Check session validity
if st.session_state.authenticated and not is_current_session_valid():
    st.session_state.authenticated = False
    st.session_state.current_user = None

# Auto-redirect based on authentication status
if not st.session_state.authenticated:
    st.switch_page("pages/1_Landing.py")
else:
    st.switch_page("pages/4_Calculator.py")
