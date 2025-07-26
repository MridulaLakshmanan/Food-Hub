from motor.motor_asyncio import AsyncIOMotorClient
from models import SupplierDB, CategoryDB, RawMaterialDB
import os

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Collections
suppliers_collection = db.suppliers
categories_collection = db.categories
materials_collection = db.raw_materials
carts_collection = db.carts
orders_collection = db.orders

async def seed_database():
    """Seed the database with initial data"""
    
    # Check if data already exists
    if await suppliers_collection.count_documents({}) > 0:
        return "Database already seeded"
    
    # Seed Suppliers
    suppliers_data = [
        {"id": 1, "name": "Fresh Farm Co.", "verified": True, "location": "Mumbai"},
        {"id": 2, "name": "Green Valley Suppliers", "verified": True, "location": "Delhi"},
        {"id": 3, "name": "Spice Master Ltd.", "verified": False, "location": "Chennai"},
        {"id": 4, "name": "Quality Foods Inc.", "verified": True, "location": "Bangalore"},
        {"id": 5, "name": "Local Market Hub", "verified": False, "location": "Pune"}
    ]
    await suppliers_collection.insert_many(suppliers_data)
    
    # Seed Categories
    categories_data = [
        {"id": "tomatoes", "name": "Tomatoes", "icon": "🍅"},
        {"id": "flour", "name": "Flour", "icon": "🌾"},
        {"id": "oil", "name": "Oil", "icon": "🫒"},
        {"id": "spices", "name": "Spices", "icon": "🌶️"},
        {"id": "onions", "name": "Onions", "icon": "🧅"},
        {"id": "rice", "name": "Rice", "icon": "🌾"},
        {"id": "vegetables", "name": "Vegetables", "icon": "🥬"},
        {"id": "meat", "name": "Meat", "icon": "🥩"}
    ]
    await categories_collection.insert_many(categories_data)
    
    # Seed Raw Materials
    materials_data = [
        {
            "id": 1, "name": "Fresh Tomatoes", "category": "tomatoes", "price": 45, "unit": "kg",
            "supplier_id": 1, "image": "https://images.unsplash.com/photo-1546470427-227527c9e1eb?w=400&h=300&fit=crop",
            "inStock": True, "description": "Fresh red tomatoes, perfect for street food preparation",
            "groupPrice": 38, "minGroupQuantity": 50
        },
        {
            "id": 2, "name": "Wheat Flour", "category": "flour", "price": 35, "unit": "kg",
            "supplier_id": 2, "image": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=300&fit=crop",
            "inStock": True, "description": "Premium quality wheat flour for breads and rotis",
            "groupPrice": 30, "minGroupQuantity": 100
        },
        {
            "id": 3, "name": "Sunflower Oil", "category": "oil", "price": 120, "unit": "liter",
            "supplier_id": 4, "image": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&h=300&fit=crop",
            "inStock": True, "description": "Pure sunflower oil for cooking and frying",
            "groupPrice": 110, "minGroupQuantity": 20
        },
        {
            "id": 4, "name": "Red Chili Powder", "category": "spices", "price": 180, "unit": "kg",
            "supplier_id": 3, "image": "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop",
            "inStock": False, "description": "Spicy red chili powder for authentic taste",
            "groupPrice": 160, "minGroupQuantity": 10
        },
        {
            "id": 5, "name": "Large Onions", "category": "onions", "price": 30, "unit": "kg",
            "supplier_id": 1, "image": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400&h=300&fit=crop",
            "inStock": True, "description": "Fresh large onions for cooking base",
            "groupPrice": 25, "minGroupQuantity": 100
        },
        {
            "id": 6, "name": "Basmati Rice", "category": "rice", "price": 85, "unit": "kg",
            "supplier_id": 2, "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop",
            "inStock": True, "description": "Premium basmati rice for biryanis and pulao",
            "groupPrice": 78, "minGroupQuantity": 50
        },
        {
            "id": 7, "name": "Turmeric Powder", "category": "spices", "price": 220, "unit": "kg",
            "supplier_id": 3, "image": "https://images.unsplash.com/photo-1615485500704-8e990f9900f7?w=400&h=300&fit=crop",
            "inStock": True, "description": "Pure turmeric powder for color and flavor",
            "groupPrice": 200, "minGroupQuantity": 5
        },
        {
            "id": 8, "name": "Green Vegetables Mix", "category": "vegetables", "price": 55, "unit": "kg",
            "supplier_id": 5, "image": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop",
            "inStock": True, "description": "Fresh mixed green vegetables",
            "groupPrice": 48, "minGroupQuantity": 30
        },
        {
            "id": 9, "name": "Chicken (Fresh)", "category": "meat", "price": 280, "unit": "kg",
            "supplier_id": 4, "image": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400&h=300&fit=crop",
            "inStock": True, "description": "Fresh chicken for non-veg preparations",
            "groupPrice": 260, "minGroupQuantity": 20
        },
        {
            "id": 10, "name": "Cumin Seeds", "category": "spices", "price": 350, "unit": "kg",
            "supplier_id": 3, "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop",
            "inStock": True, "description": "Aromatic cumin seeds for seasoning",
            "groupPrice": 320, "minGroupQuantity": 5
        }
    ]
    await materials_collection.insert_many(materials_data)
    
    return "Database seeded successfully"

