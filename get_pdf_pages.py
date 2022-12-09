import pdfplumber
import os
import gc
import time

# author:Peter
# PyPDF2速度极慢,本次使用了pdfplumber
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


# 使用PyPDF2库,获取pdf文档页数
def PyPDF2_get_pdf_pages(pdf_path):
    try:
        reader = PyPDF2.PdfFileReader(pdf_path)
        page_num = reader.getNumPages()
    except:
        print(pdf_path + "该文件出现异常，可能是权限问题")
    return page_num


if __name__ == '__main__':
    start_time = time.time()
    path = input("please input path:\n")
    for i in get_file_name(path):
        if "NY.pdf" in i:
            oldname = i
            # 新命名 = 原命名去".pdf"后缀,然后加上页数再补上后缀
            newname = i.replace(".pdf", "") + "=" + str(get_pdf_page(i)) + "P.pdf"
            # 回收内存,不然会命名失败
            gc.collect()
            os.rename(oldname, newname)
    end_time = time.time()
    input(f"the running time is : {end_time - start_time} s\nplease exit......")
