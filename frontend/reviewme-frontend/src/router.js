import LoginPage from "./pages/authPages/LoginPage";
import NotFoundPage from "./pages/stillPages/NotFoundPage";
import App from "./App";
import { createBrowserRouter } from "react-router-dom";
import RegisterPage from "./pages/authPages/RegisterPage";

const routes = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/register",
    element: <RegisterPage />,
  },
  {
    path: "*",
    element: <NotFoundPage />,
  },
]);

export default routes;
