"""This is parent for all types of sheet processing"""
from abc import ABC, abstractmethod
import os
import cv2

class SheetProcessor(ABC):
    """This is parent class for all types of sheet processing"""
    def __init__(self, pdf_path, template_path, output_folder="data"):
        self.pdf_path = pdf_path
        self.template_path = template_path
        self.output_folder = output_folder

    @abstractmethod
    def extractROIs(self):
        """Getting gthe ROI"""
        pass

    def extractImagesFromPdf(self):
        """Getting the Image form large PDF files"""
        pass

    def save_cropped_image(self, image, name):
        """Helper function to save cropped ROIs."""
        output_path = os.path.join(self.output_folder, name)
        cv2.imwrite(output_path, image)
        return output_path
