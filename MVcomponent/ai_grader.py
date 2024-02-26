#high level component that interacts with the server to process the data
# - defines an interface for sending input file (pdf or image format)
# - provides a mock student id and mock answers for each input file as a response
# in the form of a list of answers for each question
# - mock response is defined as a file

import requests
import random
import requests

class AIGrader:
    """
    Class docstring goes here.
    """

    def __init__(self, server_url = 'http://localhost:5000', response_file = 'mock_response.txt'):
        """
        Initialization of 'AI grader' object
        :param server_url: the URL of server for processing data
        :param response_file: the file containing mock responses.
        """
        self.server_url = server_url
        self.mock_responses = self.load_responses(response_file)

    def load_responses(self, response_file):
        """
        Loads mock responses from the specified file.

        :return: a list of mock responses.
        """
        with open(response_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            return [line.strip().split(',') for line in lines]
        
    def generate_response():
        num_questions = len(self.mock_responses[0])
        return [random.choice(['a', 'b', 'c', 'd', '-']) for _ in range (num_questions)]
        
    def process_input():
        student_id = self.get_studentID(file_path)
        mock_response = self.generate_mock_response(student_id)

        return student_id, mock_response;
        
    def get_studentID():
        return f"MockStudentID_{random.randint(1000, 9999)}"
    
if __name__ == "__main__":
    mock_grader = AIGrader()

    INPUT_FILE_PATH = "path/to/your/input_file.pdf"
    stud_id, mock_resp = mock_grader.process_input(INPUT_FILE_PATH)

    print(f"Mock Student ID: {stud_id}")
    print("Mock Response:")
    print(mock_resp)
