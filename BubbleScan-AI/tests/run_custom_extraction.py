"""Run Extraction"""
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Custom import CustomProcessor
import sys
import os


# Path to your PDF file
pdf_path = 'PDF/CustomSheets.pdf'

# Instantiate and process
print("Using CustomProcessor for custom sheet extraction.")
processor = CustomProcessor(pdf_path)
processor.extractROIs()

print("ROI extraction complete. Check the 'data/ROIs' directory for output files.")
