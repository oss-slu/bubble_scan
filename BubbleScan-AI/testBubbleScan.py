from Scantron import Scantron95945


def main():

    pdf_path = 'PDF/Super30.pdf'
    sc = Scantron95945(pdf_path)
    print(sc.extract_responses())


if __name__ == '__main__':
    main()
