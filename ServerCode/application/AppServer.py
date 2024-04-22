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

class AppServer:
    def __init__(self):
        self.app = Flask(__name__)
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
            reader = PdfReader(pdf_file)
            num_pages = len(reader.pages)
            student_data_list = []

            for i in range(num_pages):
                student_data = self.generate_student_data()
                student_data_list.append(student_data)

            csv_data = self.transform_json_to_csv(student_data_list)
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

    def generate_student_data(self):
        student_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        answers = {f"Q{k+1}": f"Answer_{chr(65 + k % 5)}" for k in range(20)}
        return {"studentID": student_id, "answers": answers}

    def transform_json_to_csv(self, json_data):
        csv_data = ''
        if isinstance(json_data, list):
            if json_data:
                if 'answers' in json_data[0]:
                    keys = json_data[0]['answers'].keys()
                    csv_data += ','.join(['studentID'] + list(keys)) + '\n'
                    for student in json_data:
                        csv_data += ','.join([student['studentID']] + [student['answers'].get(key, '') for key in keys]) + '\n'

        return csv_data

    def download_csv(self, file_id):
        try:
            if file_id not in self.csv_files:
                return jsonify({"status": "error", "message": "CSV file not found"})

            csv_file_data = self.csv_files[file_id]
            file_path = csv_file_data['path']
            
            if os.path.exists(file_path):
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
    app_server = AppServer()
    app_server.app.run(debug=True, port=5001)
