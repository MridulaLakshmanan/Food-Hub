import React, { useState, useEffect } from 'react';
import { ShoppingCart, Search, User, Menu, X } from 'lucide-react';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { cartManager } from '../data/mockData';

const Navbar = ({ onCartClick, cartCount }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [currentCartCount, setCurrentCartCount] = useState(0);

  useEffect(() => {
    setCurrentCartCount(cartManager.getCartCount());
  }, [cartCount]);

  const navItems = [
    { label: 'Browse', active: true },
    { label: 'Orders', active: false },
    { label: 'Suppliers', active: false },
    { label: 'Analytics', active: false }
  ];

  return (
    <nav className="bg-white shadow-lg border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-orange-500 to-red-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">SF</span>
            </div>
            <span className="text-xl font-bold text-gray-900">StreetFood Hub</span>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => (
              <button
                key={item.label}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                  item.active
                    ? 'text-orange-600 bg-orange-50 border-b-2 border-orange-500'
                    : 'text-gray-700 hover:text-orange-600 hover:bg-gray-50'
                }`}
              >
                {item.label}
              </button>
            ))}
          </div>

          {/* Right side actions */}
          <div className="flex items-center space-x-4">
            {/* Cart */}
            <Button
              variant="ghost"
              size="sm"
              onClick={onCartClick}
              className="relative hover:bg-orange-50 hover:text-orange-600 transition-all duration-200"
            >
              <ShoppingCart className="h-5 w-5" />
              {currentCartCount > 0 && (
                <Badge 
                  className="absolute -top-2 -right-2 bg-orange-500 hover:bg-orange-600 text-white text-xs px-1.5 py-0.5 animate-pulse"
                >
                  {currentCartCount}
                </Badge>
              )}
            </Button>

            {/* User Menu */}
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
                <User className="h-4 w-4 text-white" />
              </div>
              <span className="hidden sm:block text-sm text-gray-700">Vendor</span>
            </div>

            {/* Mobile menu button */}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden"
            >
              {isMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-100 bg-white">
            <div className="flex flex-col space-y-2">
              {navItems.map((item) => (
                <button
                  key={item.label}
                  className={`px-3 py-2 rounded-md text-sm font-medium text-left transition-all duration-200 ${
                    item.active
                      ? 'text-orange-600 bg-orange-50'
                      : 'text-gray-700 hover:text-orange-600 hover:bg-gray-50'
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;