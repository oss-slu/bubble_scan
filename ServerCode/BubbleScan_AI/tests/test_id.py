"""Module for testing ID extraction functionality."""
import cv2
import numpy as np
from ..Scantron import Scantron95945

class TestStudentID:
    """Tests for the ID extraction functionality."""
    def test_complete_student_id(self):
        """Tests for the ID extraction functionality."""# Test the student_id function with a complete ID (all digits filled).

        # Create a synthetic ROI with all digits filled correctly
        roi = np.full((1000, 1000), 255, dtype=np.uint8)  # White background

        num_columns = 10
        num_bubbles = 10
        column_width = roi.shape[1] // num_columns
        bubble_height = roi.shape[0] // num_bubbles

        # Fill one bubble per column corresponding to digits 0-9
        for col in range(num_columns):
            row = col % num_bubbles
            x_center = col * column_width + column_width // 2
            y_center = row * bubble_height + bubble_height // 2
            radius = int(min(column_width, bubble_height) * 0.4)
            cv2.circle(roi, (x_center, y_center), radius, 0, -1)  # Black filled circle

        # Convert to a 3-channel image
        roi_color = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)

        # Instantiate the Scantron95945 class
        scantron = Scantron95945('PDF/Scans-4-2-24.pdf')

        # Extract the student ID
        student_id = scantron.student_id(roi_color)

        # Assert that the student ID is correct
        assert student_id == '0123456789'

    def test_incomplete_student_id(self):
        """Test the student_id function with some digits missing.."""# Test the student_id function with some digits missing.

        # Create a synthetic ROI with some digits missing
        roi = np.full((1000, 1000), 255, dtype=np.uint8)  # White background

        num_columns = 10
        num_bubbles = 10
        column_width = roi.shape[1] // num_columns
        bubble_height = roi.shape[0] // num_bubbles

        # Fill bubbles only in even columns
        for col in range(0, num_columns, 2):  # Even columns
            row = col % num_bubbles
            x_center = col * column_width + column_width // 2
            y_center = row * bubble_height + bubble_height // 2
            radius = int(min(column_width, bubble_height) * 0.4)
            cv2.circle(roi, (x_center, y_center), radius, 0, -1)  # Black filled circle

        # Convert to a 3-channel image
        roi_color = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)

        # Instantiate the Scantron95945 class
        scantron = Scantron95945('PDF/Scans-4-2-24.pdf')

        # Extract the student ID
        student_id = scantron.student_id(roi_color)

        # Assert that the student ID contains 'X' for missing digits
        assert student_id == '0X2X4X6X8X'
