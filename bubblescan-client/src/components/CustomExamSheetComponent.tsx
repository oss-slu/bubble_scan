import React, { useState, useEffect } from "react";

function CustomExamSheetComponent()	{

	const [isFormVisible, setFormVisible] = useState(false);
	const [numQuestions, setNumQuestions] = useState<number>(5);  
	const [numOptions, setNumOptions] = useState<number>(4); 
	const [examTitle, setExamTitle] = useState('');

	const handleButtonClick = () => {

		setFormVisible(true);
	
	  }
	
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
					font-size: 9px; /* Slightly increased base font size */
					display: grid;
					grid-template-columns: 1fr 3fr; /* 1 part for Key ID, 3 parts for questions */
					grid-template-rows: auto auto; /* Auto height for Key ID, rest for questions */
					gap: 20px;
					height: 100vh;
					position: relative;
					align-content: start;
				  }
				  @media print {
					/* Force content to fit into a single page */
					body {
					  margin: 0;
					  height: 100vh; /* Ensures content fits within one view height */
					  overflow: hidden; /* Prevents overflow from creating a second page */
					}
					/* Avoid page breaks inside elements */
					.title, .questions-container, .student-id-container {
					  page-break-inside: avoid;
					}
				  }
				  .title {
					font-weight: bold;
					font-size: 20px; /* Slightly larger title */
					text-align: center;
					margin-bottom: 20px;
					grid-column: 1 / span 2; /* Span the title across both columns */
				  }
				  .questions-container {
					column-count: 4;
					column-gap: 12px;
					column-fill: auto;
					min-height: 200px; /* Ensure there's enough vertical space */
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
					width: 20px; /* Fixed width to handle both one- and two-digit numbers */
					text-align: right;
				  }
				  /* Larger bubbles only for the questions section */
				  .questions-container .bubble {
					width: 10px; /* Larger bubbles */
					height: 10px; /* Larger bubbles */
					border-radius: 50%;
					border: 1px solid black;
					display: inline-flex;
					align-items: center;
					justify-content: center;
					font-size: 7px; /* Slightly larger font inside bubbles */
					text-align: center;
					margin: 1px; /* Reduced margin between bubbles */
				  }
				  .questions-container .option-label {
					margin-right: 2px; /* Reduced margin between label and bubble */
				  }
				  .options {
					display: flex;
					gap: 2px; /* Adjust gap for slightly larger bubbles and labels */
					align-items: center;
				  }
				  .option-label {
					margin-right: 1px; /* Slightly larger margin */
					font-weight: bold;
					font-size: 9px; /* Slightly larger font size for option labels */
				  }
	  
				  .right-column {
					border-left: 1px solid #ddd;
					padding-left: 10px;
				  }
	  
				  /* Positioning the student ID section next to the second row of questions */
				  .student-id-container {
					position: absolute;
					top: 15%; /* Adjusted to be slightly lower */
					left: 55%; /* Keep the horizontal alignment the same */
					transform: translateX(-25%); /* Shift further toward the center */
					z-index: 1000; /* Ensure it's on top */
					border: 1px solid #ddd;
					padding: 10px; /* Smaller padding */
					background-color: white; /* Add background color to avoid text interference */
					border-radius: 8px;
					width: 180px; /* Smaller width */
					text-align: center;
				  }
				  .id-header {
					font-weight: bold;
					text-align: center;
					font-size: 12px; /* Slightly larger font for ID header */
					margin-bottom: 10px;
				  }
				  .id-inputs {
					display: flex;
					justify-content: space-around;
					margin-bottom: 5px;
				  }
				  .id-input {
					width: 16px; /* Increased width */
					height: 22px; /* Increased height */
					border: 1px solid black;
					border-radius: 3px;
					text-align: center;
					font-size: 12px; /* Larger font size */
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
				  /* Original bubbles for the Key ID and Student ID sections */
				  .key-id-options div {
					display: flex;
					align-items: center; /* Align bubbles and letters vertically */
					justify-content: center; /* Align bubbles and letters horizontally */
				  }
	
				  .key-id-container .bubble {
					width: 7px; /* Standard size bubbles for these sections */
					height: 7px;
					border-radius: 50%;
					border: 1px solid black;
					display: inline-flex;
					align-items: center;
					justify-content: center;
					font-size: 6px;
					text-align: center;
					margin-left: 2px; /* Reduce space between letter and bubble */
					margin-right: 0;  /* No extra space on the right side */
				  }

				  .id-bubble {
					width: 12px; /* Adjust the size as needed */
					height: 12px; /* Adjust the size as needed */
					border-radius: 50%; /* Makes the bubble round */
					border: 1px solid black; /* Defines the border for the bubble */
					display: inline-flex;
					align-items: center;
					justify-content: center;
					font-size: 8px; /* Adjust the font size for the number inside */
					text-align: center;
					margin: 2px; /* Adjust spacing between the bubbles */
					}
	  
				  /* Additional section below the student ID for Name, Date, and Subject */
				  .info-container {
					display: flex;
					flex-direction: column;
					margin-top: 15px;
					border: 1px solid green;
					width: 100%; /* Match the width of the Student ID section */
					padding: 5px;
					text-align: left;
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
	  
				  .key-id-container {
					grid-column: 1; /* Place it in the first column */
					grid-row: 1; /* Place it in the first row */
					border: 1px solid #ddd;
					padding: 10px;
					text-align: center;
					border-radius: 5px;
					width: 140px; /* Slightly larger width */
					margin-bottom: 10px;
				  }
				  .key-id-header {
					font-weight: bold;
					font-size: 10px; /* Slightly larger font for Key ID header */
					margin-bottom: 5px;
				  }
				  .key-id-options {
					display: flex;
					justify-content: space-between;
					gap: 5px; /* Adjust gap for slightly larger bubbles */
				  }
				</style>
			  </head>
			  <body>
				<div class="title">${examTitle}</div> <!-- Title added here in the body -->
	  
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
	  
				<!-- Questions section -->
				<div class="questions-container">
				  ${Array.from({ length: numQuestions }, (_, i) => `
					<div class="question">
					  <span class="question-label">${i + 1}.</span> <!-- Question label on the left -->
					  <div class="options">
						${Array.from({ length: numOptions }, (__, j) => `
						  <span class="option-label">${String.fromCharCode(65 + j)}</span>
						  <div class="bubble"></div>
						`).join('')}
					  </div>
					</div>
				  `).join('')}
				</div>
	  
				<!-- Student ID section -->
				<div class="student-id-container">
				  <div class="id-header">STUDENT ID NUMBER</div>
				  <!-- Add input boxes above bubbles -->
				  <div class="id-inputs">
					${Array.from({ length: 10 }).map(() => `
					  <input type="text" class="id-input" maxlength="1" />
					`).join('')}
				  </div>
				  <div class="id-row">
					${Array.from({ length: 10 }, (_, i) => `
					  <div class="id-column">
						${Array.from({ length: 10 }, (_, j) => `
						  <div class="id-bubble">${j}</div> <!-- Number inside the bubble -->
						`).join('')}
					  </div>
					`).join('')}
				  </div>
	  
				  <!-- Additional vertical section for Name, Date, and Subject -->
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
		localStorage.setItem("storedExam", examContent); // Store the exam
		examWindow?.document.close();
	};
	
	  const loadStoredExam = () => {
		const storedExam = localStorage.getItem("storedExam");
		if (storedExam) {
		  const examWindow = window.open("", "Stored Exam", "width=800,height=600");
		  examWindow?.document.write(storedExam);
		  examWindow?.document.close();
		} else {
		  alert("No stored exam found.");
		}
	  };
	
	  const printStoredExam = () => {
		const storedExam = localStorage.getItem("storedExam");
		if (storedExam) {
		  const examWindow = window.open("", "Stored Exam", "width=800,height=600");
		  examWindow?.document.write(storedExam);
		  examWindow?.document.close();
		  examWindow?.focus();
		  examWindow?.print(); // Automatically open the print dialog
		} else {
		  alert("No stored exam found.");
		}
	  };
	
	
	  return (
		<div className="container">
      <form onSubmit={generateExam} className="exam-form">
        <div className="form-group">
          <label htmlFor="examTitle">Exam Title:</label>
          <input
            id="examTitle"
            type="text"
            value={examTitle}
            onChange={(e) => setExamTitle(e.target.value)}
            placeholder="Enter exam title"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="numQuestions">Number of Questions:</label>
          <input
            id="numQuestions"
            type="number"
            value={numQuestions}
            onChange={(e) => setNumQuestions(parseInt(e.target.value))}
            min="1"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="numOptions">Number of Answer Options:</label>
          <input
            id="numOptions"
            type="number"
            value={numOptions}
            onChange={(e) => setNumOptions(parseInt(e.target.value))}
            min="2"
            max="26"
            required
          />
        </div>
        <div className="button-group">
          <button type="submit">Generate Exam Sheet</button>
          <button type="button" onClick={printStoredExam}>
            Print Stored Exam
          </button>
        </div>
      </form>
    </div>
	  );


}

  
  export default CustomExamSheetComponent;
  

