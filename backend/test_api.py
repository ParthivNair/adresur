#!/usr/bin/env python3
"""
Simple API test script for Adresur Backend
This script tests the main API endpoints to ensure they're working correctly.
"""

import requests
import json
import sys

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running.")
        return False

def test_register_user():
    """Test user registration"""
    print("🔍 Testing user registration...")
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123",
        "role": "user"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if response.status_code == 200:
            print("✅ User registration passed")
            return response.json()
        elif response.status_code == 400 and "already registered" in response.json().get("detail", ""):
            print("✅ User already exists (expected)")
            return None
        else:
            print(f"❌ User registration failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ User registration error: {e}")
        return None

def test_login_user():
    """Test user login"""
    print("🔍 Testing user login...")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ User login passed")
            return response.json().get("access_token")
        else:
            print(f"❌ User login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ User login error: {e}")
        return None

def test_protected_endpoint(token):
    """Test a protected endpoint"""
    print("🔍 Testing protected endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/cooks/", headers=headers)
        if response.status_code == 200:
            print("✅ Protected endpoint access passed")
            return True
        else:
            print(f"❌ Protected endpoint failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Protected endpoint error: {e}")
        return False

def test_api_docs():
    """Test API documentation endpoints"""
    print("🔍 Testing API documentation...")
    try:
        # Test Swagger docs
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ Swagger docs accessible")
        else:
            print(f"❌ Swagger docs failed: {response.status_code}")
        
        # Test ReDoc
        response = requests.get(f"{BASE_URL}/redoc")
        if response.status_code == 200:
            print("✅ ReDoc accessible")
            return True
        else:
            print(f"❌ ReDoc failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API docs error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Starting Adresur API Tests\n")
    
    # Test health check first
    if not test_health_check():
        print("\n❌ API is not running. Please start the server first.")
        sys.exit(1)
    
    print()
    
    # Test user registration
    test_register_user()
    print()
    
    # Test user login
    token = test_login_user()
    print()
    
    # Test protected endpoint if we have a token
    if token:
        test_protected_endpoint(token)
        print()
    
    # Test API documentation
    test_api_docs()
    
    print("\n🎉 API tests completed!")
    print(f"📚 Visit {BASE_URL}/docs for interactive API documentation")

if __name__ == "__main__":
    main() 