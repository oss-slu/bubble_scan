import React from 'react';
import './Homepage.css';

const Homepage: React.FC = () => {
  return (
    <div className="homepage">
      {/* Welcome Section with Typing Effect */}
      <div className="welcome-section">
        <h1 className="typing-effect">Welcome to <span>BubbleScan</span></h1>
        
      </div>

      {/* About Section in the Middle */}
      <div className="about-section">
        <h2>About BubbleScan</h2>
        <p> BubbleScan is a user-friendly tool designed to streamline the grading process for scantron sheets. It enables seamless PDF uploads, efficient grading, and easy generation of custom answer sheets, helping educators save time and reduce reliance on physical scantron machines. Whether you're looking to create tailored exam sheets or retrieve insightful grading reports, BubbleScan simplifies it all.
     
                </p>
      </div>

      {/* Features Section at the Bottom */}
      <div className="features-container">
        <div className="feature-box">
          <h3>Upload Files</h3>
          <p>Upload your scantron sheets effortlessly for fast, automated grading..</p>
        </div>
        <div className="feature-box">
          <h3>Create Custom Sheets</h3>
          <p>Tailor answer sheets to your exam needs with flexible custom templates.</p>
        </div>
        <div className="feature-box">
          <h3>View Results</h3>
          <p>Access and download detailed grading reports for insightful analysis.</p>
        </div>
      </div>
    </div>
  );
};

export default Homepage;
