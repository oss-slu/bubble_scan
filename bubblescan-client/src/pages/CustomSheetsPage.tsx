import React from "react";
import CustomExamSheetComponent from "../components/CustomExamSheetComponent";

function CustomSheetsPage() {
  return (
    <div className="scan-page">
      <h1>Create Custom Sheets Here</h1>
      <p>You can generate your custom exam sheets below</p>
      <div className="file-upload-container">
        <CustomExamSheetComponent />
      </div>
    </div>
  );
}

export default CustomSheetsPage;
