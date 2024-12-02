"""
This module provides functionalities to upload files.
Convert JSON to CSV and allow dowloading the CSV.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logging
import webbrowser
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
from flask_cors import CORS
from BubbleScan_AI.Scantron import Scantron95945
from BubbleScan_AI.Custom import CustomProcessor

# Define CORS origins
CORS_ORIGINS = [
    'http://localhost:5173'
]

app = Flask(__name__, static_folder='static')
CORS(app, resources={r"/*": {"origins": CORS_ORIGINS}})
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5001"}})

class AppServer:
    """
    Class for managing routes and functionalities of the Flask app.
    """
    def __init__(self, flask_app):
        """
        Initializes the AppServer class.

        Parameters:
            flask_app (Flask): The Flask application instance.
        """
        self.app = flask_app
        self.uploads_dir = os.path.join(self.app.instance_path, 'uploads')
        os.makedirs(self.uploads_dir, exist_ok=True)
        logging.basicConfig(level=logging.DEBUG)
        self.file_info = {}
        self.csv_files = {}
        self.routes()

    def routes(self):
        """
        Defines the routes for various functionalities of the app.
        """
        self.app.route('/', methods=['GET'])(self.frontend)
        self.app.route('/static/<path:path>',methods=['GET'])(self.serve_static)
        self.app.route('/assets/<path:path>',methods=['GET'])(self.serve_assets)
        self.app.route('/api/data', methods=['GET'])(self.get_data)
        self.app.route('/api/message', methods=['POST'])(self.receive_message)
        self.app.route('/api/upload', methods=['POST'])(self.file_upload)
        self.app.route('/api/process_pdf', methods=['POST'])(self.process_pdf)
        self.app.route('/api/download_csv/<file_id>', methods=['GET'])(self.download_csv)
        self.app.route('/api/csv_acknowledgment/<file_id>', methods=['POST'])(self.csv_acknowledgment)

    def frontend(self):
        """
        Serves the frontend of the web application.

        This method handles the request to the root URL and serves the main HTML file 
        (typically 'index.html') from the 'static' directory, which is the entry point 
        for the frontend of the application.

        Returns:
            Response: The HTML content of the 'index.html' file located in the 'static' directory.
        """
        print("Serving index.html from static folder")
        return send_from_directory('static', 'index.html')

    def serve_static(self,path):
        """
        Serves static files from the 'static' directory.

        This method handles requests for static files by serving them from the 'static' 
        directory based on the given path. It can serve various types of static content 
        such as JavaScript, CSS, images, etc.

        Args:
            path (str): The relative path to the static file within the 'static' directory.

        Returns:
            Response: The content of the requested static file.
        """
        return send_from_directory('static', path)

    def serve_assets(self,path):
        """
        Redirects to serve asset files from the 'assets' subdirectory within 'static'.

        This method handles requests for assets by redirecting them to the appropriate 
        static file path within the 'assets' subdirectory. It constructs the new path and 
        then uses the 'serve_static' method to serve the file.

        Args:
            path (str): The relative path to the asset file within the 'assets' subdirectory.

        Returns:
            Response: A redirect response to the constructed URL for the asset file.
        """
        return redirect(url_for('serve_static', path=f'assets/{path}'))

    def get_data(self):
        """
        Returns a simple message as JSON data.

        Returns:
            dict: JSON data with a message.
        """
        data = {"message": "Hello from Flask!"}
        return jsonify(data)

    def receive_message(self):
        """
        Receives a message from the client and logs it.

        Returns:
            dict: JSON data indicating successful message reception.
        """
        message_data = request.json
        message = message_data.get('message', '')
        print(f"Received message: {message}")
        return jsonify({"status": "success", "message": "Message received successfully!"})

    def file_upload(self):
        """
        Handles file upload requests, processes PDF files, and returns CSV data.
        Allows the user to specify whether the sheet is a standard Scantron or a custom sheet.
        """
        if 'file' not in request.files or 'sheetType' not in request.form:
            return jsonify({"status": "error", "message": "No file or sheet type in the request"})

        file = request.files['file']
        sheet_type = request.form['sheetType']  # Get the sheet type from the form

        if file.filename == '':
            return jsonify({"status": "error", "message": "No selected file"})

        if file and file.filename.lower().endswith('.pdf'):
            try:
                filename = secure_filename(file.filename)
                file_path = os.path.join(self.uploads_dir, filename)
                file.save(file_path)

                file_id = os.urandom(16).hex()
                self.file_info[file_id] = {
                    'filename': filename,
                    'path': file_path,
                    'processed': False
                }

                response_data = self.process_pdf(file_path, file_id, sheet_type)
                os.remove(file_path)

                return jsonify({"status": "success", "message": "PDF processed successfully", "file_id": file_id, "data": response_data})

            except Exception as e:
                return jsonify({"status": "error", "message": f"Error processing PDF: {e}"})

        else:
            return jsonify({"status": "error", "message": "Only PDF files are allowed"})


    def process_pdf(self, pdf_file, file_id, sheet_type):
        """
        Processes a PDF file to extract responses and convert them to CSV.

        Parameters:
            pdf_file (str): Path to the PDF file.
            file_id (str): Unique identifier for the file.
            sheet_type (str): Type of sheet (e.g., 'standard' or 'custom').

        Returns:
            str: Name of the generated CSV file.
        """
        try:
            # Choose the correct processor based on sheet type
            if sheet_type == "custom":
                processor = CustomProcessor(pdf_file)
            else:
                processor = Scantron95945(pdf_file)

            # Extract data in JSON format
            data = processor.extract_responses()

            # Transform JSON data to CSV format
            csv_data = self.transform_json_to_csv(data)
            csv_filename = f'output_{file_id}.csv'
            csv_file_path = os.path.join(self.uploads_dir, csv_filename)

            # Write CSV data to file
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                csv_file.write(csv_data)
                print(f"CSV Data written successfully to {csv_file_path}")

            # Save CSV file path for download
            self.csv_files[file_id] = {'filename': csv_filename, 'path': csv_file_path}
            self.file_info[file_id]['processed'] = True

            return csv_filename

        except Exception as e:
            logging.error("Error processing PDF: %s", e)
            return ''

    def transform_json_to_csv(self, json_data):
        """
        Transforms JSON data to CSV format.

        Parameters:
            json_data (list or dict): JSON data to be converted to CSV.

        Returns:
            str: CSV data as a string.
        """
        csv_data = ''
        print("The JSON data received is:", json_data)

        students, is_custom_sheet = self.parse_json_data(json_data)
        if students is None:
            return csv_data

        answers_keys = self.get_answer_keys(students, is_custom_sheet)
        if not answers_keys:
            print("No answers found in student data")
            return csv_data

        # Create the CSV header
        csv_data += ','.join(['studentID'] + answers_keys) + '\n'

        # Process each student's data
        for student in students:
            csv_row = self.process_student_data(student, answers_keys, is_custom_sheet)
            csv_data += csv_row + '\n'

        print("Final CSV data:\n", csv_data)
        return csv_data

    def parse_json_data(self, json_data):
        """
        Parses the input JSON data and determines the sheet type.

        Returns:
            Tuple[List[Dict], bool]: A tuple containing the list of students and
            a boolean indicating if it's a custom sheet.
        """
        if isinstance(json_data, list):  # Custom sheets
            students = json_data
            is_custom_sheet = True
        elif isinstance(json_data, dict) and 'students' in json_data:  # Standard scantron sheets
            students = json_data['students']
            is_custom_sheet = False
        else:
            print("Invalid JSON data format")
            return None, None

        if not students:
            print("No student data found")
            return None, None

        return students, is_custom_sheet

    def get_answer_keys(self, students, is_custom_sheet):
        """
        Determines the keys for answers based on sheet type.

        Returns:
            List[str]: A list of answer keys.
        """
        first_student = students[0]
        if is_custom_sheet:
            # For custom sheets, exclude 'studentID' from the keys
            answers_keys = [key for key in first_student.keys() if key != 'studentID']
        else:
            # For scantron sheets, get keys from 'answers' dictionary
            answers_keys = list(first_student.get('answers', {}).keys())
        return answers_keys

    def process_student_data(self, student, answers_keys, is_custom_sheet):
        """
        Processes individual student data to create a CSV row.

        Returns:
            str: A CSV formatted string for the student.
        """
        student_id = student.get('studentID', '')
        answers = []

        if is_custom_sheet:
            # For custom sheets, answers are at the top level
            answers_dict = student
        else:
            # For scantron sheets, answers are within the 'answers' dictionary
            answers_dict = student.get('answers', {})

        for key in answers_keys:
            answer = answers_dict.get(key, '')
            if isinstance(answer, list):
                answer = '|'.join(answer)
            elif answer is None:
                answer = ''
            answers.append(answer)

        return ','.join([student_id] + answers)

    def download_csv(self, file_id):
        """
        Allows downloading of a CSV file.

        Parameters:
            file_id (str): Unique identifier for the file.

        Returns:
            Response: Flask response object containing the CSV file.
        """
        try:
            if file_id not in self.csv_files:
                return jsonify({"status": "error", "message": "CSV file not found"})

            csv_file_data = self.csv_files[file_id]
            file_path = csv_file_data['path']
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as csv_file:
                    csv_data = csv_file.read()
                    print("CSV Data:\n", csv_data)
                return send_from_directory(self.uploads_dir, os.path.basename(file_path), as_attachment=True)
            
            return jsonify({"status": "error", "message": "CSV file not found"})

        except Exception as e:
            return jsonify({"status": "error", "message": f"Error downloading CSV: {e}"}), 500

    def csv_acknowledgment(self, file_id):
        """
        Handles acknowledgment of CSV file transmission.

        Parameters:
            file_id (str): Unique identifier for the file.

        Returns:
            dict: JSON data indicating the status of the acknowledgment.
        """
        if file_id in self.file_info:
            self.file_info[file_id]['csv_sent'] = True
            return jsonify({"status": "success", "message": "CSV is sent to the React successfully"})
        
        return jsonify({"status": "error", "message": "File ID not found"})

app_server = AppServer(app)

if __name__ == '__main__':

    # Open the browser
    webbrowser.open('http://127.0.0.1:5001')

    # Start the server
    app_server.app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
