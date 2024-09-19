import React from 'react';

interface ExamSheetProps {
  numQuestions: number;
  numOptions: number;
}

const ExamSheet: React.FC<ExamSheetProps> = ({ numQuestions, numOptions }) => {
  const optionsArray = Array.from({ length: numOptions }, (_, i) => String.fromCharCode(65 + i)); // ['A', 'B', 'C', ...]

  return (
    <div className="exam-sheet">
      <h2>Custom Exam Sheet</h2>
      <div className="student-info">
        <label>
          Student Name: <input type="text" placeholder="Enter Student Name" />
        </label>
        <label>
          Student ID: <input type="text" placeholder="Enter Student ID" />
        </label>
      </div>

      <div className="questions">
        {Array.from({ length: numQuestions }).map((_, questionIndex) => (
          <div key={questionIndex} className="question-row">
            <span>Question {questionIndex + 1}:</span>
            <div className="options">
              {optionsArray.map((option, optionIndex) => (
                <label key={optionIndex} className="option">
                  <input type="radio" name={`question-${questionIndex}`} />
                  {option}
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
