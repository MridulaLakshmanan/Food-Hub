import { useState, useEffect, useCallback } from 'react';
import { materialsApi, categoriesApi } from '../services/api';

export const useMaterials = () => {
  const [materials, setMaterials] = useState([]);
  const [categories, setCategories] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch materials with filtering and sorting
  const fetchMaterials = useCallback(async (params = {}) => {
    try {
      setIsLoading(true);
      setError(null);
      
      const [materialsData, categoriesData] = await Promise.all([
        materialsApi.getMaterials(params),
        categories.length === 0 ? categoriesApi.getCategories() : Promise.resolve(categories)
      ]);

      setMaterials(materialsData);
      if (categories.length === 0) {
        setCategories(categoriesData);
      }
    } catch (err) {
      console.error('Error fetching materials:', err);
      setError(err.message || 'Failed to fetch materials');
    } finally {
      setIsLoading(false);
    }
  }, [categories.length]);

  // Initialize data on hook mount
  useEffect(() => {
    fetchMaterials();
  }, [fetchMaterials]);

  return {
    materials,
    categories,
    isLoading,
    error,
    fetchMaterials
  };
};