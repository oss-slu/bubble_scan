"""Run Extraction"""
import os
import sys

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from BubbleScan_AI.Custom import CustomProcessor

# Path to your BubbleScan_AI/PDF file
pdf_path = 'BubbleScan_AI/PDF/CustomSheets.pdf'

# Instantiate and process
print("Using CustomProcessor for custom sheet extraction.")
processor = CustomProcessor(pdf_path)
processor.extractROIs()

print("ROI extraction complete. Check the 'data/ROIs' directory for output files.")
