from modules.pdf_parser import PdfParser
from modules.text_parser import TextParser

if __name__ == "__main__":
    pdf_parser = PdfParser("./SAE J1939-71 (1).pdf")
    pdf_parser.parse()
    text_parser = TextParser()
    text_parser.parse()
