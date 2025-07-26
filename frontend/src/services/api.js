import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Generate or get session ID for cart management
const getSessionId = () => {
  let sessionId = localStorage.getItem('sessionId');
  if (!sessionId) {
    sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('sessionId', sessionId);
  }
  return sessionId;
};

// Materials API
export const materialsApi = {
  // Get all materials with optional filtering and sorting
  getMaterials: async (params = {}) => {
    try {
      const response = await apiClient.get('/materials', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching materials:', error);
      throw error;
    }
  },

  // Get material by ID
  getMaterialById: async (id) => {
    try {
      const response = await apiClient.get(`/materials?id=${id}`);
      return response.data[0];
    } catch (error) {
      console.error('Error fetching material:', error);
      throw error;
    }
  }
};

// Categories API
export const categoriesApi = {
  getCategories: async () => {
    try {
      const response = await apiClient.get('/categories');
      return response.data;
    } catch (error) {
      console.error('Error fetching categories:', error);
      throw error;
    }
  }
};

// Suppliers API
export const suppliersApi = {
  getSuppliers: async () => {
    try {
      const response = await apiClient.get('/suppliers');
      return response.data;
    } catch (error) {
      console.error('Error fetching suppliers:', error);
      throw error;
    }
  }
};

// Cart API
export const cartApi = {
  // Get cart for current session
  getCart: async () => {
    try {
      const sessionId = getSessionId();
      const response = await apiClient.get(`/cart/${sessionId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching cart:', error);
      throw error;
    }
  },

  // Add item to cart
  addToCart: async (materialId, quantity = 1, isGroup = false) => {
    try {
      const sessionId = getSessionId();
      const response = await apiClient.post(`/cart/${sessionId}/add`, {
        material_id: materialId,
        quantity: quantity,
        is_group: isGroup
      });
      return response.data;
    } catch (error) {
      console.error('Error adding to cart:', error);
      throw error;
    }
  },

  // Update cart item quantity
  updateCartItem: async (itemId, quantity) => {
    try {
      const sessionId = getSessionId();
      const response = await apiClient.put(`/cart/${sessionId}/item/${itemId}`, {
        quantity: quantity
      });
      return response.data;
    } catch (error) {
      console.error('Error updating cart item:', error);
      throw error;
    }
  },

  // Remove item from cart
  removeFromCart: async (itemId) => {
    try {
      const sessionId = getSessionId();
      const response = await apiClient.delete(`/cart/${sessionId}/item/${itemId}`);
      return response.data;
    } catch (error) {
      console.error('Error removing from cart:', error);
      throw error;
    }
  },

  // Clear entire cart
  clearCart: async () => {
    try {
      const sessionId = getSessionId();
      const response = await apiClient.delete(`/cart/${sessionId}`);
      return response.data;
    } catch (error) {
      console.error('Error clearing cart:', error);
      throw error;
    }
  }
};

// Orders API
export const ordersApi = {
  // Create order (checkout)
  createOrder: async () => {
    try {
      const sessionId = getSessionId();
      const response = await apiClient.post('/orders', {
        session_id: sessionId
      });
      return response.data;
    } catch (error) {
      console.error('Error creating order:', error);
      throw error;
    }
  },

  // Get orders for current session
  getOrders: async () => {
    try {
      const sessionId = getSessionId();
      const response = await apiClient.get(`/orders/${sessionId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching orders:', error);
      throw error;
    }
  }
};

// Export session utilities
export const sessionUtils = {
  getSessionId,
  clearSession: () => {
    localStorage.removeItem('sessionId');
  }
};

export default apiClient;