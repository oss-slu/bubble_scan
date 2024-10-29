import React, { useEffect, useState, useRef } from "react";
import FileUploadComponent from "./components/FileUploadComponent";
import CustomExamSheetComponent from "./components/CustomExamSheetComponent";
import config from "./utils/config";

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
    fetch(`${config.apiBaseUrl}/api/data`)
      .then((response) => response.json())
      .then((data) => setData(data.message))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  
  // Function to send message to Flask
  const sendMessage = async () => {
    console.log("Sending message to Flask...");
    try {
      const res = await fetch(`${config.apiBaseUrl}/api/message`, {
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
    <div className="welcome">
      <h1>Welcome to Bubble Scan</h1>
      <h4>You can upload your files below</h4>
      <FileUploadComponent />

      
      <CustomExamSheetComponent />
    </div>
  );
};

export default App;