async def get_supplier_by_id(supplier_id: int):
    """Get supplier by ID"""
    supplier = await suppliers_collection.find_one({"id": supplier_id})
    return supplier

async def get_all_suppliers():
    """Get all suppliers"""
    suppliers = await suppliers_collection.find().to_list(100)
    return suppliers

async def get_all_categories():
    """Get all categories"""
    categories = await categories_collection.find().to_list(100)
    return categories

async def get_materials_with_suppliers(query_params=None):
    """Get materials with their supplier information"""
    pipeline = []
    
    # Match stage for filtering
    match_conditions = {}
    
    if query_params:
        if query_params.get('category') and query_params['category'] != 'all':
            match_conditions['category'] = query_params['category']
        
        if query_params.get('filter_by'):
            if query_params['filter_by'] == 'instock':
                match_conditions['inStock'] = True
            elif query_params['filter_by'] == 'group':
                pipeline.append({
                    "$addFields": {
                        "hasGroupDeal": {"$lt": ["$groupPrice", "$price"]}
                    }
                })
                match_conditions['hasGroupDeal'] = True
        
        if query_params.get('search'):
            search_term = query_params['search']
            match_conditions['$or'] = [
                {"name": {"$regex": search_term, "$options": "i"}},
                {"description": {"$regex": search_term, "$options": "i"}}
            ]
    
    if match_conditions:
        pipeline.append({"$match": match_conditions})
    
    # Lookup suppliers
    pipeline.extend([
        {
            "$lookup": {
                "from": "suppliers",
                "localField": "supplier_id",
                "foreignField": "id",
                "as": "supplier"
            }
        },
        {
            "$unwind": "$supplier"
        }
    ])
    
    # Additional filtering based on supplier verification
    if query_params and query_params.get('filter_by') == 'verified':
        pipeline.append({"$match": {"supplier.verified": True}})
    
    # Sorting
    sort_field = "name"
    if query_params and query_params.get('sort_by'):
        if query_params['sort_by'] == 'price':
            sort_field = "price"
        elif query_params['sort_by'] == 'supplier':
            sort_field = "supplier.name"
    
    pipeline.append({"$sort": {sort_field: 1}})
    
    # Limit and offset
    if query_params:
        if query_params.get('offset'):
            pipeline.append({"$skip": query_params['offset']})
        if query_params.get('limit'):
            pipeline.append({"$limit": query_params['limit']})
    
    materials = await materials_collection.aggregate(pipeline).to_list(1000)
    return materials