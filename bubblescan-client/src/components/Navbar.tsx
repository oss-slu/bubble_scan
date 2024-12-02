import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
function Navbar() {
    const location = useLocation();
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    };
    const handleLinkClick = () => {
        setIsMenuOpen(false);
    };
    return (

        <nav>
            <div className="hamburger" onClick={toggleMenu}>
                <div className={`bar ${isMenuOpen ? "change" : ""}`}></div>
                <div className={`bar ${isMenuOpen ? "change" : ""}`}></div>
                <div className={`bar ${isMenuOpen ? "change" : ""}`}></div>
            </div>
            <ul className={`navbar-links ${isMenuOpen ? "active" : ""}`}>
                <li>
                    <Link to="/" className={location.pathname === "/" ? "active" : ""} onClick={handleLinkClick}>Home</Link>
                </li>
                <li>
                    <Link to="/upload" className={location.pathname === "/upload" ? "active" : ""} onClick={handleLinkClick}>Upload Sheets</Link>
                </li>
                <li>
                    <Link to="/create" className={location.pathname === "/create" ? "active" : ""} onClick={handleLinkClick}>Create Custom Sheets</Link>
                </li>
                <li>
                    <Link to="/about" className={location.pathname === "/about" ? "active" : ""} onClick={handleLinkClick}>About Us</Link>
                </li>
            </ul>
        </nav>
    );
}
export default Navbar;