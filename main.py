# from PyPDF4 import PdfFileReader
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    # device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    # text = retstr.getvalue()

    fp.close()
    device.close()
    return retstr


if __name__ == '__main__':
    with convert_pdf_to_txt('files/mn01.pdf') as txt:
        txt.seek(0)
        reg = None
        for line in txt.readlines():
            reg = re.findall(r'Документ зарегистрирован № МН-(\d\d/\d+) от (\d\d)\.(\d\d)\.(\d{4})', line)
            for rr in reg:
                print(f'Регистрация: MN-{rr[0]}/{rr[1]}{rr[2]}{rr[3]} ')

            ips = re.findall(r'(\d{1,3})\[\.\](\d{1,3})\[\.\](\d{1,3})\[\.\](\d{1,3})', line)
            match = re.search(r'((?!-)[A-Za-z0-9-]{1,63}(?<!-)\[\.\])+[A-Za-z]{2,6}', line)
            for ip in ips:
                print(f"{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}")
            if match:
                print(match.group(0))


    # with open(txt_document, "r", encoding="utf-8") as tfile:
    #     for line in tfile:
    #         tstring = line.strip()
    #
    #         res = re.findall(r'(\d{1,3})\[\.\](\d{1,3})\[\.\](\d{1,3})\[\.\](\d{1,3})', tstring)
    #         for ip in res:
    #             print(f"{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}")


    # print(re.sub(r'\[(\.)\]', r'\1', hres.string))
