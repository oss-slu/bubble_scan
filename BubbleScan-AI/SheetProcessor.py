from abc import ABC, abstractmethod
import os
import cv2
import numpy as np

class SheetProcessor(ABC):
    def __init__(self, pdf_path, template_path, output_folder="data"):
        self.pdf_path = pdf_path
        self.template_path = template_path
        self.output_folder = output_folder

    @abstractmethod
    def extractROIs(self):
        pass

    def extractImagesFromPdf(self):
        pass

    def save_cropped_image(self, image, name):
        """Helper function to save cropped ROIs."""
        output_path = os.path.join(self.output_folder, name)
        cv2.imwrite(output_path, image)
        return output_path
