"""Testing the ROI after Croping"""

import sys
import os
import cv2
import numpy as np
from unittest.mock import patch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Scantron import Scantron95945


class TestCropROI:
    """Test that crop_roi correctly crops the ROIs when valid markers are present."""
    @patch('cv2.imwrite', return_value=True)
    @patch('os.makedirs')
    @patch('cv2.imread')
    @patch.object(Scantron95945, 'align_image')
    @patch.object(Scantron95945, 'extractROIs')
    @patch.object(Scantron95945, 'template_matching')
    @patch.object(Scantron95945, 'extractImagesFromPdf')
    def test_valid_crop(self, mock_extractImagesFromPdf, mock_template_matching, mock_extractROIs, mock_align_image, mock_imread, mock_makedirs, mock_imwrite):
        """Test that crop_roi correctly crops the ROIs when valid markers are present."""

        # Create a synthetic image with the necessary markers
        image = np.full((2186, 1689, 3), 255, dtype=np.uint8)  # White background

        # Draw top markers (at least 4)
        cv2.rectangle(image, (100, 10), (160, 50), (0, 0, 0), -1)   # Top marker 1
        cv2.rectangle(image, (500, 10), (560, 50), (0, 0, 0), -1)   # Top marker 2
        cv2.rectangle(image, (900, 10), (960, 50), (0, 0, 0), -1)   # Top marker 3
        cv2.rectangle(image, (1300, 10), (1360, 50), (0, 0, 0), -1) # Top marker 4

        # Draw left markers (at least 54)
        y_positions = np.linspace(80, 2000, 54).astype(int)
        for y in y_positions:
            cv2.rectangle(image, (10, y), (60, y + 30), (0, 0, 0), -1)

        # Mock the necessary functions to return our synthetic image
        mock_imread.return_value = image
        mock_align_image.return_value = image

        # Instantiate the Scantron95945 class
        scantron = Scantron95945('ServerCode/BubbleScan_AI/PDF/Scans-4-2-24.pdf')
        image_path = 'aligned_images/Image_1.jpg'

        # Mock os.path.exists to return True
        with patch('os.path.exists', return_value=True):
            # Call crop_roi to test the ROI extraction
            rois = scantron.crop_roi(image_path)

        # Assert that the ROIs are not None
        assert rois is not None
        first_col_path, second_col_path, student_id_path = rois

        # Check that the correct file paths are returned
        assert first_col_path.endswith('first_column_roi.jpg')
        assert second_col_path.endswith('second_column_roi.jpg')
        assert student_id_path.endswith('student_id_roi.jpg')
