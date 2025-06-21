import LoginPage from "./pages/authPages/LoginPage";
import NotFoundPage from "./pages/stillPages/NotFoundPage";
import App from "./App";
import { createBrowserRouter } from "react-router-dom";
import RegisterPage from "./pages/authPages/RegisterPage";
import RootLayout from "./layouts/RootLayout";
import CenterBody from "./layouts/CenterBody";
import SearchPage from "./pages/SearchPage";
import ItemPage from "./pages/ItemPage";

const routes = createBrowserRouter([
  {
    element: <RootLayout />, // 🔁 Wraps all routes in AuthProvider
    children: [
      { path: "/login", element: <LoginPage /> },
      { path: "/register", element: <RegisterPage /> },
      {
        element: <CenterBody />,
        children: [
          { path: "/", element: <App /> },
          { path: "/search", element: <SearchPage /> },
          { path: "*", element: <NotFoundPage /> },
          { path:"/item/:id", element: <ItemPage /> }
        ],
      },
    ],
  },
]);

export default routes;
