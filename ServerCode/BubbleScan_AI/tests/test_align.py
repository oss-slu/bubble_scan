"""Testing the alignment"""
import cv2
import numpy as np
from ..Scantron import Scantron95945

class TestAlignImage:
    """Testing the alignment"""
    def test_correct_alignment(self):
        """Test that the align_image function correctly aligns an image when keypoints are present."""

        # Create synthetic images with features (a white circle in the center)
        image = np.zeros((1000, 1000, 3), dtype=np.uint8)
        template = np.zeros((1000, 1000, 3), dtype=np.uint8)
        cv2.circle(image, (500, 500), 50, (255, 255, 255), -1)  # Circle in the image
        cv2.circle(template, (500, 500), 50, (255, 255, 255), -1)  # Circle in the template

        # Instantiate the Scantron95945 class
        scantron = Scantron95945('PDF/Scans-4-2-24.pdf')

        # Align the image with the template
        aligned = scantron.align_image(image, template)

        # Assert that the aligned image has the same shape as the template
        assert aligned.shape == template.shape

    def test_missing_keypoints(self):
        """Test that the align_image function returns the original image when no keypoints are found."""

        # Create synthetic images without features (completely black)
        image = np.zeros((1000, 1000, 3), dtype=np.uint8)
        template = np.zeros((1000, 1000, 3), dtype=np.uint8)

        # Instantiate the Scantron95945 class
        scantron = Scantron95945('PDF/Scans-4-2-24.pdf')

        # Attempt to align the image with the template
        aligned = scantron.align_image(image, template)

        # Assert that the aligned image is the same as the original image
        assert np.array_equal(aligned, image)
