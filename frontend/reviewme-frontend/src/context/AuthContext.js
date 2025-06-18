import { createContext, useState, useEffect, useContext } from "react";
import { jwtDecode } from "jwt-decode";
import { useNavigate } from "react-router-dom";
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const AuthContext = createContext();
export const AuthProvider = ({ children }) => {
  const [loading, setLoading] = useState(true);

  const [authTokens, setAuthTokens] = useState(
    JSON.parse(localStorage.getItem("authTokens")) || null
  );
  const [user, setUser] = useState(
    authTokens ? jwtDecode(authTokens.access) : null
  );
  const [isAuthenticated, setIsAuthenticated] = useState(
    authTokens ? true : false
  );

  //   console.log(
  //     "AuthContext initialized with user:",
  //     user,
  //     "isAuthenticated:",
  //     isAuthenticated
  //   );

  const navigate = useNavigate();

  const loginUser = async (credentials) => {
    try {
      const response = await fetch(BACKEND_URL + "/token/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(credentials),
      });

      if (response.ok) {
        const data = await response.json();
        setUser(jwtDecode(data.access));
        localStorage.setItem("authTokens", JSON.stringify(data));
        setAuthTokens(data);
        setIsAuthenticated(true);
        navigate("/");
      } else {
        throw new Error("Login failed");
      }
    } catch (error) {
      console.error("Login error:", error);
    }
  };

  const logoutUser = () => {
    setIsAuthenticated(false);
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem("authTokens");
    navigate("/login");
  };

  const updateToken = async () => {
    if (authTokens) {
      try {
        const response = await fetch(BACKEND_URL + "/token/refresh/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ refresh: authTokens.refresh }),
        });

        if (response.ok) {
          const data = await response.json();
          setAuthTokens(data);
          setUser(jwtDecode(data.access));
          localStorage.setItem("authTokens", JSON.stringify(data));
        } else {
          logoutUser();
        }
      } catch (error) {
        console.error("Token update error:", error);
      }

      if (loading) {
        setLoading(false);
      }
    }
  };

  useEffect(() => {
    if (loading) {
      updateToken();
    }
    const interval = setInterval(() => {
      updateToken();
    }, 1000 * 60 * 4);
    return () => clearInterval(interval);
  }, [authTokens, loading]);

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isAuthenticated,
        loginUser,
        logoutUser,
        updateToken,
        authTokens,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};
