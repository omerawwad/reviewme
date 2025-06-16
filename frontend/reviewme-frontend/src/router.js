import LoginPage from "./pages/authPages/LoginPage";
import NotFoundPage from "./pages/stillPages/NotFoundPage";
import App from "./App";
import { createBrowserRouter } from "react-router-dom";
import RegisterPage from "./pages/authPages/RegisterPage";
import RootLayout from "./layouts/RootLayout";

const routes = createBrowserRouter([
  {
    element: <RootLayout />, // 🔁 Wraps all routes in AuthProvider
    children: [
      { path: "/", element: <App /> },
      { path: "/login", element: <LoginPage /> },
      { path: "/register", element: <RegisterPage /> },
      { path: "*", element: <NotFoundPage /> },
    ],
  },
]);

export default routes;
