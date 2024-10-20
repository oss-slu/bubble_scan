import React, { useState } from "react";

function FileUploadComponent() {
  const [file, setFile] = useState<File | null>(null);
  const [successMessage, setSuccessMessage] = useState<string>("");

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setSuccessMessage("");
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file) {
      alert("Please select a file before submitting.");
      return;
    }

    // Simulate file upload
    setSuccessMessage("File uploaded successfully!");
  };

  const clearForm = () => {
    setFile(null);
    setSuccessMessage("");
    const fileInput = document.getElementById("file-input") as HTMLInputElement;
    if (fileInput) fileInput.value = "";
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          id="file-input"
          onChange={handleFileChange}
          accept=".pdf, image/*" // Accept PDFs and images
        />
        <div className="button-group">
          <button type="submit">Upload</button>
          <button type="button" onClick={clearForm}>
            Clear
          </button>
        </div>
      </form>
      {successMessage && <p className="success-message">{successMessage}</p>}
    </div>
  );
}

export default FileUploadComponent;
