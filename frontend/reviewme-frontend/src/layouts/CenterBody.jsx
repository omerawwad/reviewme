import NavBar from "../components/NavBar";
import "../styles/CenterBody.css";

const links = [
  { name: "Home", path: "/" },
  { name: "Top Reviews", path: "/top" },
  { name: "Categories", path: "/categories" },
];

function CenterBody({ children, navBar = true }) {
  return (
    <>
      {navBar && <NavBar links={links} />}
      <div className="center-body">
        <div className="center-body-content">{children}</div>
      </div>
    </>
  );
}

export default CenterBody;
