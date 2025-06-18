import React, { useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import "../styles/NavBar.css";
import { MdOutlineRateReview } from "react-icons/md";
import { IoSearch } from "react-icons/io5";
import { MdKeyboardCommandKey } from "react-icons/md";
import { useLocation } from "react-router-dom";
import { useRef } from "react";
import { useAuth } from "../context/AuthContext";
import { Badge } from "antd";
import { FiLogOut } from "react-icons/fi";
import { IoMdNotificationsOutline } from "react-icons/io";
import { FiUser } from "react-icons/fi";

const userAgent = navigator.userAgent.toLowerCase();
const isMacAgent = /macintosh|mac os x/i.test(userAgent);
const isMobileAgent = /iphone|android|mobile/i.test(userAgent);

const innerWidth = window.innerWidth;
const isMobileScreen = innerWidth <= 850; // TODO: Make this dynamic

function NavBar({ children, links = [] }) {
  const inputRef = useRef(null);
  const { user, isAuthenticated, logoutUser } = useAuth();

  // console.log("isAuthenticated in NavBar:", isAuthenticated);
  // console.log("user in NavBar", user);

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
        {isAuthenticated ? (
          <NavbarToolsSignedIn user={user} logoutUser={logoutUser} />
        ) : (
          <NavbarToolsSignedOut />
        )}
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

function NavbarToolsSignedIn({ user, logoutUser, notificationCount }) {
  // console.log("User in NavbarToolsSignedIn:", logoutUser);
  return (
    <div className="navbar-links">
      {!isMobileAgent && (
        <NotificationBell notificationCount={notificationCount} />
      )}
      {user && (
        <Link className="navbar-link" to="/profile">
          <FiUser className="navbar-user-icon" size={20} />
        </Link>
      )}
      <p className="navbar-link" to="/login" onClick={() => logoutUser()}>
        <FiLogOut className="navbar-logout-icon" size={20} />
      </p>
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

function NotificationBell({ notificationCount = 3 }) {
  return (
    <div className="navbar-notification">
      <Badge
        count={notificationCount}
        offset={[0, 0]}
        size="small"
        className="navbar-notification-badge"
      >
        <IoMdNotificationsOutline size={20} />
      </Badge>
    </div>
  );
}

export default NavBar;
