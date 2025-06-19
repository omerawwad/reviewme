import React, { useEffect, useContext } from "react";
import useNotifications from "../hooks/useNotifications";
import useSearch from "../hooks/useSearch";
import { Link, useNavigate } from "react-router-dom";
import "../styles/NavBar.css";
import { MdOutlineRateReview } from "react-icons/md";
import { IoSearch } from "react-icons/io5";
import { MdKeyboardCommandKey } from "react-icons/md";
import { useLocation } from "react-router-dom";
import { useRef, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { Badge } from "antd";
import { FiLogOut } from "react-icons/fi";
import { IoMdNotificationsOutline } from "react-icons/io";
import { FiUser } from "react-icons/fi";
import { Popover } from "antd";

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

function NavbarToolsSignedIn({ user, logoutUser }) {
  // console.log("User in NavbarToolsSignedIn:", logoutUser);
  return (
    <div className="navbar-links">
      {!isMobileAgent && <NotificationBell />}
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
  const [searchQuery, setSearchQuery] = useState("");
  const [finalQuery, setFinalQuery] = useState("");
  const navigate = useNavigate();
  const { setQuery } = useSearch(finalQuery);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      // Navigate to search results page with query
      setFinalQuery(searchQuery.trim());
      setQuery(searchQuery.trim());
      navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSearch(e);
    }
  };

  return (
    <div className="navbar-input">
      <form onSubmit={handleSearch} className="nav-bar-search">
        <IoSearch />
        <input
          ref={inputRef}
          type="text"
          placeholder="Search Items..."
          className="navbar-input-field"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        {!isMobileAgent && (
          <kbd className="navbar-input-kbd">
            {isMacAgent ? <MdKeyboardCommandKey /> : "Ctrl "}K
          </kbd>
        )}
      </form>
    </div>
  );
}

function NotificationBell({}) {
  const { notifications, loading, error, totalNotifications, refetch } =
    useNotifications();
  return (
    <div className="navbar-notification">
      <Popover
        content={
          <NotivicationMenu
            notifications={notifications}
            loading={loading}
            error={error}
            totalNotifications={totalNotifications}
          />
        }
        title={`Notifications (${totalNotifications})`}
        placement="bottomRight"
        trigger="click"
      >
        <Badge
          count={totalNotifications}
          offset={[0, 0]}
          size="small"
          className="navbar-notification-badge"
        >
          <IoMdNotificationsOutline size={20} />
        </Badge>
      </Popover>
    </div>
  );
}

function NotivicationMenu({
  notifications = [],
  loading,
  error,
  totalNotifications,
}) {
  return (
    <div className="navbar-notification-menu">
      {totalNotifications > 0 ? (
        <NotificationList
          notifications={notifications}
          loading={loading}
          error={error}
        />
      ) : (
        <span>No new notifications</span>
      )}
    </div>
  );
}

function NotificationList({ notifications, loading, error }) {
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      {notifications.map((n) => (
        <Notification notification={n} key={n.id} />
      ))}
    </div>
  );
}

function Notification({ notification }) {
  return (
    <div className="notification-item">
      <span>{notification.message.slice(0, 45) + "..."}</span>
      <small>
        {new Date(notification.created_at).toLocaleString("en-GB", {
          day: "2-digit",
          month: "short",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
          hour12: true,
        })}
      </small>
    </div>
  );
}

export default NavBar;
