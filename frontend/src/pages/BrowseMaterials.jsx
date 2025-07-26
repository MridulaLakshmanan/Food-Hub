import React, { useState, useEffect } from 'react';
import { Toaster } from '../components/ui/toaster';
import Navbar from '../components/Navbar';
import SearchAndFilters from '../components/SearchAndFilters';
import MaterialCard from '../components/MaterialCard';
import Cart from '../components/Cart';
import { useMaterials } from '../hooks/useMaterials';
import { useCart } from '../hooks/useCart';
import { ordersApi } from '../services/api';

const BrowseMaterials = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [sortBy, setSortBy] = useState('name');
  const [filterBy, setFilterBy] = useState('all');
  const [isCartOpen, setIsCartOpen] = useState(false);

  // Use custom hooks for data management
  const { materials, categories, isLoading: materialsLoading, fetchMaterials } = useMaterials();
  const { cart, addToCart, isLoading: cartLoading } = useCart();

  // Fetch materials when filters change
  useEffect(() => {
    const params = {};
    if (searchTerm) params.search = searchTerm;
    if (selectedCategory !== 'all') params.category = selectedCategory;
    if (sortBy) params.sort_by = sortBy;
    if (filterBy !== 'all') params.filter_by = filterBy;
    
    fetchMaterials(params);
  }, [searchTerm, selectedCategory, sortBy, filterBy, fetchMaterials]);

  const handleAddToCart = async (material, quantity, isGroup) => {
    await addToCart(material.id, quantity, isGroup);
  };

  const handleCartClick = () => {
    setIsCartOpen(true);
  };

  const handleCartClose = () => {
    setIsCartOpen(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar 
        onCartClick={handleCartClick}
        cartCount={cartCount}
      />

      <SearchAndFilters
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        selectedCategory={selectedCategory}
        onCategoryChange={setSelectedCategory}
        categories={categories}
        sortBy={sortBy}
        onSortChange={setSortBy}
        filterBy={filterBy}
        onFilterChange={setFilterBy}
      />

      {/* Results Header */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              Browse Raw Materials
            </h1>
            <p className="text-gray-600 mt-1">
              {filteredMaterials.length} materials found
              {selectedCategory !== 'all' && (
                <span className="ml-2">
                  in {categories.find(cat => cat.id === selectedCategory)?.name}
                </span>
              )}
            </p>
          </div>
          
          {/* Quick Stats */}
          <div className="hidden sm:flex items-center space-x-4 text-sm text-gray-600">
            <div className="flex items-center space-x-1">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span>{rawMaterials.filter(m => m.inStock).length} In Stock</span>
            </div>
            <div className="flex items-center space-x-1">
              <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
              <span>{rawMaterials.filter(m => m.supplier.verified).length} Verified</span>
            </div>
            <div className="flex items-center space-x-1">
              <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
              <span>{rawMaterials.filter(m => m.groupPrice < m.price).length} Group Deals</span>
            </div>
          </div>
        </div>

        {/* Materials Grid */}
        {filteredMaterials.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">📦</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No materials found</h3>
            <p className="text-gray-600">
              Try adjusting your search or filters to find what you're looking for.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredMaterials.map((material) => (
              <MaterialCard
                key={material.id}
                material={material}
                onAddToCart={handleAddToCart}
              />
            ))}
          </div>
        )}

        {/* Load More Button - Future Enhancement */}
        {filteredMaterials.length > 0 && (
          <div className="text-center mt-12">
            <p className="text-gray-600">
              Showing {filteredMaterials.length} of {rawMaterials.length} materials
            </p>
          </div>
        )}
      </div>

      {/* Cart Sidebar */}
      <Cart
        isOpen={isCartOpen}
        onClose={handleCartClose}
        onCartUpdate={updateCartCount}
      />

      <Toaster />
    </div>
  );
};

export default BrowseMaterials;