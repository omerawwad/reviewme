import { useState } from "react";
import { useAuth } from "../context/AuthContext";

const useMarkNotificationRead = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
  const { authTokens, isAuthenticated } = useAuth();

  const markAsRead = async (notificationId) => {
    setLoading(true);
    setError(null);
    setSuccess(false);
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
        `${BACKEND_URL}/notification/read?notification_id=${notificationId}`,
        {
          method: "POST",
          headers,
        }
      );
      if (!response.ok) {
        throw new Error("Failed to mark notification as read");
      }
      setSuccess(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { markAsRead, loading, error, success };
};

export default useMarkNotificationRead; 