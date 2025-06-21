import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";

const useItem = (itemId, page = 1, size = 10) => {
  const [item, setItem] = useState(null);
  const [highlighted, setHighlighted] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [pageInfo, setPageInfo] = useState({
    page: 1,
    page_size: size,
    total_pages: 0,
    total_reviews: 0,
  });

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
  const { authTokens, isAuthenticated } = useAuth();

  function setPage(newPage) {
    if (newPage < 1 || newPage > pageInfo.total_pages) return;
    setPageInfo((prev) => ({ ...prev, page: newPage }));
  }

  useEffect(() => {
    if (!itemId) return;
    const fetchItem = async () => {
      setLoading(true);
      setError(null);
      try {
        const headers =
          isAuthenticated && authTokens
            ? {
                Authorization: `Bearer ${authTokens.access}`,
                "Content-Type": "application/json",
              }
            : {
                "Content-Type": "application/json",
              };
        const response = await fetch(`${BACKEND_URL}/item/${itemId}`, {
          method: "GET",
          headers,
        });
        if (!response.ok) {
          throw new Error("Failed to fetch item");
        }
        const data = await response.json();
        setItem(data.item || null);
        setHighlighted(data.highlighted || false);
      } catch (err) {
        setError(err.message);
        setItem(null);
        setHighlighted(false);
      } finally {
        setLoading(false);
      }
    };
    const fetchReviews = async () => {
      setLoading(true);
      setError(null);
      try {
        const headers =
          isAuthenticated && authTokens
            ? {
                Authorization: `Bearer ${authTokens.access}`,
                "Content-Type": "application/json",
              }
            : {
                "Content-Type": "application/json",
              };
        const response = await fetch(
          `${BACKEND_URL}/reviews/${itemId}?page=${page}&size=${size}`,
          {
            method: "GET",
            headers,
          }
        );
        if (!response.ok) {
          throw new Error("Failed to fetch item reviews");
        }
        const data = await response.json();
        // console.log("Fetched reviews:", data);
        setReviews(data.reviews || []);
        setPageInfo({
          page: data.page || 1,
          page_size: data.page_size || size,
          total_pages: data.total_pages || 0,
          total_reviews: data.total_reviews || 0,
        });
      } catch (err) {
        setError(err.message);
        setReviews([]);
        setPageInfo({
          page: 1,
          page_size: size,
          total_pages: 0,
          total_reviews: 0,
        });
      } finally {
        setLoading(false);
      }
    };
    fetchItem();
    fetchReviews();
  }, [itemId, isAuthenticated, authTokens, BACKEND_URL]);

  return { item, loading, error, reviews, pageInfo, setPage };
};

export default useItem;
