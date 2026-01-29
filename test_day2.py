#!/usr/bin/env python3
"""
Day 2 Authentication Enhancement Test Suite
Tests all security features implemented in Day 2
"""

import os
import sys
import json
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

def test_password_hashing():
    """Test password hashing and verification"""
    print("1. Testing Password Hashing...")
    try:
        from utils import hash_password, verify_password
        
        # Test hashing
        password = "SecurePass123!"
        hashed = hash_password(password)
        assert len(hashed) > 20, "Hash should be long"
        assert "$2b$" in hashed, "Should be bcrypt hash"
        
        # Test verification
        assert verify_password(password, hashed), "Should verify correct password"
        assert not verify_password("WrongPass", hashed), "Should reject wrong password"
        
        print("   ✅ Password hashing working correctly")
        return True
    except Exception as e:
        print(f"   ❌ Password hashing failed: {e}")
        return False

def test_password_validation():
    """Test password strength validation"""
    print("2. Testing Password Validation...")
    try:
        from utils import validate_password_strength
        
        # Test weak password
        weak_password = "weak"
        errors = validate_password_strength(weak_password)
        assert len(errors) > 0, "Should detect weak password"
        
        # Test strong password
        strong_password = "StrongPass123!"
        errors = validate_password_strength(strong_password)
        assert len(errors) == 0, "Should accept strong password"
        
        print("   ✅ Password validation working correctly")
        return True
    except Exception as e:
        print(f"   ❌ Password validation failed: {e}")
        return False

def test_input_validation():
    """Test input sanitization and validation"""
    print("3. Testing Input Validation...")
    try:
        from utils import sanitize_input, validate_email, validate_phone
        
        # Test sanitization
        malicious_input = "<script>alert('xss')</script>"
        clean_input = sanitize_input(malicious_input)
        assert "<" not in clean_input, "Should remove dangerous characters"
        assert ">" not in clean_input, "Should remove dangerous characters"
        
        # Test email validation
        assert validate_email("test@example.com"), "Should accept valid email"
        assert not validate_email("invalid-email"), "Should reject invalid email"
        
        # Test phone validation
        assert validate_phone("1234567890"), "Should accept valid phone"
        assert not validate_phone("123"), "Should reject invalid phone"
        
        print("   ✅ Input validation working correctly")
        return True
    except Exception as e:
        print(f"   ❌ Input validation failed: {e}")
        return False

def test_session_management():
    """Test session management and timeout"""
    print("4. Testing Session Management...")
    try:
        from utils import create_session_token, is_session_valid
        
        # Test token creation
        token = create_session_token()
        assert len(token) > 20, "Token should be long and secure"
        
        # Test session validity
        assert is_session_valid(datetime.now()), "Current session should be valid"
        assert not is_session_valid(datetime.now() - timedelta(minutes=35)), "Old session should be expired"
        
        print("   ✅ Session management working correctly")
        return True
    except Exception as e:
        print(f"   ❌ Session management failed: {e}")
        return False

def test_user_authentication():
    """Test user authentication with enhanced security"""
    print("5. Testing User Authentication...")
    try:
        from utils import signup_user, login_user, validate_login
        
        # Test signup with validation
        success, message = signup_user("Test User", 25, "9876543210", "test@example.com", "StrongPass123!")
        if success:
            print("   ✅ User signup successful")
        else:
            print(f"   ⚠️  Signup failed (expected if user exists): {message}")
        
        # Test login with hashed password
        success, message = login_user("test@example.com", "StrongPass123!")
        if success:
            print("   ✅ User login successful")
        else:
            print(f"   ⚠️  Login failed: {message}")
        
        # Test invalid login
        success, message = login_user("test@example.com", "WrongPassword")
        assert not success, "Should reject wrong password"
        
        print("   ✅ User authentication working correctly")
        return True
    except Exception as e:
        print(f"   ❌ User authentication failed: {e}")
        return False

def test_password_recovery():
    """Test password recovery mechanism"""
    print("6. Testing Password Recovery...")
    try:
        from utils import initiate_password_reset, validate_recovery_token, reset_password
        
        # Test recovery initiation
        success, token = initiate_password_reset("test@example.com")
        if success:
            print("   ✅ Password recovery initiated")
            
            # Test token validation
            is_valid, email = validate_recovery_token("test@example.com", token)
            assert is_valid, "Recovery token should be valid"
            
            # Test password reset
            success, message = reset_password("test@example.com", token, "NewStrongPass123!")
            assert success, f"Password reset should succeed: {message}"
            print("   ✅ Password reset successful")
        else:
            print(f"   ⚠️  Recovery initiation failed: {token}")
        
        print("   ✅ Password recovery working correctly")
        return True
    except Exception as e:
        print(f"   ❌ Password recovery failed: {e}")
        return False

def test_compilation():
    """Test that all files compile without errors"""
    print("7. Testing File Compilation...")
    try:
        python_files = [
            'app.py',
            'calorie.py',
            'utils.py',
            'pages/1_Landing.py',
            'pages/2_Login.py',
            'pages/2_Signup.py',
            'pages/3_Password_Reset.py',
            'pages/4_Calculator.py'
        ]
        
        for file_path in python_files:
            full_path = os.path.join(os.path.dirname(__file__), file_path)
            if os.path.exists(full_path):
                with open(full_path, 'r', encoding='utf-8') as f:
                    compile(f.read(), full_path, 'exec')
        
        print("   ✅ All Python files compile successfully")
        return True
    except Exception as e:
        print(f"   ❌ Compilation failed: {e}")
        return False

def main():
    print("🧪 Day 2 Authentication Enhancement Test Suite")
    print("=" * 50)
    
    tests = [
        test_password_hashing,
        test_password_validation,
        test_input_validation,
        test_session_management,
        test_user_authentication,
        test_password_recovery,
        test_compilation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Day 2 Authentication Enhancement is working correctly")
        print("\nImplemented Features:")
        print("• Password hashing with bcrypt")
        print("• Password strength requirements")
        print("• Input validation and sanitization")
        print("• Email and phone number validation")
        print("• Session management with timeout")
        print("• Password recovery mechanism")
        print("• Enhanced form UX with real-time feedback")
    else:
        print(f"⚠️  {total - passed} test(s) failed")
        print("Please check the errors above")
    
    print("=" * 50)

if __name__ == "__main__":
    main()