import React, { useEffect, useState, useRef } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import FileUploadComponent from "./components/FileUploadComponent";
import CustomExamSheetComponent from "./components/CustomExamSheetComponent";
import Navbar from './components/Navbar';
import UploadPage from "./components/UploadPage";
import About from "./components/About";
import CustomExamSheetPage from "./components/CustomExamSheetPage";
import "./App.css";

function App() {
  const [data, setData] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const [response, setResponse] = useState<string>("");
  const [isFormVisible, setFormVisible] = useState(false);
  const [numQuestions, setNumQuestions] = useState<number>(5);
  const [numOptions, setNumOptions] = useState<number>(4);
  const [examTitle, setExamTitle] = useState('');
  const [component, setComponent] = useState<JSX.Element | null>(null); // Correctly typed


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


  return (

    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={
          <div className="welcome">
            <h1>Welcome to Bubble Scan</h1>
            <h3>Grading made easy</h3>
            <button onClick={() => setComponent(<FileUploadComponent />)}>Scan</button>
            <button onClick={() => setComponent(<CustomExamSheetComponent />)}>Custom Sheet</button>
            <div className="dynamic-content">
              {component}
            </div>
          </div>
        } />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/create" element={<CustomExamSheetPage />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </Router>
  );
};

export default App;