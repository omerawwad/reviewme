import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";

const useSearch = (query = "", page = 1, size = 10) => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [pageInfo, setPageInfo] = useState({
    page: 1,
    page_size: size,
    total_pages: 0,
    total_items: 0,
  });

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
  const { authTokens, isAuthenticated } = useAuth();

  const searchItems = async (
    searchQuery = query,
    pageNum = page,
    pageSize = size
  ) => {
    if (!searchQuery.trim()) {
      setItems([]);
      setPageInfo({
        page: 1,
        page_size: pageSize,
        total_pages: 0,
        total_items: 0,
      });
      return;
    }

    const header =
      isAuthenticated && authTokens
        ? {
            Authorization: `Bearer ${authTokens.access}`,
            "Content-Type": "application/json",
          }
        : {
            "Content-Type": "application/json",
          };

    try {
      setLoading(true);
      const response = await fetch(
        `${BACKEND_URL}/search?query=${encodeURIComponent(
          searchQuery
        )}&page=${pageNum}&size=${pageSize}`,
        {
          method: "GET",
          headers: header,
        }
      );

      if (!response.ok) {
        throw new Error("Failed to search items");
      }

      const data = await response.json();
      setItems(data.items || []);
      setPageInfo({
        page: data.page || 1,
        page_size: data.page_size || pageSize,
        total_pages: data.total_pages || 0,
        total_items: data.total_items || 0,
      });
      setError(null);
    } catch (err) {
      setError(err.message);
      setItems([]);
      setPageInfo({
        page: 1,
        page_size: pageSize,
        total_pages: 0,
        total_items: 0,
      });
    } finally {
      setLoading(false);
    }
  };

  const setPage = (newPage) => {
    if (newPage < 1 || newPage > pageInfo.total_pages) {
      return;
    }
    searchItems(query, newPage, size);
  };

  const setQuery = (newQuery) => {
    searchItems(newQuery, 1, size);
  };

  useEffect(() => {
    if (query.trim()) {
      searchItems(query, page, size);
    }
  }, [query, page, size, isAuthenticated]);

  return {
    items,
    loading,
    error,
    pageInfo,
    search: searchItems,
    setPage,
    setQuery,
  };
};

export default useSearch;
