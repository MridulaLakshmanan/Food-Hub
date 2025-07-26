import React, { useState, useEffect } from 'react';
import { X, Minus, Plus, ShoppingBag, CreditCard, Truck } from 'lucide-react';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Separator } from './ui/separator';
import { useCart } from '../hooks/useCart';
import { ordersApi } from '../services/api';
import { useToast } from '../hooks/use-toast';

const Cart = ({ isOpen, onClose }) => {
  const { cart, updateCartItem, removeFromCart, isLoading } = useCart();
  const [isCheckingOut, setIsCheckingOut] = useState(false);
  const { toast } = useToast();

  const handleUpdateQuantity = async (itemId, newQuantity) => {
    await updateCartItem(itemId, newQuantity);
  };

  const handleRemoveItem = async (itemId) => {
    await removeFromCart(itemId);
  };

  const handleCheckout = async () => {
    setIsCheckingOut(true);
    
    try {
      const orderResult = await ordersApi.createOrder();
      
      setIsCheckingOut(false);
      onClose();
      toast({
        title: "Order Placed Successfully! 🎉",
        description: `Your order #${orderResult.order_id} has been submitted and will be processed soon.`,
      });
    } catch (error) {
      setIsCheckingOut(false);
      toast({
        title: "Error",
        description: "Failed to place order. Please try again.",
        variant: "destructive",
      });
    }
  };

  const total = cart.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const itemCount = cart.items.reduce((count, item) => count + item.quantity, 0);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex justify-end">
      <div className="bg-white w-full max-w-md h-full overflow-hidden flex flex-col animate-in slide-in-from-right">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <div className="flex items-center space-x-2">
            <ShoppingBag className="h-5 w-5 text-orange-500" />
            <h2 className="text-lg font-semibold text-gray-900">
              Your Cart ({itemCount} items)
            </h2>
          </div>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="h-5 w-5" />
          </Button>
        </div>

        {/* Cart Items */}
        <div className="flex-1 overflow-y-auto p-4">
          {cart.items.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-gray-500">
              <ShoppingBag className="h-16 w-16 mb-4 text-gray-300" />
              <p className="text-lg font-medium">Your cart is empty</p>
              <p className="text-sm">Add some materials to get started!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {cart.items.map((item) => (
                <Card key={item.id} className="overflow-hidden">
                  <CardContent className="p-4">
                    <div className="flex space-x-3">
                      <img
                        src={item.image}
                        alt={item.material_name}
                        className="w-16 h-16 object-cover rounded-md"
                      />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between">
                          <div>
                            <h3 className="text-sm font-medium text-gray-900 truncate">
                              {item.material_name}
                            </h3>
                            <p className="text-xs text-gray-600">{item.supplier_name}</p>
                            {item.is_group && (
                              <Badge className="bg-purple-100 text-purple-800 mt-1" size="sm">
                                Group Deal
                              </Badge>
                            )}
                          </div>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleRemoveItem(item.id)}
                            className="text-red-500 hover:text-red-700 hover:bg-red-50"
                            disabled={isLoading}
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        </div>
                        
                        <div className="flex items-center justify-between mt-2">
                          <div className="flex items-center space-x-2">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleUpdateQuantity(item.id, item.quantity - 1)}
                              disabled={item.quantity <= 1 || isLoading}
                              className="h-8 w-8 p-0"
                            >
                              <Minus className="h-3 w-3" />
                            </Button>
                            <span className="text-sm font-medium min-w-[2rem] text-center">
                              {item.quantity}
                            </span>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleUpdateQuantity(item.id, item.quantity + 1)}
                              disabled={isLoading}
                              className="h-8 w-8 p-0"
                            >
                              <Plus className="h-3 w-3" />
                            </Button>
                          </div>
                          <div className="text-right">
                            <p className="text-sm font-semibold text-gray-900">
                              ₹{(item.price * item.quantity).toFixed(2)}
                            </p>
                            <p className="text-xs text-gray-600">
                              ₹{item.price}/{item.unit}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>

        {/* Footer - Checkout */}
        {cart.items.length > 0 && (
          <div className="border-t border-gray-200 bg-gray-50 p-4">
            <div className="space-y-3">
              {/* Total */}
              <div className="flex items-center justify-between">
                <span className="text-base font-medium text-gray-900">Total</span>
                <span className="text-xl font-bold text-gray-900">₹{total.toFixed(2)}</span>
              </div>
              
              <Separator />
              
              {/* Delivery Info */}
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Truck className="h-4 w-4" />
                <span>Estimated delivery: 2-3 business days</span>
              </div>

              {/* Checkout Button */}
              <Button
                onClick={handleCheckout}
                disabled={isCheckingOut}
                className="w-full bg-green-600 hover:bg-green-700 text-white py-3 text-base font-medium"
              >
                {isCheckingOut ? (
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Processing...</span>
                  </div>
                ) : (
                  <div className="flex items-center space-x-2">
                    <CreditCard className="h-4 w-4" />
                    <span>Proceed to Checkout - ₹{total.toFixed(2)}</span>
                  </div>
                )}
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Cart;