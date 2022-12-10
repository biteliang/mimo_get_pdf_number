import gc
import os
import time
import tqdm
import datetime

import pdfplumber
from pdfminer.pdfparser import PDFSyntaxError

# author:Peter
'''

1. 输入路径
2. 获取路径下所有的文件名
3. 执行判断,如果文件名包含"NY.pdf"则进行改名

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
            # dir_list.append(dbtype)  或许可以把路径也添加上 dir_list.append(os.path.join(dir_path, dbtype))
            # 这样lir_list就直接是一个路径的列表了
            # 这样应该就不需要 以下这段代码了
            # for j in tqdm.tqdm(nearly_three_day_dirs):
            #     nearly_three_day_dirs = "N:\\indigo-7900\\" + j
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
    # start_time = time.time()

    path = input("please input path:\n请输入路径:\n")
    # path = "N:\\indigo-7900"

    # 获取仅当前路径下所有文件夹名
    d_list = get_file_name(path)
    for i in d_list:
        if "NY.pdf" in i:
            old_name = i
            # 新命名 = 原命名去".pdf"后缀,然后加上页数再补上后缀
            new_name = i.replace(".pdf", "") + "=" + str(get_pdf_page(i)) + "P.pdf"
            # 回收内存
            gc.collect()
            # 进行改名
            os.rename(old_name, new_name)
            # 调试使用
            # print(old_name + "====>" + new_name)
    input("已完成,按任意键退出程序")


    # 筛选出近三天日期的文件夹（以文件名的形式,看看需不需要修改成以创建日期的形式）
    # 创建空列表,存放带有近三天日期的文件夹
    # nearly_three_day_dirs = []
    # for i in d_list:
    #     if get_today() in i:
    #         nearly_three_day_dirs.append(i)
    #     if str(int(get_today()) - 1) in i:
    #         nearly_three_day_dirs.append(i)
    #     if str(int(get_today()) - 2) in i:
    #         nearly_three_day_dirs.append(i)
    #     if str(int(get_today()) - 3) in i:
    #         nearly_three_day_dirs.append(i)
    #     if str(int(get_today()) - 4) in i:
    #         nearly_three_day_dirs.append(i)
    #     if str(int(get_today()) - 5) in i:
    #         nearly_three_day_dirs.append(i)

    # nearly_three_day_dirs_list = []  # 一般用来调试
    # # 拼接路径,合并nearly_three_day_dirs 然后把这作为一个路径
    # for j in d_list:
    #     nearly_three_day_dirs = "N:\\indigo-7900\\" + j
    #     # 获取这个路径下的所有文件名
    #     # 设置函数,增加一个调试,如果=1则调试,如果=2则启动命名
    #     proc_bar = tqdm.tqdm(get_file_name(nearly_three_day_dirs))
    #     for k in proc_bar:
    #         proc_bar.set_postfix({"正在处理": f"{k}"})
    #         # 对文件名进行一个判断
    #         if "NY.pdf" in k:
    #             old_name = k
    #             # 新命名 = 原命名去".pdf"后缀,然后加上页数再补上后缀
    #             new_name = k.replace(".pdf", "") + "=" + str(get_pdf_page(k)) + "P.pdf"
    #             # 回收内存
    #             gc.collect()
    #             # 进行改名
    #             os.rename(old_name, new_name)
    #             nearly_three_day_dirs_list.append(new_name)
    # end_time = time.time()
    # 结束计时并输出运行时间和修改数量
    # print(f"the running time is : {end_time - start_time} s.\n本次修改文件数量为：{len(nearly_three_day_dirs_list)}")
    # input("")
