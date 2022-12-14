import gc
import os
import time
import tqdm
import datetime

import pdfplumber
from pdfminer.pdfparser import PDFSyntaxError

# author:Peter
'''

先获取N:/7900文件夹下所有的目录
筛选今天日期和昨天日期和前天日期,放到一个列表里
把这列表的文件进行判定,是NY.pdf则执行命名

'''


# 获取文件夹中的文件名
def get_file_name(file_path):
    file_list = []
    # root 表示当前正在访问的文件夹路径
    # dirs 是list,表示该文件夹中所有的目录的名字（不包括子目录）
    # files 是list,表示内容是该文件夹中所有的文件（不包括子目录）
    for root, dirs, files in os.walk(file_path):
        for name in files:
            f_name = os.path.join(root, name)
            file_list.append(f_name)
    return file_list


# 获取文件夹中的文件夹名
def get_dirs_name(dir_path):
    dir_list = []
    dbtype_list = os.listdir(dir_path)
    for dbtype in dbtype_list:
        if os.path.isdir(os.path.join(dir_path, dbtype)):
            dir_list.append(dbtype)
    return dir_list


# 使用pdfplumber,获取pdf文档页数
def get_pdf_page(pdf_path):
    try:
        f = pdfplumber.open(pdf_path)
        page = len(f.pages)
    except PDFSyntaxError:
        page = 0
    return page


# 获取今天的日期并格式化,例：1201  代表12月1日
def get_today():
    today = datetime.date.today()
    formatted_today = today.strftime("%m%d")
    return formatted_today


if __name__ == '__main__':
    start_time = time.time()

    # path = input("please input path:\n请输入路径:\n")
    path = "N:\\indigo-7900"

    # 获取路径下所有文件夹名
    d_list = get_dirs_name(path)

    # 创建空列表,存放带有近三天日期的文件夹
    nearly_three_day_dirs = []
    for i in d_list:
        if get_today() in i:
            nearly_three_day_dirs.append(i)
        if str(int(get_today()) - 1) in i:
            nearly_three_day_dirs.append(i)
        if str(int(get_today()) - 2) in i:
            nearly_three_day_dirs.append(i)

    nearly_three_day_dirs_list = []
    # 拼接路径,合并nearly_three_day_dirs 然后把这作为一个路径
    for j in tqdm.tqdm(nearly_three_day_dirs):
        nearly_three_day_dirs = "N:\\indigo-7900\\" + j
        # 获取这个路径下的所有文件名
        for k in get_file_name(nearly_three_day_dirs):
            # 对文件名进行一个判断
            if "NY.pdf" in k:
                old_name = k
                # 新命名 = 原命名去".pdf"后缀,然后加上页数再补上后缀
                new_name = k.replace(".pdf", "") + "=" + str(get_pdf_page(k)) + "P.pdf"
                # 回收内存
                gc.collect()
                # 进行改名
                os.rename(old_name, new_name)
                nearly_three_day_dirs_list.append(new_name)
    end_time = time.time()
    # 结束计时并输出运行时间和修改数量
    print(f"the running time is : {end_time - start_time} s.\n本次修改文件数量为：{len(nearly_three_day_dirs_list)}")
    input("")
