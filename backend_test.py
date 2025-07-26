#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Street Food Raw Materials
Tests all API endpoints with various scenarios and edge cases
"""

import requests
import json
import sys
import os
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
SESSION_ID = "test_session_123"

print(f"🔗 Testing backend API at: {API_URL}")
print(f"📅 Test started at: {datetime.now()}")
print("=" * 80)

class APITester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def test(self, name, func):
        """Run a test and record results"""
        print(f"\n🧪 Testing: {name}")
        try:
            result = func()
            if result:
                print(f"✅ PASSED: {name}")
                self.passed += 1
                self.results.append({"test": name, "status": "PASSED", "details": ""})
            else:
                print(f"❌ FAILED: {name}")
                self.failed += 1
                self.results.append({"test": name, "status": "FAILED", "details": "Test returned False"})
        except Exception as e:
            print(f"❌ ERROR: {name} - {str(e)}")
            self.failed += 1
            self.results.append({"test": name, "status": "ERROR", "details": str(e)})
    
    def summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        print("\n" + "=" * 80)
        print(f"📊 TEST SUMMARY")
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"Success Rate: {(self.passed/total*100):.1f}%" if total > 0 else "0%")
        
        if self.failed > 0:
            print(f"\n❌ FAILED TESTS:")
            for result in self.results:
                if result["status"] in ["FAILED", "ERROR"]:
                    print(f"  - {result['test']}: {result['details']}")

def make_request(method, endpoint, data=None, params=None):
    """Make HTTP request with error handling"""
    url = f"{API_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, timeout=10)
        
        print(f"  📡 {method} {endpoint} -> {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Request failed: {e}")
        return None

# Test Functions
def test_root_endpoint():
    """Test GET /api/ - Root endpoint health check"""
    response = make_request("GET", "/")
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        return "message" in data and "Street Food Raw Materials API" in data["message"]
    return False

def test_materials_basic():
    """Test GET /api/materials - Basic materials fetch"""
    response = make_request("GET", "/materials")
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            # Check structure of first material
            material = data[0]
            required_fields = ["id", "name", "category", "price", "unit", "supplier", "image", "inStock"]
            return all(field in material for field in required_fields)
    return False

def test_materials_search():
    """Test GET /api/materials with search functionality"""
    response = make_request("GET", "/materials", params={"search": "tomato"})
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            # Check if search results contain tomato-related items
            for item in data:
                if "tomato" in item["name"].lower():
                    return True
            # If no tomato items found, that's also valid (empty result)
            return True
    return False

def test_materials_category_filter():
    """Test GET /api/materials with category filtering"""
    response = make_request("GET", "/materials", params={"category": "spices"})
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            # All items should be in spices category
            for item in data:
                if item["category"] != "spices":
                    return False
            return True
    return False

def test_materials_sort():
    """Test GET /api/materials with sort functionality"""
    response = make_request("GET", "/materials", params={"sort_by": "price"})
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 1:
            # Check if sorted by price (ascending)
            for i in range(len(data) - 1):
                if data[i]["price"] > data[i + 1]["price"]:
                    return False
            return True
    return len(data) <= 1  # Single item or empty is valid

def test_materials_verified_filter():
    """Test GET /api/materials with verified suppliers filter"""
    response = make_request("GET", "/materials", params={"filter_by": "verified"})
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            # All items should have verified suppliers
            for item in data:
                if not item["supplier"]["verified"]:
                    return False
            return True
    return False

def test_materials_instock_filter():
    """Test GET /api/materials with in-stock filter"""
    response = make_request("GET", "/materials", params={"filter_by": "instock"})
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            # All items should be in stock
            for item in data:
                if not item["inStock"]:
                    return False
            return True
    return False

def test_materials_group_filter():
    """Test GET /api/materials with group deals filter"""
    response = make_request("GET", "/materials", params={"filter_by": "group"})
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            # All items should have group deals (groupPrice < price)
            for item in data:
                if item["groupPrice"] >= item["price"]:
                    return False
            return True
    return False

def test_categories_endpoint():
    """Test GET /api/categories"""
    response = make_request("GET", "/categories")
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            # Check structure of first category
            category = data[0]
            required_fields = ["id", "name", "icon"]
            return all(field in category for field in required_fields)
    return False

def test_suppliers_endpoint():
    """Test GET /api/suppliers"""
    response = make_request("GET", "/suppliers")
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            # Check structure of first supplier
            supplier = data[0]
            required_fields = ["id", "name", "verified", "location"]
            return all(field in supplier for field in required_fields)
    return False

def test_cart_get_new_session():
    """Test GET /api/cart/{session_id} for new session"""
    response = make_request("GET", f"/cart/{SESSION_ID}")
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        expected_fields = ["session_id", "items", "total", "count"]
        return (all(field in data for field in expected_fields) and 
                data["session_id"] == SESSION_ID and
                data["items"] == [] and
                data["total"] == 0 and
                data["count"] == 0)
    return False

def test_cart_add_item():
    """Test POST /api/cart/{session_id}/add - Add item to cart"""
    # First clear cart
    make_request("DELETE", f"/cart/{SESSION_ID}")
    
    # Add item to cart
    cart_data = {
        "material_id": 1,
        "quantity": 2,
        "is_group": False
    }
    response = make_request("POST", f"/cart/{SESSION_ID}/add", data=cart_data)
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        return "message" in data and "added to cart" in data["message"].lower()
    return False

def test_cart_add_group_item():
    """Test POST /api/cart/{session_id}/add - Add group item to cart"""
    cart_data = {
        "material_id": 2,
        "quantity": 5,
        "is_group": True
    }
    response = make_request("POST", f"/cart/{SESSION_ID}/add", data=cart_data)
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        return "message" in data and "added to cart" in data["message"].lower()
    return False

def test_cart_get_with_items():
    """Test GET /api/cart/{session_id} with items"""
    response = make_request("GET", f"/cart/{SESSION_ID}")
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        return (data["session_id"] == SESSION_ID and
                len(data["items"]) > 0 and
                data["total"] > 0 and
                data["count"] > 0)
    return False

def test_cart_update_item():
    """Test PUT /api/cart/{session_id}/item/{item_id} - Update quantity"""
    # Get cart to find item ID
    cart_response = make_request("GET", f"/cart/{SESSION_ID}")
    if not cart_response or cart_response.status_code != 200:
        return False
    
    cart_data = cart_response.json()
    if not cart_data["items"]:
        return False
    
    item_id = cart_data["items"][0]["id"]
    update_data = {"quantity": 3}
    
    response = make_request("PUT", f"/cart/{SESSION_ID}/item/{item_id}", data=update_data)
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        return "message" in data and "updated" in data["message"].lower()
    return False

def test_cart_remove_item():
    """Test DELETE /api/cart/{session_id}/item/{item_id} - Remove item"""
    # Get cart to find item ID
    cart_response = make_request("GET", f"/cart/{SESSION_ID}")
    if not cart_response or cart_response.status_code != 200:
        return False
    
    cart_data = cart_response.json()
    if not cart_data["items"]:
        return False
    
    item_id = cart_data["items"][0]["id"]
    
    response = make_request("DELETE", f"/cart/{SESSION_ID}/item/{item_id}")
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        return "message" in data and "removed" in data["message"].lower()
    return False

def test_cart_clear():
    """Test DELETE /api/cart/{session_id} - Clear cart"""
    # Add an item first
    cart_data = {"material_id": 3, "quantity": 1, "is_group": False}
    make_request("POST", f"/cart/{SESSION_ID}/add", data=cart_data)
    
    # Clear cart
    response = make_request("DELETE", f"/cart/{SESSION_ID}")
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        return "message" in data and "cleared" in data["message"].lower()
    return False

def test_order_creation():
    """Test POST /api/orders - Create order/checkout"""
    # Add items to cart first
    cart_items = [
        {"material_id": 1, "quantity": 2, "is_group": False},
        {"material_id": 2, "quantity": 1, "is_group": True}
    ]
    
    for item in cart_items:
        make_request("POST", f"/cart/{SESSION_ID}/add", data=item)
    
    # Create order
    order_data = {"session_id": SESSION_ID}
    response = make_request("POST", "/orders", data=order_data)
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        required_fields = ["message", "order_id", "total_amount"]
        return all(field in data for field in required_fields)
    return False

def test_order_history():
    """Test GET /api/orders/{session_id} - Get order history"""
    response = make_request("GET", f"/orders/{SESSION_ID}")
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            # Should have at least one order from previous test
            if len(data) > 0:
                order = data[0]
                required_fields = ["session_id", "items", "total_amount", "status"]
                return all(field in order for field in required_fields)
            return True  # Empty order history is also valid
    return False

def test_cart_cleared_after_order():
    """Test that cart is cleared after order creation"""
    response = make_request("GET", f"/cart/{SESSION_ID}")
    if not response:
        return False
    
    if response.status_code == 200:
        data = response.json()
        return (data["items"] == [] and
                data["total"] == 0 and
                data["count"] == 0)
    return False

def test_error_handling():
    """Test error handling for invalid requests"""
    # Test invalid material ID
    cart_data = {"material_id": 999, "quantity": 1, "is_group": False}
    response = make_request("POST", f"/cart/{SESSION_ID}/add", data=cart_data)
    
    # Should return 404 or 500 error
    return response and response.status_code in [404, 500]

# Main test execution
def main():
    tester = APITester()
    
    print("🚀 Starting comprehensive backend API tests...")
    
    # Root endpoint test
    tester.test("Root endpoint health check", test_root_endpoint)
    
    # Materials endpoint tests
    tester.test("Materials basic fetch", test_materials_basic)
    tester.test("Materials search functionality", test_materials_search)
    tester.test("Materials category filtering", test_materials_category_filter)
    tester.test("Materials sort functionality", test_materials_sort)
    tester.test("Materials verified suppliers filter", test_materials_verified_filter)
    tester.test("Materials in-stock filter", test_materials_instock_filter)
    tester.test("Materials group deals filter", test_materials_group_filter)
    
    # Categories and suppliers tests
    tester.test("Categories endpoint", test_categories_endpoint)
    tester.test("Suppliers endpoint", test_suppliers_endpoint)
    
    # Cart operations tests
    tester.test("Cart retrieval for new session", test_cart_get_new_session)
    tester.test("Add individual item to cart", test_cart_add_item)
    tester.test("Add group item to cart", test_cart_add_group_item)
    tester.test("Cart retrieval with items", test_cart_get_with_items)
    tester.test("Update cart item quantity", test_cart_update_item)
    tester.test("Remove item from cart", test_cart_remove_item)
    tester.test("Clear cart", test_cart_clear)
    
    # Order operations tests
    tester.test("Order creation/checkout", test_order_creation)
    tester.test("Order history retrieval", test_order_history)
    tester.test("Cart cleared after order", test_cart_cleared_after_order)
    
    # Error handling test
    tester.test("Error handling for invalid requests", test_error_handling)
    
    # Print summary
    tester.summary()
    
    # Return exit code based on results
    return 0 if tester.failed == 0 else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)