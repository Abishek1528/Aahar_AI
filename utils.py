import json
import os
import bcrypt
import re
import time
from datetime import datetime, timedelta
import secrets
import hashlib

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

# Password hashing functions
def hash_password(password):
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed_password):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Password strength validation
def validate_password_strength(password):
    """Validate password strength requirements"""
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one digit")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)")
    
    return errors

# Input sanitization
def sanitize_input(text):
    """Sanitize user input to prevent injection attacks"""
    if not isinstance(text, str):
        return ""
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>&"\'/]', '', text)
    # Limit length
    return sanitized[:100]

# Email validation
def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Phone number validation
def validate_phone(phone):
    """Validate phone number format (10 digits)"""
    pattern = r'^\d{10}$'
    return re.match(pattern, phone) is not None

# Session management with timeout
def create_session_token():
    """Create a secure session token"""
    return secrets.token_urlsafe(32)

def is_session_valid(session_start_time, timeout_minutes=30):
    """Check if session is still valid"""
    if not session_start_time:
        return False
    session_age = datetime.now() - session_start_time
    return session_age < timedelta(minutes=timeout_minutes)

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
def user_exists(identifier):
    users = load_users()
    # Check by email
    if identifier in users:
        return True
    # Check by phone number
    for user_data in users.values():
        if user_data.get('contact') == identifier:
            return True
    return False

# Create new user with enhanced security
def create_user(name, age, contact, email, password):
    users = load_users()
    
    # Sanitize inputs
    name = sanitize_input(name)
    contact = sanitize_input(contact)
    email = sanitize_input(email)
    
    # Hash password
    hashed_password = hash_password(password)
    
    # Create session token
    session_token = create_session_token()
    
    users[email] = {
        "name": name,
        "age": age,
        "contact": contact,
        "email": email,
        "password": hashed_password,
        "session_token": session_token,
        "created_at": datetime.now().isoformat(),
        "last_login": None
    }
    save_users(users)
    return True

# Validate login credentials with enhanced security
def validate_login(identifier, password):
    users = load_users()
    
    # Sanitize inputs
    identifier = sanitize_input(identifier)
    
    # Check if user exists with email
    if identifier in users:
        user = users[identifier]
        if verify_password(password, user["password"]):
            # Update last login time
            user["last_login"] = datetime.now().isoformat()
            save_users(users)
            return user
    
    # Also check by phone number
    for email, user in users.items():
        if user.get("contact") == identifier and verify_password(password, user["password"]):
            # Update last login time
            user["last_login"] = datetime.now().isoformat()
            save_users(users)
            return user
    
    return None

# Login function with enhanced security
def login_user(identifier, password):
    user = validate_login(identifier, password)
    if user:
        import streamlit as st
        st.session_state.authenticated = True
        st.session_state.current_user = user
        st.session_state.login_time = datetime.now()
        st.session_state.session_token = user.get('session_token', create_session_token())
        return True, "Login successful"
    return False, "Invalid credentials"

# Logout function
def logout_user():
    import streamlit as st
    st.session_state.authenticated = False
    st.session_state.current_user = None
    st.session_state.login_time = None
    st.session_state.session_token = None

# Enhanced signup function with validation
def signup_user(name, age, contact, email, password):
    # Input validation
    errors = []
    
    # Name validation
    if not name or len(name.strip()) < 2:
        errors.append("Name must be at least 2 characters long")
    
    # Age validation
    if not isinstance(age, int) or age < 13 or age > 120:
        errors.append("Age must be between 13 and 120")
    
    # Contact validation
    contact = contact.replace('-', '').replace(' ', '')
    if not validate_phone(contact):
        errors.append("Phone number must be 10 digits")
    
    # Email validation
    if not validate_email(email):
        errors.append("Invalid email format")
    
    # Password validation
    password_errors = validate_password_strength(password)
    errors.extend(password_errors)
    
    # Check if user already exists
    if user_exists(email):
        errors.append("Email already exists")
    
    if user_exists(contact):
        errors.append("Phone number already exists")
    
    # Return errors if any
    if errors:
        return False, "; ".join(errors)
    
    # Create user if all validations pass
    success = create_user(name.strip(), age, contact, email.lower(), password)
    if success:
        return True, "Account created successfully. You can now login."
    return False, "Failed to create account"

# Password recovery functions
def generate_recovery_token():
    """Generate a secure password recovery token"""
    return secrets.token_urlsafe(32)

def initiate_password_reset(identifier):
    """Initiate password reset process"""
    users = load_users()
    user_found = False
    
    # Find user by email or phone
    for email, user_data in users.items():
        if email == identifier or user_data.get('contact') == identifier:
            # Generate recovery token
            recovery_token = generate_recovery_token()
            user_data['recovery_token'] = recovery_token
            user_data['recovery_expires'] = (datetime.now() + timedelta(hours=1)).isoformat()
            user_found = True
            save_users(users)
            return True, recovery_token
    
    if not user_found:
        return False, "User not found"

def validate_recovery_token(identifier, token):
    """Validate recovery token"""
    users = load_users()
    
    for email, user_data in users.items():
        if (email == identifier or user_data.get('contact') == identifier) and \
           user_data.get('recovery_token') == token:
            
            # Check if token is expired
            expires_str = user_data.get('recovery_expires')
            if expires_str:
                expires_time = datetime.fromisoformat(expires_str)
                if datetime.now() < expires_time:
                    return True, email
            return False, "Token expired"
    
    return False, "Invalid token"

def reset_password(identifier, token, new_password):
    """Reset user password"""
    # Validate token
    is_valid, email = validate_recovery_token(identifier, token)
    if not is_valid:
        return False, email  # email contains error message in this case
    
    # Validate new password
    password_errors = validate_password_strength(new_password)
    if password_errors:
        return False, "; ".join(password_errors)
    
    # Update password
    users = load_users()
    if email in users:
        users[email]['password'] = hash_password(new_password)
        # Clear recovery token
        users[email].pop('recovery_token', None)
        users[email].pop('recovery_expires', None)
        save_users(users)
        return True, "Password reset successfully"
    
    return False, "User not found"

# Session validation
def is_current_session_valid():
    """Check if current session is still valid"""
    import streamlit as st
    
    if not st.session_state.get('authenticated', False):
        return False
    
    login_time = st.session_state.get('login_time')
    if login_time and not is_session_valid(login_time, timeout_minutes=30):
        # Session expired
        logout_user()
        return False
    
    return True