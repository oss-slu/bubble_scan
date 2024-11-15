import React, { useEffect, useState, useRef } from "react";
import FileUploadComponent from "./components/FileUploadComponent";
import CustomExamSheetComponent from "./components/CustomExamSheetComponent";
import config from "./utils/config";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import Header from "./components/Header";
import Home from "./components/Home";
import Footer from "./components/Footer"; 
import AboutUs from "./components/AboutUs"; 


function App() {
  const [data, setData] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const [response, setResponse] = useState<string>("");
  const [isFormVisible, setFormVisible] = useState(false);
  const [numQuestions, setNumQuestions] = useState<number>(5);
  const [numOptions, setNumOptions] = useState<number>(4);
  const [examTitle, setExamTitle] = useState("");

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
    // <>
    // <Header />
    //   <div className="welcome">

    //     <h1>Welcome to Bubble Scan</h1>
    //     <h4>You can upload your files below</h4>
    //     <FileUploadComponent />

    //     <CustomExamSheetComponent />
    //   </div>
    //   </>
    <Router>
      <div className="main-container">
        <Header />
        <div className="main-content">
          <div className="appContent">
            <div>
              <Routes>
                <Route path = "/" element = {<Home />}/>
                <Route path = "/custom-sheets" element = {<CustomExamSheetComponent />}/>
                <Route path = "/scan-sheets" element = {<FileUploadComponent />}/>
                <Route path = "/about-us" element = {<AboutUs />}/>
              </Routes>
            </div>
          </div>
        </div>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
