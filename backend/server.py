from fastapi import FastAPI, APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Import models and database functions after loading env vars
from models import (
    RawMaterial, Supplier, Category, Cart, CartItem, Order,
    AddToCartRequest, UpdateCartItemRequest, MaterialsQuery, CheckoutRequest
)
from database import (
    initialize_database, seed_database, get_all_suppliers, get_all_categories, 
    get_materials_with_suppliers, suppliers_collection, categories_collection,
    carts_collection, orders_collection, materials_collection
)

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Seed database on startup
@app.on_event("startup")
async def startup_event():
    try:
        # Initialize database connection
        initialize_database()
        result = await seed_database()
        print(f"Database initialization: {result}")
    except Exception as e:
        print(f"Error seeding database: {e}")

# Root endpoint
@api_router.get("/")
async def root():
    return {"message": "Street Food Raw Materials API"}

# Materials endpoints
@api_router.get("/materials", response_model=List[dict])
async def get_materials(
    search: Optional[str] = Query(None, description="Search term for materials or suppliers"),
    category: Optional[str] = Query("all", description="Filter by category"),
    sort_by: Optional[str] = Query("name", description="Sort by: name, price, supplier"),
    filter_by: Optional[str] = Query("all", description="Filter by: all, verified, instock, group"),
    limit: Optional[int] = Query(50, description="Limit number of results"),
    offset: Optional[int] = Query(0, description="Offset for pagination")
):
    try:
        query_params = {
            "search": search,
            "category": category,
            "sort_by": sort_by,
            "filter_by": filter_by,
            "limit": limit,
            "offset": offset
        }
        
        materials = await get_materials_with_suppliers(query_params)
        
        # Format the response to match frontend expectations
        formatted_materials = []
        for material in materials:
            formatted_material = {
                "id": material["id"],
                "name": material["name"],
                "category": material["category"],
                "price": material["price"],
                "unit": material["unit"],
                "supplier": {
                    "id": material["supplier"]["id"],
                    "name": material["supplier"]["name"],
                    "verified": material["supplier"]["verified"],
                    "location": material["supplier"]["location"]
                },
                "image": material["image"],
                "inStock": material["inStock"],
                "description": material["description"],
                "groupPrice": material["groupPrice"],
                "minGroupQuantity": material["minGroupQuantity"]
            }
            formatted_materials.append(formatted_material)
        
        return formatted_materials
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching materials: {str(e)}")

@api_router.get("/categories", response_model=List[Category])
async def get_categories():
    try:
        categories = await get_all_categories()
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching categories: {str(e)}")

@api_router.get("/suppliers", response_model=List[Supplier])
async def get_suppliers():
    try:
        suppliers = await get_all_suppliers()
        return suppliers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching suppliers: {str(e)}")

