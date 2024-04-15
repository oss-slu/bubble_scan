# Bubblescan

## Project Overview
This project automates the scanning of Scantron documents and extraction of data to CSV files using a web-based application. Users can upload scanned images of their Scantron forms, which are then processed by our backend AI algorithms to generate and retrieve CSV files containing the extracted data. This system is designed for educational institutions and testing centers to streamline their grading processes and data management.

This project was bootstrapped with [Vite](https://vitejs.dev/). It is a simple setup to get started with React and Vite.

## Prerequisites

Before you begin, ensure you have the following software installed on your system:
- Node.js (including npm)
- Python 3.6 or newer
- Git

## React Environment Setup

**Start by cloning the repository to your local machine and navigating into the project directory:**

```bash
git clone <your-repository-url>
cd <your-project-name>
```

**Go to the bubblescan directory and run the React component using below commands**

```
cd bubblescan-client
npm install
npm install cors
npm run dev
```
**The React component is accessible at**
```bash
http://localhost:5173/
```

**You must run the App server i.e `AppServer.py` to run the app**

## Flask Application Setup

This guide provides step-by-step instructions for setting up a Flask application within a virtual environment. This ensures that your project dependencies are managed efficiently without affecting other Python projects.

## Prerequisites

Before you start, make sure you have Python installed on your system. Flask supports Python 3.6 and newer.

### Step 1: Go into ServerCode folder

```bash
cd ServerCode/application
```

### Step 2: Create the Virtual Environment

- **On macOS and Linux:**
```bash
python3 -m venv venv
```
- **On Windows:**
```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

Before you can start using the virtual environment, you need to activate it. The command varies depending on your operating system.

- **On Windows:**

  ```cmd
  .\env\Scripts\activate
  ```

- **On macOS and Linux:**

  ```bash
  source venv/bin/activate
  ```

You'll know the virtual environment is activated because its name will appear at the beginning of the terminal prompt.

### Step 4: Install Flask or dependencies

With the virtual environment activated, install Flask using pip:

```bash
pip install Flask

pip3 install -r requirements.txt
```

### Step 5: Run Your Flask Application

You can run your Flask applications using the `AppServer.py` file as your entry point:

```bash
python3 AppServer.py
```

Your App server Flask application will be accessible at `http://127.0.0.1:5001/`.

### Step 7: Deactivate the Virtual Environment

When you're done working on your project, you can deactivate the virtual environments by running:

```bash
deactivate
```

This command will return you to your system's default Python interpreter.

## Usage

**Uploading a scantron document**

1. Navigate to 'http://localhost:5173/'
2. Follow the prompts to upload a scanned image of the Scantron document.

**Initiating the Scanning process**

Once the document is uploaded, the processing starts automatically.

**Retrieving the generated CSV file**

Upon completion, a link to download the CSV file will be available directly on the web interface. 