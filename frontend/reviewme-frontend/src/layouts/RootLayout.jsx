import { Outlet } from "react-router-dom";
import { AuthProvider } from "../context/AuthContext";
import { Provider } from "../components/ui/provider";
import { LightMode } from "../components/ui/color-mode";

const RootLayout = () => (
  <AuthProvider>
    <Provider style={{ backgroundColor: "white" }}>
      <LightMode>
        <Outlet />
      </LightMode>
    </Provider>
  </AuthProvider>
);

export default RootLayout;
