import pdfTools
import xlwt
from time import strftime, gmtime, ctime, localtime, time
import  re



str='(S,E)-1-methoxy-4-(3-phenylbut-1-en-1-yl)benzene (3a)'

chem = re.findall(r'(\([A-Z],[A-Z]\)-.*?) \(\d[a-z]\)', str, re.S)
flag = chem[0].__contains__('-')
#
str_line = '2,3,3-trimethylbutan-2-yl	 (3d).	'
b = re.sub(r'\t|\n', '', str_line)

def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.



if __name__ == '__main__':
    print_hi('PyCharm')

flie_lst = pdfTools.get_file_list(r"F:\ZMJ\Code\CrawlerPdf\rcc-a\test", "pdf")

for fl in flie_lst:
    print("filepath:" + fl)
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('My Worksheet')
    worksheet.write(0, 0, label="name")
    worksheet.write(0, 1, label="ee")
    worksheet.write(0, 2, label="yield")
    i = 2
    for index, value in enumerate(pdfTools.pdf_to_txt(fl)):
        i = index + 1
        worksheet.write(i, 0, label=value['name'])
        worksheet.write(i, 1, label=value['ee'])
        worksheet.write(i, 2, label=value['yield'])
    pdf_name = fl.split('.pdf')[0]
    file_name = pdf_name + strftime("%Y-%m-%d@%H-%M-%S", localtime(time()))
    workbook.save(file_name + '.xls')
