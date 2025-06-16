import { Outlet } from "react-router-dom";
import { AuthProvider } from "../context/AuthContext";

const RootLayout = () => (
  <AuthProvider>
    <Outlet />
  </AuthProvider>
);

export default RootLayout;
