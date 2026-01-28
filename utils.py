import json
import os

# User data file path - relative to project root
# Handle both direct execution and execution from pages directory
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)
USER_DATA_FILE = os.path.join(root_dir, 'users.json')

# Ensure the file exists in the correct location
if not os.path.exists(USER_DATA_FILE):
    # Try alternative path (same directory as this file)
    alt_path = os.path.join(script_dir, 'users.json')
    if os.path.exists(alt_path):
        USER_DATA_FILE = alt_path
    else:
        # Create the file if it doesn't exist
        with open(USER_DATA_FILE, 'w') as f:
            json.dump({
                "admin@example.com": {
                    "name": "Admin User",
                    "age": 25,
                    "contact": "1234567890",
                    "email": "admin@example.com",
                    "password": "admin123"
                }
            }, f)

# Load user data from file
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

# Save user data to file
def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f)

# Check if user exists
def user_exists(username_or_phone):
    users = load_users()
    return username_or_phone in users

# Create new user
def create_user(name, age, contact, email, password):
    users = load_users()
    users[email] = {
        "name": name,
        "age": age,
        "contact": contact,
        "email": email,
        "password": password
    }
    save_users(users)
    return True

# Validate login credentials
def validate_login(username_or_phone, password):
    users = load_users()
    # Check if user exists with email or phone
    if username_or_phone in users:
        user = users[username_or_phone]
        if user["password"] == password:
            return user
    # Also check by phone number if email doesn't match
    for email, user in users.items():
        if user["contact"] == username_or_phone and user["password"] == password:
            return user
    return None

# Login function
def login_user(username_or_phone, password):
    user = validate_login(username_or_phone, password)
    if user:
        import streamlit as st
        st.session_state.authenticated = True
        st.session_state.current_user = user
        return True
    return False

# Logout function
def logout_user():
    import streamlit as st
    st.session_state.authenticated = False
    st.session_state.current_user = None

# Signup function
def signup_user(name, age, contact, email, password):
    if user_exists(email):
        return False, "Email already exists"
    if user_exists(contact):
        return False, "Phone number already exists"
    
    success = create_user(name, age, contact, email, password)
    if success:
        return True, "Account created successfully"
    return False, "Failed to create account"