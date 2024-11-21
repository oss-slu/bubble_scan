"""Tesing the bubble detection"""
import sys
import os
# Adding the parent directory to the system path to import Scantron95945

import sys
import os
import cv2
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Scantron import Scantron95945
from TestScantron import Scantron95945TestHelper


class TestBubbleDetection:
    """Create a synthetic image representing a row with one bubble filled ('A')"""
    def test_get_responses_bubble_row_single_fill(self):
        """Create a synthetic image representing a row with one bubble filled ('A')"""
        image = np.full((100, 500, 3), 255, dtype=np.uint8)  # White background
        bubble_width = 500 // 5  # 100 pixels per bubble

        # Bubble 'A' is the first bubble (index 0)
        x_center = bubble_width // 2  # Center of bubble 'A'
        cv2.circle(image, (x_center, 50), 30, (0, 0, 0), -1)  # Black filled circle

        # Instantiate the TestScantron95945 class
        scantron = Scantron95945TestHelper('BubbleScan-AI/PDF/Scans-4-2-24.pdf')

        # Get the response from the image
        response = scantron.get_responses_bubble_row(image)

        # Assert that the response is 'A'
        assert response == 'A'

    def test_get_responses_bubble_row_multiple_fills(self):
        """Create a synthetic image representing a row with multiple bubbles filled ('A' and 'B')"""
        image = np.full((100, 500, 3), 255, dtype=np.uint8)  # White background
        bubble_width = 500 // 5  # 100 pixels per bubble

        # Bubble 'A' (index 0) and Bubble 'B' (index 1)
        x_center_A = bubble_width // 2  # Center of bubble 'A'
        x_center_B = bubble_width + bubble_width // 2  # Center of bubble 'B'

        cv2.circle(image, (x_center_A, 50), 30, (0, 0, 0), -1)  # Black filled circle for 'A'
        cv2.circle(image, (x_center_B, 50), 30, (0, 0, 0), -1)  # Black filled circle for 'B'

        # Instantiate the TestScantron95945 class
        scantron = Scantron95945TestHelper('BubbleScan-AI/PDF/Scans-4-2-24.pdf')

        # Get the response from the image
        response = scantron.get_responses_bubble_row(image)

        # Assert that the response contains both 'A' and 'B'
        assert response == ['A', 'B']


    def test_bubble_column_single_fill(self):
        """Test bubble_column with a single bubble filled."""

        # Create a synthetic column image with one bubble filled (index 4)
        column = np.zeros((1000, 100, 1), dtype=np.uint8)
        cv2.rectangle(column, (0, 400), (100, 500), 255, -1)  # Filling bubble at index 4

        # Instantiate the Scantron95945 class
        scantron = Scantron95945('BubbleScan-AI/PDF/Scans-4-2-24.pdf')

        # Get the index of the filled bubble
        index = scantron.bubble_column(column)

        # Assert that the index is 4
        assert index == 4

    def test_bubble_column_no_fill(self):
        """Test bubble_column when no bubbles are filled."""

        # Create a synthetic empty column image
        column = np.zeros((1000, 100, 1), dtype=np.uint8)

        # Instantiate the Scantron95945 class
        scantron = Scantron95945('BubbleScan-AI/PDF/Scans-4-2-24.pdf')

        # Get the index of the filled bubble
        index = scantron.bubble_column(column)

        # Assert that the index is None since no bubble is filled
        assert index is None
