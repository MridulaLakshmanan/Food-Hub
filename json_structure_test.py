#!/usr/bin/env python3
"""
Test to verify the exact JSON structure of the order history response
"""

import requests
import json
import sys
from datetime import datetime

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading backend URL: {e}")
        return None

BASE_URL = get_backend_url()
API_URL = f"{BASE_URL}/api"
SESSION_ID = "json_structure_test_789"

def make_request(method, endpoint, data=None):
    """Make HTTP request with error handling"""
    url = f"{API_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, timeout=10)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def main():
    print("🔍 Testing JSON structure of order history response...")
    
    # Clear cart and add items
    make_request("DELETE", f"/cart/{SESSION_ID}")
    
    # Add items to cart
    cart_items = [
        {"material_id": 1, "quantity": 2, "is_group": False},
        {"material_id": 2, "quantity": 1, "is_group": True}
    ]
    
    for item in cart_items:
        make_request("POST", f"/cart/{SESSION_ID}/add", data=item)
    
    # Create order
    make_request("POST", "/orders", data={"session_id": SESSION_ID})
    
    # Get order history
    response = make_request("GET", f"/orders/{SESSION_ID}")
    
    if response and response.status_code == 200:
        print("✅ Order history retrieved successfully")
        
        # Pretty print the JSON response
        try:
            data = response.json()
            print("\n📋 JSON Response Structure:")
            print(json.dumps(data, indent=2, default=str))
            
            # Verify it's valid JSON by parsing it again
            json.dumps(data)
            print("\n✅ Response is valid, serializable JSON")
            
            # Check for any remaining ObjectId references
            response_text = response.text
            if "ObjectId" in response_text:
                print("❌ Found ObjectId references in response text")
                return 1
            else:
                print("✅ No ObjectId references found in response")
                
        except Exception as e:
            print(f"❌ JSON parsing error: {e}")
            return 1
    else:
        print(f"❌ Failed to get order history: {response.status_code if response else 'No response'}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)