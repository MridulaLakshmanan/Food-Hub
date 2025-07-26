import { useState, useEffect, useCallback } from 'react';
import { cartApi } from '../services/api';
import { useToast } from './use-toast';

export const useCart = () => {
  const [cart, setCart] = useState({ items: [], total: 0, count: 0 });
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  // Fetch cart data
  const fetchCart = useCallback(async () => {
    try {
      setIsLoading(true);
      const cartData = await cartApi.getCart();
      setCart(cartData);
    } catch (error) {
      console.error('Error fetching cart:', error);
      toast({
        title: "Error",
        description: "Failed to load cart data.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  }, [toast]);

  // Add item to cart
  const addToCart = useCallback(async (materialId, quantity = 1, isGroup = false) => {
    try {
      setIsLoading(true);
      await cartApi.addToCart(materialId, quantity, isGroup);
      await fetchCart(); // Refresh cart data
      
      toast({
        title: "Added to Cart!",
        description: `Item has been added to your cart.`,
      });
    } catch (error) {
      console.error('Error adding to cart:', error);
      toast({
        title: "Error",
        description: "Failed to add item to cart.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  }, [fetchCart, toast]);

  // Update cart item quantity
  const updateCartItem = useCallback(async (itemId, quantity) => {
    try {
      setIsLoading(true);
      if (quantity <= 0) {
        await cartApi.removeFromCart(itemId);
      } else {
        await cartApi.updateCartItem(itemId, quantity);
      }
      await fetchCart(); // Refresh cart data
    } catch (error) {
      console.error('Error updating cart item:', error);
      toast({
        title: "Error",
        description: "Failed to update cart item.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  }, [fetchCart, toast]);

  // Remove item from cart
  const removeFromCart = useCallback(async (itemId) => {
    try {
      setIsLoading(true);
      await cartApi.removeFromCart(itemId);
      await fetchCart(); // Refresh cart data
      
      toast({
        title: "Item Removed",
        description: "Item has been removed from your cart.",
      });
    } catch (error) {
      console.error('Error removing from cart:', error);
      toast({
        title: "Error",
        description: "Failed to remove item from cart.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  }, [fetchCart, toast]);

  // Clear entire cart
  const clearCart = useCallback(async () => {
    try {
      setIsLoading(true);
      await cartApi.clearCart();
      await fetchCart(); // Refresh cart data
      
      toast({
        title: "Cart Cleared",
        description: "All items have been removed from your cart.",
      });
    } catch (error) {
      console.error('Error clearing cart:', error);
      toast({
        title: "Error",
        description: "Failed to clear cart.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  }, [fetchCart, toast]);

  // Initialize cart on hook mount
  useEffect(() => {
    fetchCart();
  }, [fetchCart]);

  return {
    cart,
    isLoading,
    addToCart,
    updateCartItem,
    removeFromCart,
    clearCart,
    refreshCart: fetchCart
  };
};