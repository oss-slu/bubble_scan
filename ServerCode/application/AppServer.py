from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging
from werkzeug.utils import secure_filename
import json
import uuid

# Assuming that Scantron95945 is the class from your provided Bubble_Scan_AI code
#from BubbleScan-AI.Bubble_Scan_AI import Scantron95945

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

                file_id = uuid.uuid4().hex
                self.file_info[file_id] = {
                    'filename': filename,
                    'path': file_path,
                    'processed': False
                }

                # Process the PDF using Scantron95945
                scantron_processor = Scantron95945(file_path)
                response_data = scantron_processor.final_output

                # Assuming that the data is processed into a CSV and saved at 'result_data.json'
                with open('result_data.json', 'r') as json_file:
                    json_data = json.load(json_file)
                csv_filename = self.transform_json_to_csv(json_data["students"], f'{file_id}.csv')

                os.remove(file_path)  # Optional: Remove the original PDF file

                return jsonify({"status": "success", "message": "PDF processed successfully", "file_id": file_id, "data": csv_filename})

            except Exception as e:
                return jsonify({"status": "error", "message": f"Error processing PDF: {e}"})

        else:
            return jsonify({"status": "error", "message": "Only PDF files are allowed"})

    def transform_json_to_csv(self, json_data, csv_filename):
        keys = json_data[0].get('answers', {}).keys()
        csv_data = ','.join(['studentID'] + list(keys)) + '\n'
        for student in json_data:
            row = [student['studentID']] + [student['answers'].get(k, '') for k in keys]
            csv_data += ','.join(row) + '\n'

        csv_file_path = os.path.join(self.uploads_dir, csv_filename)
        with open(csv_file_path, 'w', newline='') as file:
            file.write(csv_data)
        
        self.csv_files[csv_filename] = {'filename': csv_filename, 'path': csv_file_path}
        return csv_filename

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
