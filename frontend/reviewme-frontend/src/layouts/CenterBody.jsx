import { Outlet } from "react-router-dom";
import NavBar from "../components/NavBar";
import "../styles/CenterBody.css";

const links = [
  { name: "Home", path: "/" },
  { name: "Top Reviews", path: "/top" },
];

function CenterBody({ children, navBar = true }) {
  return (
    <>
      {navBar && <NavBar links={links} />}
      <div className="center-body">
        <div className="center-body-content">
          <Outlet />
        </div>
      </div>
    </>
  );
}

export default CenterBody;
