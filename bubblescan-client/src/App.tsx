import React, { useEffect, useState } from "react";
import FileUploadComponent from "./components/FileUploadComponent";
import CustomSheetComponent from "./components/CustomSheetComponent"
import "./App.css";

function App() {
  const [data, setData] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const [response, setResponse] = useState<string>("");
  const [isFormVisible, setFormVisible] = useState(false);
  const [numQuestions, setNumQuestions] = useState<number>(10);  
  const [numOptions, setNumOptions] = useState<number>(4);  

  // Fetch initial data from Flask
  useEffect(() => {
    fetch("/api/data")
      .then((response) => response.json())
      .then((data) => setData(data.message))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  // Function to send message to Flask
  const sendMessage = async () => {
    console.log("Sending message to Flask...");
    try {
      const res = await fetch("/api/message", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });
      const data = await res.json();
      console.log("Message sent successfully. Response:", data);
      setResponse(data.message);
    } catch (error) {
      console.error("Error sending message:", error);
      setResponse("Failed to send message.");
    }
  };

  const handleButtonClick = () => {

    setFormVisible(true);

  }

  const handleGenerateSheet = (event: React.FormEvent) => {
    event.preventDefault();

    // Open a new window for the custom sheet
    const sheetWindow = window.open("", "_blank", "width=800,height=600");

    // Inject the custom sheet HTML into the new window
    if (sheetWindow) {
      sheetWindow.document.write(`
        <html>
          <head>
            <title>Custom Exam Sheet</title>
            <style>
              body { font-family: Arial, sans-serif; padding: 20px; }
              .student-info label { display: block; margin-bottom: 10px; }
              .question-row { margin-bottom: 15px; }
              .options { display: flex; gap: 10px; }
              .option { display: flex; align-items: center; gap: 5px; }
              .circle {
                width: 15px;
                height: 15px;
                border: 2px solid black;
                border-radius: 50%;
                display: inline-block;
              }
            </style>
          </head>
          <body>
            <h1>Custom Exam Sheet</h1>
            <div class="student-info">
              <label>Student Name: <input type="text" /></label>
              <label>Student ID: <input type="text" /></label>
            </div>
            <div class="questions">
              ${Array.from({ length: numQuestions }).map((_, questionIndex) => `
                <div class="question-row">
                  <span>Question ${questionIndex + 1}:</span>
                  <div class="options">
                    ${Array.from({ length: numOptions }).map((_, optionIndex) => `
                      <span class="option">
                        <span class="circle"></span>
                        ${String.fromCharCode(65 + optionIndex)} <!-- A, B, C, etc. -->
                      </span>
                    `).join('')}
                  </div>
                </div>
              `).join('')}
            </div>
          </body>
        </html>
      `);
      sheetWindow.document.close();
    }
    
  };

  return (
    <div className="welcome">
      <h1>Welcome to Bubble Scan</h1>
      <h4>You can upload your files below</h4>
      <FileUploadComponent />

      <h1>You can create Custom Sheets here</h1>
      <button onClick={handleButtonClick}>Custom Sheet</button>
      

      {isFormVisible && (
        <div className="custom-sheet-form">
          <h2>Enter the number of questions and options</h2>
          <form onSubmit={handleGenerateSheet}>
            <label>
              Number of Questions:
              <input
                type="number"
                value={numQuestions}
                onChange={(e) => setNumQuestions(parseInt(e.target.value))}
                min="1"
              />
            </label>
            <label>
              Number of Answer Options:
              <input
                type="number"
                value={numOptions}
                onChange={(e) => setNumOptions(parseInt(e.target.value))}
                min="2"
                max="26" // Limit to 26 options (A-Z)
              />
            </label>
            <button type="submit">Generate Exam Sheet</button>
          </form>
        </div>
      )}
    </div>
  );
}

export default App;