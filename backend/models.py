from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

# Base Models
class Supplier(BaseModel):
    id: int
    name: str
    verified: bool = False
    location: str

class Category(BaseModel):
    id: str
    name: str
    icon: str

class RawMaterial(BaseModel):
    id: int
    name: str
    category: str
    price: float
    unit: str
    supplier: Supplier
    image: str
    inStock: bool = True
    description: str
    groupPrice: float
    minGroupQuantity: int

# Database Models (for MongoDB operations)
class SupplierDB(BaseModel):
    id: int
    name: str
    verified: bool = False
    location: str

class CategoryDB(BaseModel):
    id: str
    name: str
    icon: str

class RawMaterialDB(BaseModel):
    id: int
    name: str
    category: str
    price: float
    unit: str
    supplier_id: int
    image: str
    inStock: bool = True
    description: str
    groupPrice: float
    minGroupQuantity: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Cart Models
class CartItem(BaseModel):
    id: int
    material_id: int
    material_name: str
    quantity: int
    price: float
    unit: str
    is_group: bool = False
    supplier_name: str
    image: str

class Cart(BaseModel):
    session_id: str
    items: List[CartItem] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Order Models
class OrderItem(BaseModel):
    material_id: int
    material_name: str
    quantity: int
    price: float
    unit: str
    is_group: bool = False
    supplier_name: str
    total: float

class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    items: List[OrderItem]
    total_amount: float
    status: str = "pending"  # pending, confirmed, shipped, delivered
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Request/Response Models
class AddToCartRequest(BaseModel):
    material_id: int
    quantity: int = 1
    is_group: bool = False

class UpdateCartItemRequest(BaseModel):
    quantity: int

class MaterialsQuery(BaseModel):
    search: Optional[str] = None
    category: Optional[str] = None
    sort_by: Optional[str] = "name"  # name, price, supplier
    filter_by: Optional[str] = "all"  # all, verified, instock, group
    limit: Optional[int] = 50
    offset: Optional[int] = 0

class CheckoutRequest(BaseModel):
    session_id: str