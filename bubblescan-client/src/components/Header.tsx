import { Link, useLocation } from "react-router-dom";
import "./header.css";

function Header() {
  const location = useLocation();

  return (
    <>
      <nav className="navbar">
        <div className="container">
          <Link className="navbar-logo" to="/">
            Bubble Scan
          </Link>
          <div className="nav-links">
            <Link
              className={`nav-link ${
                location.pathname === "/" ? "active" : ""
              }`}
              to="/"
            >
              Home
            </Link>
            <Link
              className={`nav-link ${
                location.pathname === "/scan-sheets" ? "active" : ""
              }`}
              to="/scan-sheets"
            >
              Scan
            </Link>
            <Link
              className={`nav-link ${
                location.pathname === "/custom-sheets" ? "active" : ""
              }`}
              to="/custom-sheets"
            >
              Custom Sheets
            </Link>
            <Link
              className={`nav-link ${
                location.pathname === "/about-us" ? "active" : ""
              }`}
              to="/about-us"
            >
              About Us
            </Link>
          </div>
        </div>
      </nav>
    </>
  );
}

export default Header;
