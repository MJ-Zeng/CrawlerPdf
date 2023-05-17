from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextBoxHorizontal, LTImage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfpage import PDFPage
import glob
import re




def get_file_list(root=".", file_suffix="*") -> list:
    l = glob.glob("{}/*.".format(root) + file_suffix)
    return l


def pdf_to_txt(file_path: str):
    my_pdf = open(file_path, 'rb')
    print("File:", file_path)
    par = PDFParser(my_pdf)
    my_doc = PDFDocument(par)
    if not my_doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        res = PDFResourceManager()
        la = LAParams()
        dev = PDFPageAggregator(res, laparams=la)
        my_interpreter = PDFPageInterpreter(res, dev)
        rs = []
        lt_dict = {}
        for pg in PDFPage.create_pages(my_doc):
            k = pg.pageid
            # if k>200:
            #     return  rs
            my_interpreter.process_page(pg)
            layout = dev.get_result()
            tmp = None
            for obj in layout:
                if isinstance(obj, LTTextBox):
                    len_dict = len(lt_dict)
                    if len_dict != 0 and len_dict % 3 == 0:
                        rs.append(lt_dict)
                        lt_dict = {}
                        if tmp is not  None:
                            lt_dict['name'] = tmp
                            tmp = None

                    line = obj.get_text().splitlines()
                    str_line = " ".join (line)
                    str_line = re.sub(r'\t|\n', '', str_line)
                    chem = re.findall(r'(\([A-Z],[A-Z]\)-.*?) \(\d[a-z]\)', str_line, re.S)
                    ee = re.findall(r'([0-9.]+%) ? ?ee', str_line, re.S)
                    chem_yield = re.findall(r'([0-9.]+%) ? ?yield', str_line, re.S)
                    if len(chem) != 0 and chem[0].__contains__('-') and 'name' not in lt_dict:
                        lt_dict['name'] = chem[0]
                    elif 'name' in lt_dict and len(chem) != 0:
                        tmp = chem

                    if 'name' in lt_dict and len(ee) != 0:
                        lt_dict['ee'] = ee[0]

                    if 'name' in lt_dict and len(chem_yield) != 0:
                        lt_dict['yield'] = chem_yield[0]

            print(k)
    return rs
