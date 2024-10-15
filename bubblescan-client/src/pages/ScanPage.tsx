import React from "react";
import FileUploadComponent from "../components/FileUploadComponent";
import CustomExamSheetComponent from "../components/CustomExamSheetComponent";

function ScanPage() {
  return (
    <div className="scan-page">
      <h1>Scan Your Sheets Here</h1>
      <p>You can upload your files below</p>
      <FileUploadComponent />
      <CustomExamSheetComponent />
    </div>
  );
}

export default ScanPage;
