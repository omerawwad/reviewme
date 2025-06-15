import "../styles/AuthLayout.css";
import { Link } from "react-router-dom";
import { MdOutlineRateReview } from "react-icons/md";

function AuthLayout({ children }) {
  return (
    <div className="centered-form">
      <div className="form-container">
        <AuthPageHeader />
        {children}
      </div>
    </div>
  );
}

function AuthPageHeader() {
  return (
    <div>
      <Link className="authpage-logo" to="/">
        <MdOutlineRateReview className="authpage-logo-icon" />
        REVIEW ME
      </Link>
    </div>
  );
}

export default AuthLayout;
