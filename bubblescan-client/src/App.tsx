import React, { useEffect, useState } from "react";
import FileUploadComponent from "./components/FileUploadComponent";
import "./App.css";

function App() {
  const [data, setData] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const [response, setResponse] = useState<string>("");

  // Fetch initial data from Flask
  useEffect(() => {
    console.log("Fetching initial data...");
    fetch("http://localhost:5001/api/data")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Data received:", data);
        setData(data.message)})
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
    <div className="welcome">
      <h1>Welcome to Bubble Scan</h1>
      <h4>You can upload your files below</h4>
      <FileUploadComponent />
    </div>
  );
}

export default App;