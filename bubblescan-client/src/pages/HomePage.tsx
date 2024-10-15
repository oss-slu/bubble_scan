import React from "react";
import { useNavigate } from "react-router-dom";

function HomePage() {
  const navigate = useNavigate();

  const handleScanClick = () => {
    navigate("/scan");
  };

  return (
    <div className="home-page">
      <h1>Bubble Scan</h1>
      <p>Grading Made Easy</p>
      <button onClick={handleScanClick} className="scan-button">
        Scan
      </button>
    </div>
  );
}

export default HomePage;
