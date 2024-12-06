# Bubblescan

### Project Overview
The chemistry department at SLU uses paper scantron (fill-in-the-bubble) sheets for exams. To grade exams, they physically take the papers to one of the two machines on campus capable of processing the data. This process is time-consuming and a bit risky - the machines are getting old and might break. In general, they like using paper-based fill-in-the-bubble exams but are interested in digitizing the grading process through software that presents them with detailed results, similar to the results they get from the physical scantron machines. The specific sheets used by the chemistry department are Scantron form number 95945. While not hugely expensive, not having to order such sheets is a cost-saving. Most importantly, this software would replace the technology that's becoming obsolete and simplify the grading process. 


This project automates the scanning of Scantron documents and the extraction of data to CSV files using a web-based application. Users can upload scanned images of their Scantron forms, which are then processed by our backend AI algorithms to generate and retrieve CSV files containing the extracted data. This system is designed for educational institutions and testing centers to streamline their grading processes and data management.

### Software Architecture

![Optional Alt Text](inputData/architecture.jpg)

##### Prerequisites

Before you begin, ensure you have the following software installed on your system:
- Node.js (including npm)
- Python 3.6 or newer
- Git

### Environment Setup

If you want to run the app locally, you will need two terminals to get Bubble scan set up. One for the React component, and other for the Flask component.

#### React Application Setup

This project was bootstrapped with [Vite](https://vitejs.dev/). It is a simple setup to get started with React and Vite.

First, clone the repository and navigate into the project directory:

```bash
git clone <your-repository-url>
cd <your-project-name>

npm install
npm install cors
npm run build
npm run dev
```
Your React application will be accessible at `http://localhost:5173/`.
#### Flask Application Setup
##### Prerequisites
This guide provides step-by-step instructions for setting up a Flask application within a virtual environment. This ensures that your project dependencies are managed efficiently without affecting other Python projects.

Before you start, make sure you have Python installed on your system. Flask supports Python 3.6 and newer.

#### Step 1: Go into ServerCode folder

```bash
cd ServerCode/application
```

#### Step 2: Create the Virtual Environment
- **On macOS and Linux:**

  ```bash
  python3 -m venv venv
  ```

- **On Windows:**

  ```bash
  python -m venv venv
  ```


#### Step 3: Activate the Virtual Environment

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

#### Step 4: Install Flask or dependencies

With the virtual environment activated, install all the requirements using pip:

```bash
pip3 install -r requirements.txt
```

#### Step 5: Run Your Flask Application

**You must run the App server i.e `AppServer.py` to run the app**

You can run your Flask applications using the `AppServer.py` file as your entry point:

```bash
python3 AppServer.py
```

Your App server Flask application will be accessible at `http://127.0.0.1:5001/`.

#### Step 6: Deactivate the Virtual Environment

When you're done working on your project, you can deactivate the virtual environments by running:

```bash
deactivate
```

This command will return you to your system's default Python interpreter.

### Usage

**Uploading a scantron document:**

1. Navigate to `http://localhost:5173/`
2. Follow the prompts to upload a scanned image of the Scantron document.

**Initiating the Scanning process**

Once the document is uploaded, the processing starts automatically.

**Retrieving the generated CSV file**

Upon completion, a link to download the CSV file will be available directly on the web interface. 

## Docker Set Up
**Make sure your docker file exists in the root directory and your docker is active.**
The docker file helps running the app in a single server. Follow the commands below:
```
cd bubble_scan

// Build the docker image
docker build -t bscan .

// Run the docker container
docker run -p 5001:5001 -p 5173:5173 bscan
```
Your bubble scan application will be accessible at `http://127.0.0.1:5001/`.

## How to run the Excecutable

**How to run the script**

```bash

chmod +x Bubblescan.sh
./Bubblescan.sh

```
**Bubblescan.exe will be in the dist folder in BubbleScan/ServerCode/dist**


## Upcoming Features: Custom Sheet Processing
**Description**
The program will allow the users to create custom sheets based on the amount of questions and answer choices the user desires. These sheets will then be seamlesssly processed in the program.

**Key Development Milestones**
- Adding frontend functinality to create custom sheets and preview them
