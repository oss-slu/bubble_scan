"""
This module calls the class Scantron95945 and takes a PDF file as input for processing
"""
from Scantron import Scantron95945


def main():
    """
    Main function to process a PDF file using Scantron95945 class.

    This function initializes a Scantron95945 object with a PDF file path and
    prints the extracted responses.

    Parameters:
    None

    Returns:
    None
    """
    pdf_path = 'PDF/BubbleScans-redacted 1-4.pdf'
    sc = Scantron95945(pdf_path)
    print(sc.extract_responses())


if __name__ == '__main__':
    main()
