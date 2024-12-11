from PyPDF4 import PdfFileReader

if __name__ == '__main__':
    pdf_document = "files/mn.pdf"
    with open(pdf_document, "rb") as fpdf:
        pdf = PdfFileReader(fpdf)

        info = pdf.getDocumentInfo()
        pages = pdf.getNumPages()
        print("Количество страниц в документе: %i\n\n" % pages)
        print("Мета-описание: ", info)
        # for i in range(pages):
        page = pdf.getPage(0)
        print(" мета: ", page, "\n\nСодержание;\n")
        print(page.extractText())