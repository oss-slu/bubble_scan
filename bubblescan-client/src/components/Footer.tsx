import { Link } from "react-router-dom";
import "./footer.css";

function Footer() {
  return (
    <div className="footer">
      <div className="container">
        <div className="logo-div-footer">
          <Link className="navbar-logo" to="/">
            Bubble Scan
          </Link>
        </div>
        <div className="p-div-footer">
          <p>Product of Open Source SLU</p>
        </div>
      </div>
    </div>
  );
}

export default Footer;
