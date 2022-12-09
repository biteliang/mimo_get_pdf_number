import pdfplumber
from pdfminer.pdfparser import PDFSyntaxError
import os
import gc
import time

# author:Peter
'''
先获取文件夹下所有的文件名
然后进行判定
    如果文件名后几位 == NY.PDF
    就执行命名
其他全都放在一个列表里 fileList

使用pdfplumber,分别把fileList里的放进去,然后进行改名

'''


# 获取文件夹中的文件名
def get_file_name(path):
    fileList = []
    # root 表示当前正在访问的文件夹路径
    # dirs 是list,表示该文件夹中所有的目录的名字（不包括子目录）
    # files 是list,表示内容是该文件夹中所有的文件（不包括子目录）
    for root, dirs, files in os.walk(path):
        for name in files:
            fname = os.path.join(root, name)
            fileList.append(fname)
    return fileList


# 使用pdfplumber,获取pdf文档页数
def get_pdf_page(pdf_path):
    try:
        f = pdfplumber.open(pdf_path)
        page = len(f.pages)
    except PDFSyntaxError:
        page = 0
    return page


if __name__ == '__main__':
    while True:
        start_time = time.time()
        path = input("please input path:\n请输入路径:\n")
        for i in get_file_name(path):
            if "NY.pdf" in i:
                oldname = i
                # 新命名 = 原命名去".pdf"后缀,然后加上页数再补上后缀
                newname = i.replace(".pdf", "") + "=" + str(get_pdf_page(i)) + "P.pdf"
                # 回收内存,不然会命名失败
                gc.collect()
                os.rename(oldname, newname)
                # print(newname)
        end_time = time.time()
        print(f"the running time is : {end_time - start_time} s\n本次目录已执行完毕,如需继续请直接输入路径\n")
