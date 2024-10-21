import React from "react";
import { useNavigate } from "react-router-dom";

function HomePage() {
  const navigate = useNavigate();

  const handleScanClick = () => {
    navigate("/scan");
  };

  const handleCustomSheetsClick = () => {
    navigate("/custom-sheets");
  };

  return (
    <div className="home-page">
      <h1>Bubble Scan</h1>
      <p>Grading Made Easy</p>
      <div className="button-group">
        <button onClick={handleScanClick} className="scan-button">
          Scan
        </button>
        <button
          onClick={handleCustomSheetsClick}
          className="custom-sheets-button"
        >
          Custom Sheet
        </button>
      </div>
    </div>
  );
}

export default HomePage;
