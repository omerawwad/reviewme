import React, { useEffect } from "react";
import { Link } from "react-router-dom";
import "../styles/NavBar.css";
import { MdOutlineRateReview } from "react-icons/md";
import { IoSearch } from "react-icons/io5";
import { MdKeyboardCommandKey } from "react-icons/md";
import { useLocation } from "react-router-dom";
import { useRef } from "react";

const userAgent = navigator.userAgent.toLowerCase();
const isMacAgent = /macintosh|mac os x/i.test(userAgent);
const isMobileAgent = /iphone|android|mobile/i.test(userAgent);

const innerWidth = window.innerWidth;
const isMobileScreen = innerWidth <= 850; // TODO: Make this dynamic

function NavBar({ children, user = null, links = [] }) {
  const inputRef = useRef(null);
  useEffect(() => {
    const handleKeyDown = (e) => {
      const cmdOrCtrl = isMacAgent ? e.metaKey : e.ctrlKey;

      if (cmdOrCtrl && e.key.toLowerCase() === "k") {
        e.preventDefault();
        inputRef.current?.focus();
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);
  return (
    <div className="navbar">
      <div className="navbar-main">
        <Logo />
        <NavBarLinks links={links} />
      </div>
      <div className="navbar-tools">
        <SearchWithKbd inputRef={inputRef} />
        <NavbarToolsSignedOut />
      </div>
    </div>
  );
}

function Logo() {
  return (
    <div>
      <Link className="navbar-logo" to="/">
        <MdOutlineRateReview className="navbar-logo-icon" />
        REVIEW ME
      </Link>
    </div>
  );
}

function NavBarLinks({ links }) {
  const [selectedTab, setSelectedTab] = React.useState("");
  const location = useLocation();

  useEffect(() => {
    // const location = window.location.pathname;
    // console.log("Current location:", location);
    setSelectedTab(location.pathname);
  }, [location]);
  return (
    <div className="navbar-links">
      {links.map((link) => (
        <Link
          key={link.path}
          className={`navbar-link ${
            selectedTab === link.path ? "navbar-link-active" : ""
          }`}
          to={link.path}
          onClick={() => setSelectedTab(link.path)}
        >
          {link.name}
        </Link>
      ))}
    </div>
  );
}

function NavbarToolsSignedOut() {
  return (
    <div className="navbar-links">
      <Link className="navbar-link" to="/login">
        Login
      </Link>
      <Link className="navbar-link" to="/register">
        Register
      </Link>
    </div>
  );
}

function NavbarToolsSignedIn({ user }) {
  return (
    <div className="navbar-links">
      <Link className="navbar-link" to="/profile">
        {user.username}
      </Link>
      <Link className="navbar-link" to="/logout">
        Logout
      </Link>
    </div>
  );
}

function SearchWithKbd({ inputRef }) {
  //   console.log(isMobileScreen);
  return (
    <div className="navbar-input">
      <div className="nav-bar-search">
        <IoSearch />
        <input
          ref={inputRef}
          type="text"
          placeholder="Search Items..."
          className="navbar-input-field"
        />
        {!isMobileAgent && (
          <kbd className="navbar-input-kbd">
            {isMacAgent ? <MdKeyboardCommandKey /> : "Ctrl "}K
          </kbd>
        )}
      </div>
    </div>
  );
}

export default NavBar;
