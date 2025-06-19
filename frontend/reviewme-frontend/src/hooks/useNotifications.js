import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";

const useNotifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [totalNotifications, setTotalNotifications] = useState(0);

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
  const { authTokens, isAuthenticated } = useAuth();

  const fetchNotifications = async () => {
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
      const response = await fetch(`${BACKEND_URL}/notifications`, {
        method: "GET",
        headers: header,
      });
      if (!response.ok) {
        throw new Error("Failed to fetch notifications");
      }
      const data = await response.json();
      setNotifications(data.notifications || []);
      setTotalNotifications(data.total_notifications || 0);
      setError(null);
    } catch (err) {
      setError(err.message);
      setNotifications([]);
      setTotalNotifications(0);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, [isAuthenticated]);

  return {
    notifications,
    loading,
    error,
    totalNotifications,
    refetch: fetchNotifications,
  };
};

export default useNotifications; 