# Cart endpoints
@api_router.get("/cart/{session_id}")
async def get_cart(session_id: str):
    try:
        cart = await carts_collection.find_one({"session_id": session_id})
        if not cart:
            return {"session_id": session_id, "items": [], "total": 0, "count": 0}
        
        total = sum(item["price"] * item["quantity"] for item in cart["items"])
        count = sum(item["quantity"] for item in cart["items"])
        
        return {
            "session_id": session_id,
            "items": cart["items"],
            "total": total,
            "count": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching cart: {str(e)}")

@api_router.post("/cart/{session_id}/add")
async def add_to_cart(session_id: str, request: AddToCartRequest):
    try:
        # Get material details
        material = await materials_collection.find_one({"id": request.material_id})
        if not material:
            raise HTTPException(status_code=404, detail="Material not found")
        
        # Get supplier details
        supplier = await suppliers_collection.find_one({"id": material["supplier_id"]})
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        
        # Create cart item
        price = material["groupPrice"] if request.is_group else material["price"]
        cart_item = {
            "id": len(await carts_collection.find_one({"session_id": session_id}) or {"items": []}.get("items", [])) + 1,
            "material_id": material["id"],
            "material_name": material["name"],
            "quantity": request.quantity,
            "price": price,
            "unit": material["unit"],
            "is_group": request.is_group,
            "supplier_name": supplier["name"],
            "image": material["image"]
        }
        
        # Update or create cart
        existing_cart = await carts_collection.find_one({"session_id": session_id})
        
        if existing_cart:
            # Check if item already exists with same group status
            item_exists = False
            for item in existing_cart["items"]:
                if item["material_id"] == request.material_id and item["is_group"] == request.is_group:
                    item["quantity"] += request.quantity
                    item_exists = True
                    break
            
            if not item_exists:
                existing_cart["items"].append(cart_item)
            
            existing_cart["updated_at"] = datetime.utcnow()
            await carts_collection.replace_one({"session_id": session_id}, existing_cart)
        else:
            new_cart = {
                "session_id": session_id,
                "items": [cart_item],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            await carts_collection.insert_one(new_cart)
        
        return {"message": "Item added to cart successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding to cart: {str(e)}")

@api_router.put("/cart/{session_id}/item/{item_id}")
async def update_cart_item(session_id: str, item_id: int, request: UpdateCartItemRequest):
    try:
        cart = await carts_collection.find_one({"session_id": session_id})
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        
        # Update item quantity
        item_found = False
        for item in cart["items"]:
            if item["id"] == item_id:
                if request.quantity <= 0:
                    cart["items"].remove(item)
                else:
                    item["quantity"] = request.quantity
                item_found = True
                break
        
        if not item_found:
            raise HTTPException(status_code=404, detail="Item not found in cart")
        
        cart["updated_at"] = datetime.utcnow()
        await carts_collection.replace_one({"session_id": session_id}, cart)
        
        return {"message": "Cart item updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating cart item: {str(e)}")

@api_router.delete("/cart/{session_id}/item/{item_id}")
async def remove_from_cart(session_id: str, item_id: int):
    try:
        cart = await carts_collection.find_one({"session_id": session_id})
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        
        # Remove item
        cart["items"] = [item for item in cart["items"] if item["id"] != item_id]
        cart["updated_at"] = datetime.utcnow()
        
        await carts_collection.replace_one({"session_id": session_id}, cart)
        
        return {"message": "Item removed from cart successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error removing from cart: {str(e)}")

@api_router.delete("/cart/{session_id}")
async def clear_cart(session_id: str):
    try:
        await carts_collection.delete_one({"session_id": session_id})
        return {"message": "Cart cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing cart: {str(e)}")

# Order endpoints
@api_router.post("/orders")
async def create_order(request: CheckoutRequest):
    try:
        # Get cart
        cart = await carts_collection.find_one({"session_id": request.session_id})
        if not cart or not cart["items"]:
            raise HTTPException(status_code=400, detail="Cart is empty")
        
        # Create order items
        order_items = []
        total_amount = 0
        
        for cart_item in cart["items"]:
            item_total = cart_item["price"] * cart_item["quantity"]
            order_item = {
                "material_id": cart_item["material_id"],
                "material_name": cart_item["material_name"],
                "quantity": cart_item["quantity"],
                "price": cart_item["price"],
                "unit": cart_item["unit"],
                "is_group": cart_item["is_group"],
                "supplier_name": cart_item["supplier_name"],
                "total": item_total
            }
            order_items.append(order_item)
            total_amount += item_total
        
        # Create order
        order = {
            "session_id": request.session_id,
            "items": order_items,
            "total_amount": total_amount,
            "status": "confirmed",
            "created_at": datetime.utcnow()
        }
        
        result = await orders_collection.insert_one(order)
        order["id"] = str(result.inserted_id)
        
        # Clear cart after successful order
        await carts_collection.delete_one({"session_id": request.session_id})
        
        return {
            "message": "Order placed successfully",
            "order_id": order["id"],
            "total_amount": total_amount
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")

@api_router.get("/orders/{session_id}")
async def get_orders(session_id: str):
    try:
        orders = await orders_collection.find({"session_id": session_id}).to_list(100)
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {str(e)}")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()