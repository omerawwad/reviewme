import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";

const useReviews = (page = 1, size = 10, pollingInterval = 5000) => {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pageInfo, setPageInfo] = useState({
    total: 0,
    current: page,
    size: size,
    totalReviews: 0,
  });

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

  const { authTokens, isAuthenticated } = useAuth();
  // console.log("Auth token in useReviews:", authTokens);

  const setPage = (newPage) => {
    if (newPage < 1 || newPage > pageInfo.total) {
      // console.warn("Invalid page number:", newPage);
      return;
    }
    setPageInfo((prev) => ({ ...prev, current: newPage }));
    // console.log("Setting page to:", newPage);
  };

  const fetchReviews = async () => {
    // console.log(
    //   "Fetching reviews for page:",
    //   pageInfo.current,
    //   "size:",
    //   pageInfo.size
    // );
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
        `${BACKEND_URL}/reviews?page=${pageInfo.current}&size=${pageInfo.size}`,
        {
          method: "GET",
          headers: header,
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch reviews");
      }

      // console.log("Fetched reviews response:", await response.text);
      const data = await response.json();
      // console.log("Fetched reviews data:", data);
      setReviews(data.reviews || []);
      setPageInfo({
        total: data.total_pages || 1,
        current: data.page,
        size: data.page_size || size,
        totalReviews: data.total_reviews || 0,
      });
      setError(null);
    } catch (err) {
      setError(err.message);
      setReviews([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // console.log("isAuthenticated in useReviews:", isAuthenticated);
    // console.log("authTokens in useReviews:", authTokens);
    fetchReviews();

    // const intervalId = setInterval(fetchReviews, pollingInterval);
    // return () => clearInterval(intervalId);
  }, [page, size, isAuthenticated]);

  return {
    reviews,
    loading,
    error,
    pageInfo,
    refetch: fetchReviews,
    setPage,
  };
};

export default useReviews;
