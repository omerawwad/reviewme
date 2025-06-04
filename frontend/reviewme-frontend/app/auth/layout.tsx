import { Outlet } from "react-router";

const Layout = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-6 bg-white rounded-lg shadow-md">
        <Outlet />
      </div>
    </div>
  );
};
export default Layout;
export function meta() {
  return [
    { title: "Auth Layout" },
    {
      name: "description",
      content: "Authentication layout for the application",
    },
  ];
}
