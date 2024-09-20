import React from 'react';

interface ExamSheetProps {
  numQuestions: number;
  numOptions: number;
}


const ExamSheet: React.FC<ExamSheetProps> = ({ numQuestions, numOptions }) => {

  const optionsArray = Array.from({ length: numOptions }, (_, i) => String.fromCharCode(65 + i)); 

  return (
    <div className="exam-sheet">
      <h2>Custom Exam Sheet</h2>

      <div className="student-info">
        {/* Static larger boxes for student name and ID */}
        <label className="static-box-label">
          <strong>Student Name:</strong>
          <div className="static-box"></div> {/* Static large box */}
        </label>
        <label className="static-box-label">
          <strong>Student ID:</strong>
          <div className="static-box"></div> {/* Static large box */}
        </label>
      </div>

      <div className="questions">
        {Array.from({ length: numQuestions }).map((_, questionIndex) => (
          <div key={questionIndex} className="question-row">
            <span className="question-label">Question {questionIndex + 1}:</span>
            <div className="options">
              {optionsArray.map((option, optionIndex) => (
                <label key={optionIndex} className="option">
                  <div className="custom-bubble"></div> {/* Static visual bubble */}
                  <span className="bubble-label">{option}</span>
                </label>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};



export default ExamSheet;
