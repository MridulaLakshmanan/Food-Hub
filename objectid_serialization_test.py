#!/usr/bin/env python3
"""
Focused test for MongoDB ObjectId serialization issue in order history endpoint
Tests the complete cart-to-order workflow and verifies proper JSON serialization
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
if not BASE_URL:
    print("❌ Could not get backend URL from frontend/.env")
    sys.exit(1)

API_URL = f"{BASE_URL}/api"
SESSION_ID = "objectid_test_session_456"

print(f"🔗 Testing ObjectId serialization at: {API_URL}")
print(f"📅 Test started at: {datetime.now()}")
print("=" * 80)

def make_request(method, endpoint, data=None, params=None):
    """Make HTTP request with error handling"""
    url = f"{API_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, timeout=10)
        
        print(f"  📡 {method} {endpoint} -> {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Request failed: {e}")
        return None

def check_for_objectids(data, path=""):
    """
    Recursively check for any ObjectId instances in the response data
    Returns True if ObjectIds found, False if all are properly serialized
    """
    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            if str(type(value)) == "<class 'bson.objectid.ObjectId'>":
                print(f"  ❌ Found ObjectId at {current_path}: {value}")
                return True
            if check_for_objectids(value, current_path):
                return True
    elif isinstance(data, list):
        for i, item in enumerate(data):
            current_path = f"{path}[{i}]" if path else f"[{i}]"
            if str(type(item)) == "<class 'bson.objectid.ObjectId'>":
                print(f"  ❌ Found ObjectId at {current_path}: {item}")
                return True
            if check_for_objectids(item, current_path):
                return True
    return False

def test_complete_cart_to_order_flow():
    """Test the complete flow from cart operations to order history retrieval"""
    print("\n🧪 Testing Complete Cart-to-Order Flow with ObjectId Serialization")
    
    # Step 1: Clear any existing cart
    print("\n1️⃣ Clearing existing cart...")
    clear_response = make_request("DELETE", f"/cart/{SESSION_ID}")
    if not clear_response or clear_response.status_code != 200:
        print("  ⚠️ Cart clear failed, but continuing...")
    
    # Step 2: Add multiple items to cart
    print("\n2️⃣ Adding items to cart...")
    cart_items = [
        {"material_id": 1, "quantity": 2, "is_group": False},
        {"material_id": 2, "quantity": 3, "is_group": True},
        {"material_id": 3, "quantity": 1, "is_group": False}
    ]
    
    for i, item in enumerate(cart_items):
        response = make_request("POST", f"/cart/{SESSION_ID}/add", data=item)
        if not response or response.status_code != 200:
            print(f"  ❌ Failed to add item {i+1} to cart")
            return False
        print(f"  ✅ Added item {i+1} to cart")
    
    # Step 3: Verify cart contents
    print("\n3️⃣ Verifying cart contents...")
    cart_response = make_request("GET", f"/cart/{SESSION_ID}")
    if not cart_response or cart_response.status_code != 200:
        print("  ❌ Failed to retrieve cart")
        return False
    
    cart_data = cart_response.json()
    if len(cart_data["items"]) != len(cart_items):
        print(f"  ❌ Expected {len(cart_items)} items, got {len(cart_data['items'])}")
        return False
    print(f"  ✅ Cart contains {len(cart_data['items'])} items as expected")
    
    # Step 4: Create order (checkout)
    print("\n4️⃣ Creating order (checkout)...")
    order_data = {"session_id": SESSION_ID}
    order_response = make_request("POST", "/orders", data=order_data)
    if not order_response or order_response.status_code != 200:
        print("  ❌ Failed to create order")
        return False
    
    order_result = order_response.json()
    if "order_id" not in order_result:
        print("  ❌ Order creation response missing order_id")
        return False
    print(f"  ✅ Order created successfully with ID: {order_result['order_id']}")
    
    # Step 5: Retrieve order history and check for ObjectId serialization
    print("\n5️⃣ Retrieving order history and checking ObjectId serialization...")
    history_response = make_request("GET", f"/orders/{SESSION_ID}")
    if not history_response or history_response.status_code != 200:
        print(f"  ❌ Failed to retrieve order history: {history_response.status_code if history_response else 'No response'}")
        if history_response:
            print(f"  ❌ Response text: {history_response.text}")
        return False
    
    # Check if response is valid JSON
    try:
        history_data = history_response.json()
        print("  ✅ Response is valid JSON")
    except json.JSONDecodeError as e:
        print(f"  ❌ Response is not valid JSON: {e}")
        print(f"  ❌ Response text: {history_response.text}")
        return False
    
    # Check for ObjectIds in the response
    if check_for_objectids(history_data):
        print("  ❌ Found ObjectId instances in response - serialization failed")
        return False
    print("  ✅ No ObjectId instances found - serialization successful")
    
    # Step 6: Verify order structure
    print("\n6️⃣ Verifying order structure...")
    if not isinstance(history_data, list):
        print("  ❌ Order history should be a list")
        return False
    
    if len(history_data) == 0:
        print("  ❌ Order history is empty")
        return False
    
    order = history_data[0]  # Get the most recent order
    required_fields = ["id", "session_id", "items", "total_amount", "status", "created_at"]
    
    for field in required_fields:
        if field not in order:
            print(f"  ❌ Missing required field: {field}")
            return False
    
    # Verify all IDs are strings
    if not isinstance(order["id"], str):
        print(f"  ❌ Order ID is not a string: {type(order['id'])}")
        return False
    
    # Check items structure
    if not isinstance(order["items"], list) or len(order["items"]) == 0:
        print("  ❌ Order items should be a non-empty list")
        return False
    
    for i, item in enumerate(order["items"]):
        if "material_id" not in item:
            print(f"  ❌ Item {i} missing material_id")
            return False
    
    print(f"  ✅ Order structure is valid with {len(order['items'])} items")
    print(f"  ✅ Order ID is properly serialized as string: {order['id']}")
    
    # Step 7: Verify cart was cleared after order
    print("\n7️⃣ Verifying cart was cleared after order...")
    final_cart_response = make_request("GET", f"/cart/{SESSION_ID}")
    if not final_cart_response or final_cart_response.status_code != 200:
        print("  ❌ Failed to retrieve cart after order")
        return False
    
    final_cart_data = final_cart_response.json()
    if len(final_cart_data["items"]) != 0:
        print(f"  ❌ Cart should be empty after order, but has {len(final_cart_data['items'])} items")
        return False
    print("  ✅ Cart was properly cleared after order creation")
    
    return True

def main():
    """Main test execution"""
    print("🚀 Starting ObjectId serialization test...")
    
    success = test_complete_cart_to_order_flow()
    
    print("\n" + "=" * 80)
    if success:
        print("🎉 ALL TESTS PASSED - ObjectId serialization issue is FIXED!")
        print("✅ Order history endpoint now properly serializes all ObjectIds to strings")
        print("✅ Complete cart-to-order workflow is functional")
        return 0
    else:
        print("❌ TEST FAILED - ObjectId serialization issue still exists")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)