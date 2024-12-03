import React from "react";
import { NavLink } from "react-router-dom";
import "../styles/Header.css";

const Header: React.FC = () => {
    return (
        <header className="header">
            <div>Bubble Scan</div>
            <nav className="nav-links">
                <NavLink to="/" className="nav-link" >Home</NavLink>
                <NavLink to="/Scan" className="nav-link" >Scan</NavLink>
                <NavLink to="/customsheets" className="nav-link" >Custom Sheets</NavLink>
                <NavLink to="/Aboutus" className="nav-link" >About Us</NavLink>

            </nav>
        </header>
    );
};

export default Header;
