<<<<<<< HEAD
import React, { useState, ChangeEvent, FormEvent } from 'react';

function FileUploadComponent() {
    const [pdfFile, setPdfFile] = useState<File | null>(null);
    const [successMessage, setSuccessMessage] = useState<string | null>(null);

    const handlePDFChange = (event: ChangeEvent<HTMLInputElement>) => {
        if (event.target.files) {
            setPdfFile(event.target.files[0]);
        }
    };

    // Helper function to clear the selected PDF file and success message
    const clearForm = () => {
        setPdfFile(null);
        setSuccessMessage(null);
    };

    // Helper function to submit the PDF file to the backend for text extraction
    const submitPDF = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();

        const formData = new FormData();
        if (pdfFile) {
            formData.append('file', pdfFile);
        }

        try {
            const response = await fetch('http://localhost:5000/api/upload', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                console.log("PDF file sent successfully");
                console.log(result.message);
                setSuccessMessage(result.message);
            } else {
                console.error('Failed to send PDF file');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                <form encType='multipart/form-data' onSubmit={submitPDF} style={{ marginBottom: '15px' }}>
                    <input type="file" name='file' accept=".pdf" onChange={handlePDFChange} />
                    <div style={{ display: 'flex', marginTop: '10px' }}>
                        <button type="submit" style={{ marginRight: '10px', padding: '5px 10px', background: '#4CAF50', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>Upload</button>
                        <button type="button" onClick={clearForm} style={{ padding: '5px 10px', background: '#f44336', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>Clear</button>
                    </div>
                </form>
                {successMessage && <p>{successMessage}</p>}
            </div>
        </>
    );
=======
import React, { useState } from "react";

function FileUploadComponent() {
  const [file, setFile] = useState<File | null>(null);
  const [successMessage, setSuccessMessage] = useState<string>("");
  const [downloadLink, setDownloadLink] = useState<string>("");
  const [fileId, setFileId] = useState<string>("");

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
      setSuccessMessage("");
      setDownloadLink("");
    } else {
      alert("Please select a PDF file.");
      if (event.target && event.target.value) {
        event.target.value = ""; // Reset file input
      }
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file) {
      alert("Please select a PDF file before submitting.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5001/api/upload", {
        method: "POST",
        body: formData,
      });
      // const result = await response.json();

      if (response.ok) {
        const result = await response.json();
        if (result.status === "success") {
          setSuccessMessage("File uploaded successfully!");
          if (result.file_id) {
            console.log("File ID:", result.file_id);
            setDownloadLink(`http://localhost:5001/api/download_csv/${result.file_id}`);
            setFileId(result.file_id);
          } else {
            setSuccessMessage("Error: CSV filename not found in the response.");
          }
        } else {
          setSuccessMessage("Error: " + result.message);
        }
      } else {
        setSuccessMessage("Upload failed.");
      }
    } catch (error) {
      console.error("Error during file upload:", error);
      setSuccessMessage("Error during file upload.");
    }
  };

  const handleDownloadCSV = async () => {
    try {
      const csvDownloadResponse = await fetch(downloadLink);

      if (csvDownloadResponse.ok) {
        const blob = await csvDownloadResponse.blob();
        const url = window.URL.createObjectURL(new Blob([blob]));
        const currentDate = new Date();
        const dateString = currentDate.toISOString().split('T')[0];
        const timeString = currentDate.toTimeString().split(' ')[0].replace(/:/g, '-');
        const filename = `data_${dateString}_${timeString}.csv`;

        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        
        // Send acknowledgment to Flask
        const acknowledgmentResponse = await fetch(`http://localhost:5001/api/csv_acknowledgment/${fileId}`, {
          method: "POST",
        });

        if (acknowledgmentResponse.ok) {
          const acknowledgmentResult = await acknowledgmentResponse.json();
          if (acknowledgmentResult.status === "success") {
            console.log("CSV acknowledgment received from Flask");
            alert("CSV file downloaded successfully!");
          } else {
            console.error("Error: ", acknowledgmentResult.message);
          }
        } else {
          console.error("Error: Failed to send CSV acknowledgment to Flask");
        }
      } else {
        console.error("Error: Failed to download CSV");
      }
    } catch (error) {
      console.error("Error during CSV download:", error);
    }
  };

  const clearForm = () => {
    setFile(null);
    setSuccessMessage("");
    setDownloadLink("");
    setFileId("");
    const fileInput = document.getElementById("file-input") as HTMLInputElement;
    if (fileInput) fileInput.value = ""; 
  };

  console.log("Download link:", downloadLink);

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          id="file-input"
          accept=".pdf"
          onChange={handleFileChange}
        />
        <button type="submit">Upload</button>
        <button
          type="button"
          onClick={clearForm}
          style={{ marginLeft: "10px" }}
        >
          Clear
        </button>
      </form>
      {successMessage && <p>{successMessage}</p>}
      {downloadLink && (
        <button onClick={handleDownloadCSV}>
          Download CSV
        </button>
      )}
    </div>
  );
>>>>>>> main
}

export default FileUploadComponent;
