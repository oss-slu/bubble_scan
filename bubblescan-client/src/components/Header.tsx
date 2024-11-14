import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./header.css";

function Header() {
  return (
    <>
      <nav className="navbar">
        <div className="container">
        
          <Link className="navbar-logo" to="/">Bubble Scan</Link>
          <div className="nav-links">
            <Link className="nav-link" to="/">Home</Link>
            <Link className="nav-link" to="/scan-sheets">Scan</Link>
            <Link className="nav-link" to="/custom-sheets">Custom Sheets</Link>

            <a className="nav-link" href="#AboutUS">
              About Us
            </a>
          </div>
        </div>
      </nav>
    </>
  );
}

export default Header;
