from modules.pdf_parser import PdfParser

if __name__ == "__main__":
    parser = PdfParser("./SAE J1939-71 (1).pdf")
    parser.parse()
