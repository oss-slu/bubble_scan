import React, { useState } from "react";

function FileUploadComponent() {
  const [file, setFile] = useState<File | null>(null);
  const [sheetType, setSheetType] = useState<string>("scantron"); // Default to Scantron
  const [successMessage, setSuccessMessage] = useState<string>("");
  const [downloadLink, setDownloadLink] = useState<string>("");
  const [fileId, setFileId] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  // Handle file input change
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (
      selectedFile &&
      (selectedFile.type === "application/pdf" ||
        selectedFile.type.startsWith("image/"))
    ) {
      setFile(selectedFile);
      setSuccessMessage("");
      setDownloadLink("");
    } else {
      alert("Please select a valid PDF or image file.");
      if (event.target && event.target.value) {
        event.target.value = ""; // Reset file input
      }
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file) {
      alert("Please select a PDF or image file before submitting.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("sheetType", sheetType); // Include the sheet type in the form data

    try {
      const response = await fetch("http://localhost:5001/api/upload", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      if (result.status === "success") {
        setSuccessMessage("File uploaded successfully!");
        if (result.file_id) {
          setDownloadLink(`http://localhost:5001/api/download_csv/${result.file_id}`);
          setFileId(result.file_id);
        }
      } else if (result.status === "custom_sheet") {
        setSuccessMessage("Custom sheets are not yet supported.");
      } else {
        setSuccessMessage("Error: " + result.message);
      }
    } catch (error) {
      console.error("Error during file upload:", error);
      setSuccessMessage("Error during file upload.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="sheetType">Select Sheet Type:</label>
          <select id="sheetType" value={sheetType} onChange={(e) => setSheetType(e.target.value)}>
            <option value="scantron">Scantron</option>
            <option value="custom">Custom Sheet</option>
          </select>
        </div>

        <input
          type="file"
          id="file-input"
          accept=".pdf, image/*" // Accept both PDFs and images
          onChange={handleFileChange}
        />
        <button type="submit">Upload</button>
        <button
          type="button"
          onClick={() => {
            setFile(null);
            setSuccessMessage("");
            setDownloadLink("");
            setFileId("");
            const fileInput = document.getElementById("file-input") as HTMLInputElement;
            if (fileInput) fileInput.value = "";
          }}
          style={{ marginLeft: "10px" }}
        >
          Clear
        </button>
      </form>
      {loading ? (
        <div className="spinner"></div> // Show loading spinner when loading
      ) : (
        <>
          {successMessage && <p>{successMessage}</p>}
          {downloadLink && <button onClick={() => window.open(downloadLink, "_blank")}>Download CSV</button>}
        </>
      )}
    </div>
  );
}

export default FileUploadComponent;
