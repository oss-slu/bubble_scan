"""Test the Data Extraction function"""
import os
import sys

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from unittest.mock import patch, MagicMock
from Scantron import Scantron95945

class TestExtractImagesFromPdf:
    """Test the Data Extraction function"""
    @patch('fitz.open')
    @patch('os.makedirs')
    @patch('os.path.exists')
    @patch('os.listdir')
    def test_valid_pdf_extraction(self, mock_listdir, mock_exists,mock_makedirs, mock_fitz_open):
        """Test that images are extracted correctly from a valid PDF."""

        # Mock the PDF document and its pages
        mock_pdf = MagicMock()
        mock_page = MagicMock()
        mock_pdf.__iter__.return_value = [mock_page]
        mock_pdf.page_count = 1
        mock_fitz_open.return_value = mock_pdf

        # Mock the page's get_pixmap method
        mock_pixmap = MagicMock()
        mock_pixmap.width = 800
        mock_pixmap.height = 1000
        mock_pixmap.save = MagicMock()
        mock_page.get_pixmap.return_value = mock_pixmap

        # Mock os.path.exists and os.listdir
        mock_exists.return_value = True
        mock_listdir.return_value = ['Image_1.jpg']

        # Instantiate the Scantron95945 class
        scantron = Scantron95945('PDF/Scans-4-2-24.pdf')

        # Check that the images are saved in the correct directory
        pdf_folder = os.path.join(scantron.output_folder, scantron.pdf_name)
        assert os.path.exists(pdf_folder)
        extracted_images = os.listdir(pdf_folder)
        assert len(extracted_images) == 1
        assert extracted_images[0] == 'Image_1.jpg'
