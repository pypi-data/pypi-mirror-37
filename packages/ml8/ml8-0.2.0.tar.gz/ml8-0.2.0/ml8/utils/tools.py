"""

"""

import json
import csv
import os
import logging


def load_json_file(path):
    """
    加载json文件
    :param path: json文件路径
    :return: json文件的内容，如果加载失败，则返回None
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = json.load(f)
            return content
    except Exception as e:
        print (e)
        return None


def dump_json_file(json_content, path):
    """
    写入到json文件
    :param file_list: json文件内容
    :param path: 需要写入的文件路径
    :return: 如果写入成功，则返回True，否则返回False
    """
    par_path = os.path.join(path, '..')

    if not os.path.exists(par_path):
        os.makedirs(par_path)

    if path[-5:] != '.json':
        print ("[Errno *] 传入的路径不是一个json文件")
        return False

    try:
        with open(path, "w", encoding="utf-8", newline='') as f:
            json.dump(json_content, f, indent=4)
            return True
    except Exception as e:
        print (e)
        return True


def load_csv_file(path):
    """
    加载csv文件
    :param path: csv文件路径
    :return: csv文件的内容，如果加载失败，则返回None
    """
    file_list = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            all_line = csv.reader(f)
            for one_line in all_line:
                file_list.append(one_line)
        return file_list
    except Exception as e:
        print (e)
        return None


def dump_csv_file(file_list, path):
    """
    写入到csv文件
    :param file_list:csv文件列表
    :param path: 需要写入的文件路径
    :return:如果写入成功，则返回True，否则返回False
    """
    par_path = os.path.join(path, '..')

    if not os.path.exists(par_path):
        os.makedirs(par_path)

    if path[-4:] != '.csv':
        print ("[Errno *] 传入的路径不是一个csv文件")
        return False
    # file_name = os.path.split(path)[-1]
    # print (file_name)
    try:
        with open(path, "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(file_list)
            return True
    except Exception as e:
        print (e)
        return None


def mytest():
    # # json_file = load_json_file(r"C:\Users\CPCN\Desktop\temp\file_test\config.json")
    # # print (json_file)
    # # dump_json_file([[1, 2], [3, 4]], r"C:\Users\CPCN\Desktop\temp\file_test\mytest.json")
    # # dump_csv_file([[1, 2], [3, 4]], r"C:\Users\CPCN\Desktop\temp\file_test\mytest.csv")
    # # load_json_file(1)
    # csv_file = load_csv_file(r"C:\Users\CPCN\Desktop\temp\file_test\mytest.csv")
    # print (csv_file)
    #
    # json_content = load_json_file(r"C:\Users\CPCN\Desktop\temp\file_test\config.json")
    # path = r"C:\Users\CPCN\Desktop\temp\file_test\123.json"
    # dump_json_file(json_content, path)
    pass

def main():
    mytest()


if __name__ == "__main__":
    main()




