from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging
from werkzeug.utils import secure_filename
import csv
import uuid
import random
import string
from PyPDF2 import PdfReader
from testScantron import testScantron95945

app = Flask(__name__)

class AppServer:
    def __init__(self, flask_app):
        self.app = flask_app
        CORS(self.app)
        self.uploads_dir = os.path.join(self.app.instance_path, 'uploads')
        os.makedirs(self.uploads_dir, exist_ok=True)
        logging.basicConfig(level=logging.DEBUG)
        self.file_info = {}
        self.csv_files = {}
        self.routes()

    def routes(self):
        self.app.route('/api/data', methods=['GET'])(self.get_data)
        self.app.route('/api/message', methods=['POST'])(self.receive_message)
        self.app.route('/api/upload', methods=['POST'])(self.file_upload)
        self.app.route('/api/process_pdf', methods=['POST'])(self.process_pdf)
        self.app.route('/api/download_csv/<file_id>', methods=['GET'])(self.download_csv)
        self.app.route('/api/csv_acknowledgment/<file_id>', methods=['POST'])(self.csv_acknowledgment)

    def get_data(self):
        data = {"message": "Hello from Flask!"}
        return jsonify(data)

    def receive_message(self):
        message_data = request.json
        message = message_data.get('message', '')
        print(f"Received message: {message}")
        return jsonify({"status": "success", "message": "Message received successfully!"})

    def file_upload(self):
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file part in the request"})

        file = request.files['file']

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

                response_data = self.process_pdf(file_path, file_id)
                os.remove(file_path)

                return jsonify({"status": "success", "message": "PDF processed successfully", "file_id": file_id, "data": response_data})

            except Exception as e:
                return jsonify({"status": "error", "message": f"Error processing PDF: {e}"})

        else:
            return jsonify({"status": "error", "message": "Only PDF files are allowed"})

    def process_pdf(self, pdf_file, file_id):
        try:
            scantron = testScantron95945(pdf_file)
            data = scantron.extract_responses()
            #print("Received the JSON data as: ", data)

            csv_data = self.transform_json_to_csv(data)
            csv_filename = f'output_{file_id}.csv'
            csv_file_path = os.path.join(self.uploads_dir, csv_filename)

            with open(csv_file_path, 'w', newline='') as csv_file:
                csv_file.write(csv_data)

            self.csv_files[file_id] = {'filename': csv_filename, 'path': csv_file_path}

            self.file_info[file_id]['processed'] = True

            return csv_filename

        except Exception as e:
            logging.error("Error processing PDF: %s", e)
            return ''

    def transform_json_to_csv(self, json_data):
        csv_data = ''
        print("The JSON data received is:", json_data)
        if isinstance(json_data, dict) and 'students' in json_data:
            students = json_data['students']
            if students:
                student_data = students[0]
                if 'answers' in student_data:
                    keys = student_data['answers'].keys()
                    print("Keys:", keys)
                    csv_data += ','.join(['studentID'] + list(keys)) + '\n'
                    for student in students:
                        student_id = student.get('studentID', '')
                        answers = []
                        for key in keys:
                            answer = student['answers'].get(key, '')
                            if isinstance(answer, list):
                                answer = '|'.join(answer)
                            elif answer is None:
                                answer = ''
                            answers.append(answer)
                        print("Student ID:", student_id)
                        print("Answers:", answers)
                        csv_data += ','.join([student_id] + answers) + '\n'
                else:
                    print("No 'answers' key found in student data")
            else:
                print("No student data found")
        else:
            print("Invalid JSON data format")
        
        print("The CSV data converted is: ", csv_data)
        return csv_data


    def download_csv(self, file_id):
        try:
            if file_id not in self.csv_files:
                return jsonify({"status": "error", "message": "CSV file not found"})

            csv_file_data = self.csv_files[file_id]
            file_path = csv_file_data['path']
            
            if os.path.exists(file_path):
                with open(file_path, 'r') as csv_file:
                    csv_data = csv_file.read()
                    print("CSV Data:\n", csv_data)
                return send_from_directory(self.uploads_dir, os.path.basename(file_path), as_attachment=True)
            else:
                return jsonify({"status": "error", "message": "CSV file not found"})

        except Exception as e:
            return jsonify({"status": "error", "message": f"Error downloading CSV: {e}"}), 500

    def csv_acknowledgment(self, file_id):
        if file_id in self.file_info:
            self.file_info[file_id]['csv_sent'] = True
            return jsonify({"status": "success", "message": "CSV is sent to the React successfully"})
        else:
            return jsonify({"status": "error", "message": "File ID not found"})

if __name__ == '__main__':
    app_server = AppServer(app)
    app_server.app.run(host='0.0.0.0', port=5001, debug=True)
