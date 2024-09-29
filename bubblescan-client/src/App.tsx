import React, { useEffect, useState, useRef } from "react";
import FileUploadComponent from "./components/FileUploadComponent";
import html2pdf from "html2pdf.js";
import "./App.css";

function App() {
  const [data, setData] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const [response, setResponse] = useState<string>("");
  const [isFormVisible, setFormVisible] = useState(false);
  const [numQuestions, setNumQuestions] = useState<number>(5);  
  const [numOptions, setNumOptions] = useState<number>(4); 
  const [examTitle, setExamTitle] = useState('');

  // Fetch initial data from Flask
  useEffect(() => {
    fetch("http://localhost:5001/api/data")
      .then((response) => response.json())
      .then((data) => setData(data.message))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  
  // Function to send message to Flask
  const sendMessage = async () => {
    console.log("Sending message to Flask...");
    try {
      const res = await fetch("http://localhost:5001/api/message", {
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
            <title>${examTitle}</title> <!-- Exam title as the HTML page title -->
            <style>
              body {
                font-family: Arial, sans-serif;
                margin: 5px;
                font-size: 8px;
                display: grid;
                grid-template-columns: 3fr 1fr; /* 3 parts for questions, 1 part for the right column */
                gap: 20px; /* Space between the question columns and the right column */
                height: 100vh;
              }
              .title {
                font-weight: bold;
                font-size: 18px;
                text-align: center;
                margin-bottom: 20px;
                grid-column: 1 / span 2; /* Span the title across both columns */
              }
              .questions-container {
                column-count: 4; /* Define number of columns for questions */
                column-gap: 15px; /* Smaller gap between columns */
                column-fill: auto; /* Fill columns vertically first */
              }
              .question {
                border: 1px solid #ddd;
                padding: 2px;
                border-radius: 3px;
                text-align: center;
                break-inside: avoid;
                margin-bottom: 2px;
                font-size: 7px;
                width: 100%;
                box-sizing: border-box;
              }
              .bubble {
                width: 5px;
                height: 5px;
                border-radius: 50%;
                border: 1px solid black;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: 6px;
                text-align: center;
                margin: 1px;
              }
              .options {
                display: flex;
                justify-content: center;
                gap: 1px;
                margin-top: 1px;
                align-items: center;
              }
              .option-label {
                margin-right: 1px;
                font-weight: bold;
                font-size: 6px;
              }
              .right-column {
                border-left: 1px solid #ddd;
                padding-left: 10px;
              }
              .id-container {
                margin-top: 20px;
              }
              .id-header {
                font-weight: bold;
                text-align: center;
                font-size: 9px;
                margin-bottom: 10px;
              }
              .id-row {
                display: flex;
                justify-content: space-around;
                margin-bottom: 10px;
              }
              .id-column {
                display: flex;
                flex-direction: column;
                align-items: center;
              }
              .id-bubble {
                width: 10px; /* Increased size for the student ID bubbles */
                height: 10px; /* Increased size for the student ID bubbles */
                border-radius: 50%;
                border: 1px solid black;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: 6px; /* Keep the font size same for readability */
                text-align: center;
                margin: 2px; /* Slightly larger margin */
              }
              .key-id-container {
                margin-top: 20px;
                border: 1px solid #ddd;
                padding: 10px;
                text-align: center;
                border-radius: 5px;
                width: 120px;
                margin-left: auto;
                margin-right: auto;
              }
              .key-id-header {
                font-weight: bold;
                font-size: 8px;
                margin-bottom: 5px;
              }
              .key-id-options {
                display: flex;
                justify-content: space-between;
                gap: 5px;
              }
            </style>
          </head>
          <body>
            <div class="title">${examTitle}</div> <!-- Title added here in the body -->
            <div class="questions-container">
              ${Array.from({ length: numQuestions }, (_, i) => `
                <div class="question">
                  <strong>${i + 1}.</strong><br/>
                  <div class="options">
                    ${Array.from({ length: numOptions }, (__, j) => `
                      <span class="option-label">${String.fromCharCode(65 + j)}</span>
                      <div class="bubble"></div>
                    `).join('')}
                  </div>
                </div>
              `).join('')}
            </div>
            
            <div class="right-column">
              <h2>Student ID</h2>
              <div class="id-container">
                <div class="id-header">STUDENT ID NUMBER</div>
                <div class="id-row">
                  ${Array.from({ length: 10 }, (_, i) => `
                    <div class="id-column">
                      ${Array.from({ length: 10 }, (_, j) => `
                        <div class="id-bubble">${j}</div> <!-- Number inside the bubble -->
                      `).join('')}
                    </div>
                  `).join('')}
                </div>
              </div>
              <!-- KEY ID section -->
              <div class="key-id-container">
                <div class="key-id-header">KEY ID</div>
                <div class="key-id-options">
                  ${['A', 'B', 'C', 'D'].map(option => `
                    <div>
                      <span class="option-label">${option}</span>
                      <div class="bubble"></div>
                    </div>
                  `).join('')}
                </div>
              </div>
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
      <form onSubmit={handleGenerateSheet}>
        <label>
          Exam Title: {/* New input field for the exam title */}
          <input
            type="text"
            value={examTitle}
            onChange={(e) => setExamTitle(e.target.value)}
            placeholder="Enter exam title"
            required
          />
        </label>
        <label>
          Number of Questions:
          <input
            type="number"
            value={numQuestions}
            onChange={(e) => setNumQuestions(parseInt(e.target.value))}
            min="1"
            required
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
            required
          />
        </label>
        <button type="submit">Generate Exam Sheet</button>
      </form>
    </div>
  );
};

export default App;