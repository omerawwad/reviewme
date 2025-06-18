import { useState, useEffect } from "react";

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

  const setPage = (newPage) => {
    if (newPage < 1 || newPage > pageInfo.total) {
      console.warn("Invalid page number:", newPage);
      return;
    }
    setPageInfo((prev) => ({ ...prev, current: newPage }));
    console.log("Setting page to:", newPage);
  };

  const fetchReviews = async () => {
    // console.log(
    //   "Fetching reviews for page:",
    //   pageInfo.current,
    //   "size:",
    //   pageInfo.size
    // );
    try {
      setLoading(true);
      const response = await fetch(
        `${BACKEND_URL}/reviews?page=${pageInfo.current}&size=${pageInfo.size}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            // Authorization: ``,
          },
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
    fetchReviews();

    // const intervalId = setInterval(fetchReviews, pollingInterval);
    // return () => clearInterval(intervalId);
  }, [page, size]);

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
