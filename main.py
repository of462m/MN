# from PyPDF4 import PdfFileReader
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re
import os

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    # codec = 'utf-8'
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

    fp.close()
    device.close()
    return retstr

if __name__ == '__main__':
    src_dirname = 'files'
    dst_dirname = 'results'
    for fname in os.listdir(src_dirname):
        fname_txt = f"{dst_dirname}/{os.path.splitext(fname)[0]}.txt"
        with convert_pdf_to_txt(f'{src_dirname}/{fname}') as txt:
            txt.seek(0)
            reg = ()
            ip_list = []
            for line in txt.readlines():
                if not reg:
                    reg = re.findall(r'Документ зарегистрирован № МН-(\d\d/\d+) от (\d\d)\.(\d\d)\.(\d{4})', line)
                    # if reg:
                    #     print(f'Регистрация: MN-{reg[0][0]}/{reg[0][1]}{reg[0][2]}{reg[0][3]} ')

                ips = re.findall(r'(\d{1,3})\[\.\](\d{1,3})\[\.\](\d{1,3})\[\.\](\d{1,3})', line)
                for ip in ips:
                    ip_list.append(f"{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}")
            ip_list_uniq = list(dict.fromkeys(ip_list))
            for ip in ip_list_uniq:
                # print(f"{ip}\t\t#MN-{reg[0][0]} {reg[0][1]}.{reg[0][2]}.{reg[0][3]}")
                print(f"{ip} -> {fname_txt}")

                # match = re.search(r'((?!-)[A-Za-z0-9-]{1,63}(?<!-)\[\.\])+[A-Za-z]{2,6}', line)
                # for ip in ips:
                #     print(f"{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}")
                # if match:
                #     print(re.sub(r'\[(\.)\]', r'\1', match.group(0)))
