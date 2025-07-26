import React from 'react';
import { Search, SlidersHorizontal, ArrowUpDown } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';

const SearchAndFilters = ({ 
  searchTerm, 
  onSearchChange, 
  selectedCategory, 
  onCategoryChange, 
  categories,
  sortBy,
  onSortChange,
  filterBy,
  onFilterChange
}) => {
  const sortOptions = [
    { value: 'name', label: 'Name' },
    { value: 'price', label: 'Price' },
    { value: 'supplier', label: 'Supplier' }
  ];

  const filterOptions = [
    { value: 'all', label: 'All', active: filterBy === 'all' },
    { value: 'verified', label: 'Verified', active: filterBy === 'verified' },
    { value: 'instock', label: 'In Stock', active: filterBy === 'instock' },
    { value: 'group', label: 'Group Deals', active: filterBy === 'group' }
  ];

  return (
    <div className="bg-white shadow-sm border-b border-gray-100 py-4">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Search Bar */}
        <div className="relative mb-6">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
          <Input
            type="text"
            placeholder="Search materials or suppliers..."
            value={searchTerm}
            onChange={(e) => onSearchChange(e.target.value)}
            className="pl-10 pr-4 py-3 w-full text-lg border-2 border-gray-200 focus:border-orange-500 focus:ring-orange-500 rounded-xl transition-all duration-200"
          />
        </div>

        {/* Category Filter Chips */}
        <div className="mb-4">
          <div className="flex overflow-x-auto scrollbar-hide space-x-3 pb-2">
            <Button
              variant={selectedCategory === 'all' ? 'default' : 'outline'}
              size="sm"
              onClick={() => onCategoryChange('all')}
              className={`whitespace-nowrap transition-all duration-200 ${
                selectedCategory === 'all'
                  ? 'bg-orange-500 hover:bg-orange-600 text-white shadow-lg'
                  : 'border-gray-300 hover:border-orange-500 hover:text-orange-600'
              }`}
            >
              All Categories
            </Button>
            {categories.map((category) => (
              <Button
                key={category.id}
                variant={selectedCategory === category.id ? 'default' : 'outline'}
                size="sm"
                onClick={() => onCategoryChange(category.id)}
                className={`whitespace-nowrap transition-all duration-200 ${
                  selectedCategory === category.id
                    ? 'bg-orange-500 hover:bg-orange-600 text-white shadow-lg'
                    : 'border-gray-300 hover:border-orange-500 hover:text-orange-600'
                }`}
              >
                <span className="mr-1">{category.icon}</span>
                {category.name}
              </Button>
            ))}
          </div>
        </div>

        {/* Sort and Filter Controls */}
        <div className="flex flex-wrap items-center justify-between gap-4">
          {/* Filter Options */}
          <div className="flex flex-wrap items-center gap-2">
            {filterOptions.map((option) => (
              <Badge
                key={option.value}
                variant={option.active ? 'default' : 'outline'}
                className={`cursor-pointer transition-all duration-200 ${
                  option.active
                    ? 'bg-blue-500 hover:bg-blue-600 text-white'
                    : 'border-gray-300 hover:border-blue-500 hover:text-blue-600'
                }`}
                onClick={() => onFilterChange(option.value)}
              >
                {option.label}
              </Badge>
            ))}
          </div>

          {/* Sort Dropdown */}
          <div className="flex items-center space-x-2">
            <ArrowUpDown className="h-4 w-4 text-gray-500" />
            <select
              value={sortBy}
              onChange={(e) => onSortChange(e.target.value)}
              className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
            >
              {sortOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  Sort by {option.label}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SearchAndFilters;