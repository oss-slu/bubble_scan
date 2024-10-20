import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import HomePage from "./pages/HomePage";
import ScanPage from "./pages/ScanPage";
import CustomSheetsPage from "./pages/CustomSheetsPage"; // New Custom Sheets Page
import "./App.css";

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/scan">Scan</Link>
            </li>
            <li>
              <Link to="/custom-sheets">Create Custom Sheets</Link>{" "}
              {/* New link */}
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/scan" element={<ScanPage />} />
          <Route path="/custom-sheets" element={<CustomSheetsPage />} />{" "}
          {/* New route */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
