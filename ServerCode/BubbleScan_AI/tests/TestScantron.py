"""Testing Scantron Sheet Processing"""

import sys
import os
import cv2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Scantron import Scantron95945
# Adding the parent directory to the system path to import Scantron95945


class Scantron95945TestHelper(Scantron95945):
    """Testing Scantron Sheet Processing"""
    def get_responses_bubble_row(self, image, num_choices=5):
        """Testing Scantron Sheet Processing"""
        bubble_width = image.shape[1] // num_choices
        filled_bubbles = []

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Remove blurring
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

        # For testing, lower the threshold
        min_white_pixels_to_fill = binary.size // num_choices * 0.1  # Adjusted threshold for testing
        print(f"min_white_pixels_to_fill: {min_white_pixels_to_fill}")

        for i in range(num_choices):
            bubble = binary[:, i * bubble_width:(i + 1) * bubble_width]
            white_pixels = cv2.countNonZero(bubble)
            print(f"Bubble {i}: white_pixels = {white_pixels}")

            if white_pixels >= min_white_pixels_to_fill:
                filled_bubbles.append(i)

        print(f"Filled bubbles: {filled_bubbles}")
        if len(filled_bubbles) == 0:
            return None
        if len(filled_bubbles) == 1:
            return chr(ord('A') + filled_bubbles[0])

        return [chr(ord('A') + index) for index in filled_bubbles]
    