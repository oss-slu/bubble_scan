"""
This module calls the class Scantron95945 and takes a PDF file as input for processing
"""
from Scantron import Scantron95945

"""Main method to recieve the input file"""
def main():

    pdf_path = 'PDF/Super30.pdf'
    sc = Scantron95945(pdf_path)
    print(sc.extract_responses())


if __name__ == '__main__':
    main()
