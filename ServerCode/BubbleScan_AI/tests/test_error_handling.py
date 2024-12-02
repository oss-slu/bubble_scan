"""Test the Error Handling."""
import pytest
from unittest.mock import patch
from BubbleScan_AI.Scantron import Scantron95945

class TestErrorHandling:
    """Test how the system handles a corrupted `PDF file."""
    @patch('fitz.open')
    def test_corrupted_pdf_handling(self, mock_fitz_open):
        """Test how the system handles a corrupted PDF file."""

        # Simulate an exception when trying to open the PDF
        mock_fitz_open.side_effect = Exception('Corrupted PDF')

        # Assert that an exception is raised when initializing the Scantron95945 class
        with pytest.raises(Exception):
            Scantron95945('corrupted.pdf')

    def test_missing_image_files(self):
        """Test how the system handles missing image files during template matching."""

        # Instantiate the Scantron95945 class
        scantron = Scantron95945('PDF/Scans-4-2-24.pdf')

        # Mock os.listdir to return an empty list (no image files)
        with patch('os.listdir', return_value=[]):
            # Call template_matching and expect it to handle the empty directory gracefully
            scantron.template_matching()
            # No exception should be raised; we can pass the test if the method completes without error
