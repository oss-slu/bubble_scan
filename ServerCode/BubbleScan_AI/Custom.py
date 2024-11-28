import os
import csv
import cv2
import fitz  # PyMuPDF for PDF processing
import shutil
import numpy as np
from BubbleScan_AI.SheetProcessor import SheetProcessor
import matplotlib.pyplot as plt

class CustomProcessor(SheetProcessor):
    """Class for processing custom answer sheets with dynamic ROI detection."""

    def __init__(self, pdf_path, template_path="custom_template.jpg"):
        super().__init__(pdf_path, template_path)
        self.template_path = template_path
        self.output_folder = "data"
        self.extractImagesFromPdf()
        self.extractROIs()

    def extractImagesFromPdf(self):
        """
        Separate the custom sheet PDF into individual pages and save them as images.
        Clears old data before processing.
        """
        # Paths for aligned and ROI directories
        aligned_folder = os.path.join(self.output_folder, "customAligned")
        roi_folder_base = os.path.join(self.output_folder, "customROIs")

        # Clear existing files in the aligned and ROI folders
        if os.path.exists(aligned_folder):
            shutil.rmtree(aligned_folder)  # Deletes the folder and its contents
        if os.path.exists(roi_folder_base):
            shutil.rmtree(roi_folder_base)

        os.makedirs(aligned_folder, exist_ok=True)  # Recreate an empty directory
        os.makedirs(roi_folder_base, exist_ok=True)

        # Extract images from PDF
        pdf_document = fitz.open(self.pdf_path)
        print("------Extracting all Images from Custom PDF------")

        for page_number, page in enumerate(pdf_document):
            image_filename = f"CustomImage_{page_number + 1:03}.jpg"  # Zero-padded filename
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

    def extractROIs(self):
        """Extract regions of interest for each custom sheet image."""
        print("------Extracting ROIs for Custom Sheet Images------")

        aligned_images_folder = os.path.join(self.output_folder, "customAligned")
        roi_folder_base = os.path.join(self.output_folder, "customROIs")
        os.makedirs(roi_folder_base, exist_ok=True)

        # List all images in the customAligned folder
        image_files = [f for f in os.listdir(aligned_images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        # Ensure consistent ordering by sorting filenames
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
    
    def student_id(self, roi, num_columns=10, num_bubbles=10):
        """
        Extracts the student ID by identifying filled bubbles in each column.

        Parameters:
            roi (numpy.ndarray): The ROI image for the student ID.
            num_columns (int): The number of columns in the ROI.
            num_bubbles (int): The number of bubbles per column.

        Returns:
            str: The student ID extracted from the ROI.
        """
        student_id = ''

        # Calculate the width of each column in the ROI
        digit_width = roi.shape[1] // num_columns

        # Process each column to detect filled bubbles
        for i in range(num_columns):
            column_roi = roi[:, i * digit_width:(i + 1) * digit_width]

            # Convert column ROI to grayscale and apply binary thresholding
            gray = cv2.cvtColor(column_roi, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            _, binary = cv2.threshold(blurred, 130, 255, cv2.THRESH_BINARY_INV)

            # Detect the filled bubble within the column
            filled_digit = self.bubble_column(binary, num_bubbles)

            # Append the detected digit to the student ID, or 'X' if not detected
            student_id += str(filled_digit) if filled_digit is not None else ''

        return student_id
    
    def bubble_column(self, column, num_bubbles=10):
        """
        Identifies the filled bubble within a column of bubbles.

        Parameters:
            column (numpy.ndarray): The binary image of the column.
            num_bubbles (int): Number of bubbles in the column.

        Returns:
            Union[int, None]: The index of the filled bubble or None if no bubble is filled.
        """
        max_white_pixels = 0
        filled_bubble_index = None
        bubble_height = column.shape[0] // num_bubbles

        for i in range(num_bubbles):
            bubble = column[i * bubble_height:(i + 1) * bubble_height, :]
            white_pixels = cv2.countNonZero(bubble)

            if white_pixels > max_white_pixels:
                max_white_pixels = white_pixels
                filled_bubble_index = i

        min_white_pixels_to_fill = column.size // num_bubbles * 0.32

        return filled_bubble_index if max_white_pixels >= min_white_pixels_to_fill else None

    def roi(self, image, start_question_num, num_choices=5):
        """
        Processes each row in the image to detect filled bubbles.

        Parameters:
            image (numpy.ndarray): The image containing bubbles.
            start_question_num (int): The starting question number.
            num_choices (int): The number of choices per question (default is 5).

        Returns:
            dict: A dictionary mapping question numbers to detected answers.
        """
        responses = {}
        row_boundaries = self.find_rows(image)  # Find the rows of bubbles in the column

        for i, (row_start, row_end) in enumerate(row_boundaries):
            question_num = start_question_num + i

            # Ensure the row_end is within the image bounds
            row_end = min(row_end, image.shape[0])

            # Extract the row image based on the identified boundaries
            row = image[row_start:row_end, :]

            # Process the row to identify the filled bubble
            response = self.get_responses_bubble_row(row, num_choices)
            responses[f'Q{question_num}'] = response

        return responses

    def find_rows(self, image):
        """
        Finds the rows in the image.

        Parameters:
            image (numpy.ndarray): The image containing bubbles.

        Returns:
            List[Tuple[int, int]]: List of row boundaries.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Vertical projection of the binary image
        vertical_projection = np.sum(binary, axis=1)

        # Detect row breaks based on projection values
        row_breaks = np.where(vertical_projection < np.max(vertical_projection) * 0.1)[0]

        row_boundaries = []
        if row_breaks[0] != 0:
            row_boundaries.append((0, row_breaks[0]))

        for start, end in zip(row_breaks, row_breaks[1:]):
            if end - start > 1:  # Significant gap
                row_boundaries.append((start, end))

        if row_breaks[-1] != len(vertical_projection) - 1:
            row_boundaries.append((row_breaks[-1], len(vertical_projection) - 1))

        return row_boundaries

    def get_responses_bubble_row(self, row, num_choices=5):
        """
        Detects which bubble is filled in a row.

        Parameters:
            row (numpy.ndarray): The row image containing bubbles.
            num_choices (int): The number of answer choices per question.

        Returns:
            str: The filled bubble (e.g., 'A', 'B') or None if no bubble is detected.
        """
        bubble_width = row.shape[1] // num_choices
        filled_bubbles = []

        gray = cv2.cvtColor(row, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (15, 15), 0)
        _, binary = cv2.threshold(blurred, 155, 255, cv2.THRESH_BINARY_INV)

        min_white_pixels_to_fill = binary.size // num_choices * 0.32

        for i in range(num_choices):
            bubble = binary[:, i * bubble_width:(i + 1) * bubble_width]
            white_pixels = cv2.countNonZero(bubble)

            if white_pixels >= min_white_pixels_to_fill:
                filled_bubbles.append(i)

        if len(filled_bubbles) == 0:
            return None
        elif len(filled_bubbles) == 1:
            return chr(ord('A') + filled_bubbles[0])

        return [chr(ord('A') + index) for index in filled_bubbles]


    def extract_responses(self):
        """
        Extracts all the bubbles and prepares them for CSV output.

        Returns:
            list[dict]: List of student responses.
        """
        students_results = []
        base_folder_path = os.path.join(self.output_folder, "customROIs")

        # Assuming the ROIs are organized by folders for each student
        student_image_folders = sorted(os.listdir(base_folder_path))

        for student_image_folder in student_image_folders:
            student_folder_path = os.path.join(base_folder_path, student_image_folder)
            if os.path.isdir(student_folder_path):
                
                # Define paths to the specific ROIs
                first_column_path = os.path.join(student_folder_path, 'first_column_custom.jpg')
                second_column_path = os.path.join(student_folder_path, 'second_column_custom.jpg')
                student_id_path = os.path.join(student_folder_path, 'student_id_custom.jpg')

                # Check if all necessary files are available
                if not all([os.path.exists(first_column_path), os.path.exists(second_column_path), os.path.exists(student_id_path)]):
                    print(f"Missing ROI images in folder: {student_folder_path}")
                    continue

                # Extract student ID and responses
                student_id = self.student_id(cv2.imread(student_id_path))
                responses_first = self.roi(cv2.imread(first_column_path), start_question_num=1)
                responses_second = self.roi(cv2.imread(second_column_path), start_question_num=26)

                # Compile student data
                student_data = {
                    "studentID": student_id,
                    **responses_first,
                    **responses_second
                }
                students_results.append(student_data)

        return students_results

    def save_to_csv(self, students_results, csv_path="output.csv"):
        """
        Save extracted responses to a CSV file.

        Parameters:
            students_results (list[dict]): List of extracted student data.
            csv_path (str): Path to save the CSV file.
        """
        if not students_results:
            print("No data to save.")
            return

        # Define standard headers for 50 questions
        expected_headers = ["studentID"] + [f"Q{i}" for i in range(1, 51)]

        # Check for unexpected keys
        all_keys = set(expected_headers)
        for student_data in students_results:
            all_keys.update(student_data.keys())

        # adding new headers dynamically
        if all_keys != set(expected_headers):
            print("Warning: Unexpected keys detected in responses. Adjusting headers dynamically.")
            expected_headers = sorted(all_keys)  # consistent order

        with open(csv_path, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=expected_headers)
            writer.writeheader()
            for student_data in students_results:
                # Fill missing keys with empty strings
                row = {key: student_data.get(key, '') for key in expected_headers}
                writer.writerow(row)

        print(f"Results saved to {csv_path}")
