import React from "react";
import FileUploadComponent from "./FileUploadComponent";

function UploadPage() {
    return (
        <div className="welcome">
            <h1>Upload Your Files</h1>
            <h4>You can upload your files below:</h4>
            <FileUploadComponent />
        </div>
    );
}

export default UploadPage;