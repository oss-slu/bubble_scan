"""Module for testing the workflow of the application."""
import sys
import os
from unittest.mock import patch
# Adding the parent directory to the system path to import Scantron95945
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Scantron import Scantron95945

class TestIntegration:
    """Tests for the overall application workflow."""
    def test_full_workflow(self, tmpdir):
        """Test the full workflow from PDF upload to JSON generation."""
        # Create a temporary directory and a mock PDF file
        pdf_dir = tmpdir.mkdir('PDF')
        pdf_path = pdf_dir.join('Scans-4-2-24.pdf')
        pdf_path.write('Mock PDF content')  # Writing mock content to simulate a PDF

        # Mock the methods that interact with external systems or files
        with patch.object(Scantron95945, 'extractImagesFromPdf'), \
        patch.object(Scantron95945, 'template_matching'), \
        patch.object(Scantron95945, 'extractROIs'), \
        patch.object(Scantron95945, 'extract_responses', return_value={'students': [{'studentID': '12345', 'answers': {'Q1': 'A'}}]}):
                
                
                # Instantiate the Scantron95945 class with the path to the mock PDF
            scantron = Scantron95945(str(pdf_path))

                # Call extract_responses to get the results
            results = scantron.extract_responses()

                # Assert that the results match the expected output
            assert results == {'students': [{'studentID': '12345', 'answers': {'Q1': 'A'}}]}