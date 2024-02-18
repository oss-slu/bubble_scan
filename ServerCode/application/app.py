from flask import Flask, request, jsonify
from flask_cors import CORS
# from application.rest import scantron
app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)

@app.route('/api/message', methods=['POST'])
def receive_message():

    message_data = request.json
    message = message_data.get('message', '')

    print(f"Received message: {message}")

    return jsonify({"status": "success", "message": "Message received successfully!"})

CORS(app)

if __name__ == '__main__': 
    app.run(debug=True)