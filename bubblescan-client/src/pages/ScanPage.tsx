import React from "react";
import FileUploadComponent from "../components/FileUploadComponent";

function ScanPage() {
  return (
    <div className="scan-page">
      <h1>Scan Your Sheets Here</h1>
      <p>You can upload your files below</p>
      <div className="file-upload-container">
        <FileUploadComponent />
      </div>
    </div>
  );
}

export default ScanPage;
