// Mock data for raw materials browsing

export const categories = [
  { id: 'tomatoes', name: 'Tomatoes', icon: '🍅' },
  { id: 'flour', name: 'Flour', icon: '🌾' },
  { id: 'oil', name: 'Oil', icon: '🫒' },
  { id: 'spices', name: 'Spices', icon: '🌶️' },
  { id: 'onions', name: 'Onions', icon: '🧅' },
  { id: 'rice', name: 'Rice', icon: '🌾' },
  { id: 'vegetables', name: 'Vegetables', icon: '🥬' },
  { id: 'meat', name: 'Meat', icon: '🥩' }
];

export const suppliers = [
  { id: 1, name: 'Fresh Farm Co.', verified: true, location: 'Mumbai' },
  { id: 2, name: 'Green Valley Suppliers', verified: true, location: 'Delhi' },
  { id: 3, name: 'Spice Master Ltd.', verified: false, location: 'Chennai' },
  { id: 4, name: 'Quality Foods Inc.', verified: true, location: 'Bangalore' },
  { id: 5, name: 'Local Market Hub', verified: false, location: 'Pune' }
];

export const rawMaterials = [
  {
    id: 1,
    name: 'Fresh Tomatoes',
    category: 'tomatoes',
    price: 45,
    unit: 'kg',
    supplier: suppliers[0],
    image: 'https://images.unsplash.com/photo-1546470427-227527c9e1eb?w=400&h=300&fit=crop',
    inStock: true,
    description: 'Fresh red tomatoes, perfect for street food preparation',
    groupPrice: 38,
    minGroupQuantity: 50
  },
  {
    id: 2,
    name: 'Wheat Flour',
    category: 'flour',
    price: 35,
    unit: 'kg',
    supplier: suppliers[1],
    image: 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=300&fit=crop',
    inStock: true,
    description: 'Premium quality wheat flour for breads and rotis',
    groupPrice: 30,
    minGroupQuantity: 100
  },
  {
    id: 3,
    name: 'Sunflower Oil',
    category: 'oil',
    price: 120,
    unit: 'liter',
    supplier: suppliers[3],
    image: 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&h=300&fit=crop',
    inStock: true,
    description: 'Pure sunflower oil for cooking and frying',
    groupPrice: 110,
    minGroupQuantity: 20
  },
  {
    id: 4,
    name: 'Red Chili Powder',
    category: 'spices',
    price: 180,
    unit: 'kg',
    supplier: suppliers[2],
    image: 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop',
    inStock: false,
    description: 'Spicy red chili powder for authentic taste',
    groupPrice: 160,
    minGroupQuantity: 10
  },
  {
    id: 5,
    name: 'Large Onions',
    category: 'onions',
    price: 30,
    unit: 'kg',
    supplier: suppliers[0],
    image: 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400&h=300&fit=crop',
    inStock: true,
    description: 'Fresh large onions for cooking base',
    groupPrice: 25,
    minGroupQuantity: 100
  },
  {
    id: 6,
    name: 'Basmati Rice',
    category: 'rice',
    price: 85,
    unit: 'kg',
    supplier: suppliers[1],
    image: 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop',
    inStock: true,
    description: 'Premium basmati rice for biryanis and pulao',
    groupPrice: 78,
    minGroupQuantity: 50
  },
  {
    id: 7,
    name: 'Turmeric Powder',
    category: 'spices',
    price: 220,
    unit: 'kg',
    supplier: suppliers[2],
    image: 'https://images.unsplash.com/photo-1615485500704-8e990f9900f7?w=400&h=300&fit=crop',
    inStock: true,
    description: 'Pure turmeric powder for color and flavor',
    groupPrice: 200,
    minGroupQuantity: 5
  },
  {
    id: 8,
    name: 'Green Vegetables Mix',
    category: 'vegetables',
    price: 55,
    unit: 'kg',
    supplier: suppliers[4],
    image: 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop',
    inStock: true,
    description: 'Fresh mixed green vegetables',
    groupPrice: 48,
    minGroupQuantity: 30
  },
  {
    id: 9,
    name: 'Chicken (Fresh)',
    category: 'meat',
    price: 280,
    unit: 'kg',
    supplier: suppliers[3],
    image: 'https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400&h=300&fit=crop',
    inStock: true,
    description: 'Fresh chicken for non-veg preparations',
    groupPrice: 260,
    minGroupQuantity: 20
  },
  {
    id: 10,
    name: 'Cumin Seeds',
    category: 'spices',
    price: 350,
    unit: 'kg',
    supplier: suppliers[2],
    image: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop',
    inStock: true,
    description: 'Aromatic cumin seeds for seasoning',
    groupPrice: 320,
    minGroupQuantity: 5
  }
];

// Cart functionality with localStorage
export const cartManager = {
  getCart: () => {
    const cart = localStorage.getItem('streetFoodCart');
    return cart ? JSON.parse(cart) : [];
  },
  
  addToCart: (item, quantity = 1, isGroup = false) => {
    const cart = cartManager.getCart();
    const existingItem = cart.find(cartItem => 
      cartItem.id === item.id && cartItem.isGroup === isGroup
    );
    
    if (existingItem) {
      existingItem.quantity += quantity;
    } else {
      cart.push({
        ...item,
        quantity,
        isGroup,
        price: isGroup ? item.groupPrice : item.price,
        addedAt: new Date().toISOString()
      });
    }
    
    localStorage.setItem('streetFoodCart', JSON.stringify(cart));
    return cart;
  },
  
  removeFromCart: (itemId, isGroup = false) => {
    const cart = cartManager.getCart();
    const updatedCart = cart.filter(item => 
      !(item.id === itemId && item.isGroup === isGroup)
    );
    localStorage.setItem('streetFoodCart', JSON.stringify(updatedCart));
    return updatedCart;
  },
  
  updateQuantity: (itemId, quantity, isGroup = false) => {
    const cart = cartManager.getCart();
    const item = cart.find(cartItem => 
      cartItem.id === itemId && cartItem.isGroup === isGroup
    );
    
    if (item) {
      item.quantity = Math.max(0, quantity);
      if (item.quantity === 0) {
        return cartManager.removeFromCart(itemId, isGroup);
      }
    }
    
    localStorage.setItem('streetFoodCart', JSON.stringify(cart));
    return cart;
  },
  
  clearCart: () => {
    localStorage.removeItem('streetFoodCart');
    return [];
  },
  
  getCartTotal: () => {
    const cart = cartManager.getCart();
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  },
  
  getCartCount: () => {
    const cart = cartManager.getCart();
    return cart.reduce((count, item) => count + item.quantity, 0);
  }
};