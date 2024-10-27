import os
import cv2
import fitz  # PyMuPDF for PDF processing
import numpy as np
from SheetProcessor import SheetProcessor
import matplotlib.pyplot as plt

class CustomProcessor(SheetProcessor):
    """Class for processing custom answer sheets with dynamic ROI detection."""

    def __init__(self, pdf_path, template_path="custom_template.jpg"):
        super().__init__(pdf_path, template_path)
        self.template_path = template_path
        self.output_folder = "data"
        self.extractImagesFromPdf()
        # Uncomment if template matching is necessary for alignment
        # self.template_matching()
        self.extractROIs()

    def extractImagesFromPdf(self):
        """
        Separate the custom sheet PDF into individual pages and save them as images.
        """
        pdf_document = fitz.open(self.pdf_path)
        print("------Extracting all Images from Custom PDF------")

        aligned_folder = os.path.join(self.output_folder, "customAligned")
        os.makedirs(aligned_folder, exist_ok=True)

        for page_number, page in enumerate(pdf_document):
            image_filename = f"CustomImage_{page_number + 1}.jpg"
            image_path = os.path.join(aligned_folder, image_filename)

            # Convert each page to an image and save
            original_pix = page.get_pixmap(matrix=fitz.Identity, colorspace=fitz.csRGB)
            scale_x = 1689 / original_pix.width
            scale_y = 2186 / original_pix.height
            matrix = fitz.Matrix(scale_x, scale_y)
            pix = page.get_pixmap(matrix=matrix, colorspace=fitz.csRGB)
            pix.save(image_path)
            print(f"Extracted {image_filename}")

        pdf_document.close()

    def template_matching(self):
        """
        Align each page with the template for consistency in ROI extraction.
        """
        print("------Template Matching for Custom Sheets------")
        template = cv2.imread(self.template_path)
        aligned_folder = os.path.join(self.output_folder, "customAligned")
        output_folder = os.path.join(self.output_folder, "customROIs")

        image_files = [f for f in os.listdir(aligned_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

        for image_file in sorted(image_files):
            image_path = os.path.join(aligned_folder, image_file)
            image = cv2.imread(image_path)

            # Implement custom alignment here if necessary
            aligned_image = self.align_image(image, template)

            # Save aligned image if alignment is done
            if aligned_image is not None:
                aligned_path = os.path.join(output_folder, image_file)
                cv2.imwrite(aligned_path, aligned_image)
                print(f"Aligned and saved {image_file}")

    def extractROIs(self):
        """Extract regions of interest for each custom sheet image."""
        print("------Extracting ROIs for Custom Sheet Images------")

        aligned_images_folder = os.path.join(self.output_folder, "customAligned")
        roi_folder_base = os.path.join(self.output_folder, "customROIs")
        os.makedirs(roi_folder_base, exist_ok=True)

        # List all images in the customAligned folder
        image_files = [f for f in os.listdir(aligned_images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        for image_file in sorted(image_files):
            image_path = os.path.join(aligned_images_folder, image_file)
            print(f"Processing file: {image_file} for ROI extraction")

            # Create a unique folder for each image's ROIs in customROIs
            image_name = os.path.splitext(image_file)[0]
            roi_folder = os.path.join(roi_folder_base, image_name)
            os.makedirs(roi_folder, exist_ok=True)

            # Extract and save ROIs based on updated layout
            first_column, second_column, key_id, student_id = self.crop_roi(image_path, roi_folder)

            # Output confirmation of saved ROI paths
            print(f"Extracted ROIs for {image_name}:")
            print("First Column Path:", first_column)
            print("Second Column Path:", second_column)
            print("Key ID Path:", key_id)
            print("Student ID Path:", student_id)

    def crop_roi(self, image_path, roi_folder):
        """Crop ROIs based on adjusted coordinates for custom sheets."""
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Unable to load image at {image_path}")
            return (None, None, None, None)

        # Define coordinates for each ROI (based on custom sheet layout)
        first_column_coords = (250, 270, 470, 1380)
        second_column_coords = (580, 270, 800, 1380)
        key_id_coords = (210, 160, 495, 200)
        student_id_coords = (230, 1555, 595, 1835)

        # Crop the regions
        first_column_roi = image[first_column_coords[1]:first_column_coords[3], first_column_coords[0]:first_column_coords[2]]
        second_column_roi = image[second_column_coords[1]:second_column_coords[3], second_column_coords[0]:second_column_coords[2]]
        key_id_roi = image[key_id_coords[1]:key_id_coords[3], key_id_coords[0]:key_id_coords[2]]
        student_id_roi = image[student_id_coords[1]:student_id_coords[3], student_id_coords[0]:student_id_coords[2]]

        # Save each ROI image in the specific image's ROI folder
        first_column_path = os.path.join(roi_folder, "first_column_custom.jpg")
        second_column_path = os.path.join(roi_folder, "second_column_custom.jpg")
        key_id_path = os.path.join(roi_folder, "key_id_custom.jpg")
        student_id_path = os.path.join(roi_folder, "student_id_custom.jpg")

        cv2.imwrite(first_column_path, first_column_roi)
        cv2.imwrite(second_column_path, second_column_roi)
        cv2.imwrite(key_id_path, key_id_roi)
        cv2.imwrite(student_id_path, student_id_roi)

        return first_column_path, second_column_path, key_id_path, student_id_path

