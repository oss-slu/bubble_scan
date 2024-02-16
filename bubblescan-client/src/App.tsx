import ListGroup from "./components/ListGroup";
import InputComponent from "./components/InputComponent";
import FileUploadComponent from "./components/FileUploadComponent";
import "./App.css";

function App() {
  return (
    <div>
      <h1>Welcome To Bubble Scan</h1>
      <h2>What is your First and Last Name?</h2>
      <InputComponent />
      <h2>You can upload your files below</h2>
      <FileUploadComponent />
      <p>Response from Flask: {data}</p>
      <div>
        <h3>Send a Message to Flask</h3>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message here"
        />
        <button onClick={sendMessage}>Send Message</button>
        {response && <p>Response from sending message: {response}</p>}
      </div>
      <ListGroup />
      <h3>What is your First and Last Name?</h3>
      <InputComponent />
      <h3>You can upload your files below</h3>
      <FileUploadComponent />
    </div>
  );
}

export default App;
