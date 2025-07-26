import React, { useState } from 'react';
import { ShoppingCart, Users, Verified, AlertCircle, Star } from 'lucide-react';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Card, CardContent } from './ui/card';
import { useToast } from '../hooks/use-toast';

const MaterialCard = ({ material, onAddToCart }) => {
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleBuyNow = async () => {
    setIsLoading(true);
    try {
      onAddToCart(material, 1, false);
      toast({
        title: "Added to Cart!",
        description: `${material.name} has been added to your cart.`,
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to add item to cart.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleJoinGroup = async () => {
    setIsLoading(true);
    try {
      onAddToCart(material, material.minGroupQuantity, true);
      toast({
        title: "Joined Group Deal!",
        description: `You've joined the group deal for ${material.name}. Minimum quantity: ${material.minGroupQuantity} ${material.unit}`,
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to join group deal.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const savings = ((material.price - material.groupPrice) / material.price * 100).toFixed(0);

  return (
    <Card className="group hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 bg-white border border-gray-200 overflow-hidden">
      <div className="relative">
        {/* Product Image */}
        <div className="aspect-w-16 aspect-h-12 bg-gray-100 overflow-hidden">
          <img
            src={material.image}
            alt={material.name}
            className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
          />
        </div>

        {/* Status Badges */}
        <div className="absolute top-2 left-2 flex flex-col space-y-1">
          {!material.inStock && (
            <Badge variant="destructive" className="text-xs">
              <AlertCircle className="h-3 w-3 mr-1" />
              Out of Stock
            </Badge>
          )}
          {material.supplier.verified && (
            <Badge className="bg-green-500 hover:bg-green-600 text-white text-xs">
              <Verified className="h-3 w-3 mr-1" />
              Verified
            </Badge>
          )}
        </div>

        {/* Group Deal Badge */}
        {material.groupPrice < material.price && (
          <div className="absolute top-2 right-2">
            <Badge className="bg-purple-500 hover:bg-purple-600 text-white text-xs animate-pulse">
              Save {savings}%
            </Badge>
          </div>
        )}
      </div>

      <CardContent className="p-4">
        {/* Material Info */}
        <div className="mb-3">
          <h3 className="text-lg font-semibold text-gray-900 group-hover:text-orange-600 transition-colors duration-200">
            {material.name}
          </h3>
          <p className="text-sm text-gray-600 mt-1 line-clamp-2">
            {material.description}
          </p>
        </div>

        {/* Supplier Info */}
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-1">
            <Star className="h-4 w-4 text-yellow-400 fill-current" />
            <span className="text-sm font-medium text-gray-700">
              {material.supplier.name}
            </span>
          </div>
          <span className="text-xs text-gray-500">{material.supplier.location}</span>
        </div>

        {/* Pricing */}
        <div className="mb-4">
          <div className="flex items-center justify-between">
            <div>
              <span className="text-xl font-bold text-gray-900">
                ₹{material.price}
              </span>
              <span className="text-sm text-gray-600 ml-1">/{material.unit}</span>
            </div>
            {material.groupPrice < material.price && (
              <div className="text-right">
                <div className="text-sm text-purple-600 font-medium">
                  Group: ₹{material.groupPrice}/{material.unit}
                </div>
                <div className="text-xs text-gray-500">
                  Min: {material.minGroupQuantity} {material.unit}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex space-x-2">
          <Button
            onClick={handleBuyNow}
            disabled={!material.inStock || isLoading}
            className="flex-1 bg-orange-500 hover:bg-orange-600 text-white transition-all duration-200"
            size="sm"
          >
            <ShoppingCart className="h-4 w-4 mr-1" />
            Buy Now
          </Button>
          
          <Button
            onClick={handleJoinGroup}
            disabled={!material.inStock || isLoading}
            variant="outline"
            className="flex-1 border-purple-500 text-purple-600 hover:bg-purple-50 hover:border-purple-600 transition-all duration-200"
            size="sm"
          >
            <Users className="h-4 w-4 mr-1" />
            Join Group
          </Button>
        </div>

        {/* Group Deal Info */}
        {material.groupPrice < material.price && (
          <div className="mt-2 p-2 bg-purple-50 rounded-md">
            <p className="text-xs text-purple-700">
              💡 Save ₹{(material.price - material.groupPrice)} per {material.unit} with group buying!
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default MaterialCard;