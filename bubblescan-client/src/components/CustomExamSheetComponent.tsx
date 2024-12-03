import React, { useState } from "react";

function CustomExamSheetComponent() {
  const [numQuestions, setNumQuestions] = useState<number>(5);
  const [numOptions, setNumOptions] = useState<number>(4);
  const [examTitle, setExamTitle] = useState("");

  const generateExam = () => {
    const examWindow = window.open("", "Exam", "width=800,height=600");
    const examContent = `
      <html>
        <head>
          <title>${examTitle}</title> <!-- Exam title as the HTML page title -->
          <style>
            body {
              font-family: Arial, sans-serif;
              margin: 5px;
              font-size: 9px;
              display: grid;
              grid-template-columns: 1fr; /* Single column grid */
              grid-template-rows: auto auto; /* Auto height for header, rest for content */
              gap: 20px;
              height: 100vh;
              position: relative;
              align-content: start;
            }
            @media print {
              body {
                margin: 0;
                height: 100vh;
                overflow: hidden;
              }
              .title, .questions-container, .student-id-container {
                page-break-inside: avoid;
              }
            }
			  .title {
              font-weight: bold;
              font-size: 20px;
              text-align: center;
              margin-bottom: 20px;
              grid-column: 1 / span 2;
            }
            /* Header container for Key ID and Title */
            .header-container {
              display: flex;
              align-items: center;
              margin-bottom: 20px;
			  marign-top: 50px;
            }
            .key-id-container {
              flex: 0 0 auto; /* Do not grow */
              margin-right: 20px; /* Space between Key ID and Title */
              border: 1px solid #ddd;
              padding: 10px;
              text-align: center;
              border-radius: 5px;
              width: 140px;
			  margin-right: 70px;
            }
            .key-id-header {
              font-weight: bold;
              font-size: 10px;
              margin-bottom: 5px;
            }
            .key-id-options {
              display: flex;
              justify-content: space-between;
              gap: 5px;
            }
            .key-id-container .bubble {
              width: 15px;
              height: 11px;
              border-radius: 50%;
              border: 1px solid black;
              display: inline-flex;
              align-items: center;
              justify-content: center;
              font-size: 6px;
              text-align: center;
              margin-left: 1px;
              margin-right: 0;
            }
            .title {
              flex: 1; /* Allow Title to grow and fill the space */
              font-weight: bold;
              font-size: 20px;
              text-align: left; /* Align text to the left */
              margin: 0;
            }
            .questions-container {
              column-count: 4;
              -webkit-column-count: 4;
              column-gap: 12px;
              -webkit-column-gap: 12px;
              column-fill: auto;
              -webkit-column-fill: auto;
              min-height: 200px;
            }
            .question:nth-child(25) {
              break-after: column;
              -webkit-column-break-after: column;
            }
            .question {
              display: flex;
              align-items: center;
              padding: 3px;
              margin-bottom: 2px;
              font-size: 9px;
              box-sizing: border-box;
            }
            .question-label {
              font-weight: bold;
              margin-right: 4px;
              font-size: 10px;
              width: 20px;
              text-align: right;
            }
            .questions-container .bubble {
              width: 17px;
              height: 12px;
              border-radius: 50%;
              border: 1px solid black;
              display: inline-flex;
              align-items: center;
              justify-content: center;
              font-size: 7px;
              text-align: center;
              margin: 1px;
            }
            .options {
              display: flex;
              gap: 2px;
              align-items: center;
            }
            .student-id-container {
              position: absolute;
              top: 70%;
              left: 8%;
              transform: translateX(-25%);
              z-index: 1000;
              border: 1px solid #ddd;
              padding: 10px;
              background-color: white;
              border-radius: 8px;
              width: 200px;
              text-align: center;
            }
            .id-header {
              font-weight: bold;
              text-align: center;
              font-size: 12px;
              margin-bottom: 10px;
            }
            .id-inputs {
              display: flex;
              justify-content: space-around;
              margin-bottom: 5px;
            }
            .id-input {
              width: 16px;
              height: 22px;
              border: 1px solid black;
              border-radius: 3px;
              text-align: center;
              font-size: 12px;
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
              width: 12px;
              height: 9px;
              border-radius: 50%;
              border: 1px solid black;
              display: inline-flex;
              align-items: center;
              justify-content: center;
              font-size: 8px;
              text-align: center;
              margin: 2px;
            }
            .info-container {
              display: flex;
              flex-direction: column;
              margin-top: 15px;
              border: 1px solid green;
              width: 350px;
              padding: 5px;
              text-align: left;
              position: absolute;
              top: 8%;
              left: 48%;
            }
            .info-item {
              border-bottom: 1px solid green;
              padding: 8px;
              text-align: left;
              font-size: 10px;
              font-weight: bold;
              background-color: white;
              color: green;
            }
            .info-item:last-child {
              border-bottom: none;
            }
          </style>
        </head>
        <body>
          <div class="header-container">
            <!-- KEY ID section -->
            <div class="key-id-container">
              <div class="key-id-header">KEY ID</div>
              <div class="key-id-options">
                ${["A", "B", "C", "D"]
        .map(
          (option) => `
                    <div>
                      <div class="bubble">${option}</div>
                    </div>
                  `
        )
        .join("")}
              </div>
            </div>
            <!-- Title -->
            <div class="title">${examTitle}</div>
          </div>

          <!-- Questions section -->
          <div class="questions-container">
            ${Array.from(
          { length: numQuestions },
          (_, i) => `
                <div class="question">
                  <span class="question-label">${i + 1}.</span>
                  <div class="options">
                    ${Array.from(
            { length: numOptions },
            (__, j) => `
                        <div class="bubble">${String.fromCharCode(65 + j)}</div>
                      `
          ).join("")}
                  </div>
                </div>
              `
        ).join("")}
          </div>

          <!-- Student Info section -->
          <div class="student-info-container">
            <!-- Student ID section -->
            <div class="student-id-container">
              <div class="id-header">STUDENT ID NUMBER</div>
              <div class="id-inputs">
                ${Array.from({ length: 10 })
        .map(
          () => `
                    <input type="text" class="id-input" maxlength="1" />
                  `
        )
        .join("")}
              </div>
              <div class="id-row">
                ${Array.from(
          { length: 10 },
          (_, i) => `
                    <div class="id-column">
                      ${Array.from(
            { length: 10 },
            (_, j) => `
                          <div class="id-bubble">${j}</div>
                        `
          ).join("")}
                    </div>
                  `
        ).join("")}
              </div>
            </div>

            <!-- Name, Date, Subject section -->
            <div class="info-container">
              <div class="info-item">NAME:</div>
              <div class="info-item">DATE:</div>
              <div class="info-item">SUBJECT:</div>
            </div>
          </div>

        </body>
      </html>
    `;

    examWindow?.document.write(examContent);
    localStorage.setItem("storedExam", examContent);
    examWindow?.document.close();
  };

  const printStoredExam = () => {
    const storedExam = localStorage.getItem("storedExam");
    if (storedExam) {
      const examWindow = window.open("", "Stored Exam", "width=800,height=600");
      examWindow?.document.write(storedExam);
      examWindow?.document.close();
      examWindow?.focus();
      examWindow?.print();
    } else {
      alert("No stored exam found.");
    }
  };

  return (
    <div className="customsheet">
      <h2>You can create Custom Sheets here</h2>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          generateExam();
        }}
        style={{ display: "flex", flexDirection: "column", gap: "1rem" }}
      >
        <label style={{ display: "flex", gap: "10rem", width: "100%", alignItems: "center" }}>
          ExamTitle:
          <input
            type="text"
            value={examTitle}
            onChange={(e) => setExamTitle(e.target.value)}
            placeholder="Enter exam title"
            required
          />
        </label>
        <label style={{ display: "flex", gap: "10rem", width: "100%", alignItems: "center" }}>
          Number of Questions:
          <input
            type="number"
            value={numQuestions}
            onChange={(e) => setNumQuestions(parseInt(e.target.value))}
            min="1"
            required
          />
        </label>
        <label style={{ display: "flex", gap: "10rem", width: "100%", alignItems: "center" }}>
          Number of Answer Options:
          <input
            type="number"
            value={numOptions}
            onChange={(e) => setNumOptions(parseInt(e.target.value))}
            min="2"
            max="26"
            required
          />
        </label>

      </form>
      <div style={{ display: "flex ", justifyContent: "space-around" }}>
        <button type="submit">Generate Exam Sheet</button>
        <button onClick={printStoredExam}>Print Stored Exam</button>

      </div>
    </div>
  );
}

export default CustomExamSheetComponent;
