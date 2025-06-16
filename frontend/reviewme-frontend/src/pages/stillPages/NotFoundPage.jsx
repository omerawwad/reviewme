import { BiSolidError } from "react-icons/bi";

import CenterBody from "../../layouts/CenterBody";
import "../../styles/NotFoundPage.css";

function NotFoundPage() {
  return (
    <CenterBody>
      <div className="not-found">
        <BiSolidError className="not-found-icon" />
        <p className="not-found-text">
          <strong className="not-found-code">404</strong> Page Not Found
        </p>
        <p>Sorry, the page you are looking for does not exist.</p>
      </div>
    </CenterBody>
  );
}

export default NotFoundPage;
