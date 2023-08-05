"""

"""
from __future__ import print_function
import csv
from os.path import dirname, join
from ..utils import Bunch
import numpy as np
import json
import pandas as pd

def describe2(data_name):
    """
    获得数据的详细描述
    :param data_name: 数据集名称
    :return: 返回该数据集的详细描述信息
    """
    module_path = dirname(__file__)
    data_name = data_name + ".rst"
    with open(join(module_path, 'data', data_name)) as rst_file:
        fdescr = rst_file.read()
    return fdescr

def describe(data_name):
    """
    获得数据的详细描述, 这个描述保存在本地的json文件中
    :param data_name: 数据集名称
    :return: 返回该数据集的详细描述信息
    """
    module_path = dirname(__file__)
    data_name = data_name + ".json"
    jsonData = None
    with open(join(module_path, 'data', data_name)) as json_file:
        jsonData = json.load(json_file)
    #接下来有条理的打印出来数据集的各个属性
    print(jsonData["title"])
    print(jsonData["desc"])
    print("年代:"+jsonData["date"])
    print("作者:"+jsonData["creator"])
    print("规模:"+str(jsonData["count"]))
    print("特征:"+str(len(jsonData["features"]))+"个")
    k = 0
    for feature in jsonData["features"]:
        print("{:2}:{}".format(k,feature["name"]))
        k+=1
    print("分类:"+str(len(jsonData["classes"]))+"个")
    k = 0
    for clas in jsonData["classes"]:
        print("{:2}:{}".format(k,clas["name"]))    
        k+=1

    # return fdescr

def load(data_name):
    """
    加载数据集
    :param data_name: 数据集名称
    :return: 返回数据集，Bunch格式
    """
    module_path = dirname(__file__)
    csv_name = data_name + ".csv"
    path = join(module_path, 'data',csv_name) 
    df_dst = pd.read_csv(path, encoding="utf8")

    rst_file = data_name + ".rst"
    with open(join(module_path, 'data', rst_file)) as rst_file:
        fdescr = rst_file.read()

    return Bunch(df = df_dst,
                 DESCR=fdescr)

def load_data2(module_path, data_file_name, X_names=[], y_name=None):
    """
    加载数据集
    :param module_path:数据集的路径
    :param data_file_name:数据集文件名
    :param X_names:数据集特征名
    :param y_name:数据集标签名
    :return:X,y,X_names,y_name分别是数据集、标签、数据集特征名、数据集标签名
    """
    with open(join(module_path, 'data', data_file_name)) as csv_file:
        data_file = csv.reader(csv_file)
        field = next(data_file)

        if y_name == None: # 不指定标签列，则最后一列为标签列
            y_name = field[len(field) - 1]

        if len(X_names) == 0: # 不指定特征列，则合并所有除标签以外的特征列
            X_names = field[:field.index(y_name)] + field[field.index(y_name)+1:]

        X, y = [], []

        for item in data_file:
            X_list = []
            for i in X_names:
                X_list.append(item[field.index(i)])
            X.append(X_list)
            y.append(item[field.index(y_name)])

        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.int32)

    return X, y, X_names, y_name, field

def load_iris(return_X_y=False, X_names=[], y_name=None):
    """
    加载鸢尾花数据集
    :param return_X_y: 该参数表示是否返回X和y
    :param X_names: 数据集特征名
    :param y_name: 数据集标签名
    :return: 返回一个Bunch，这是一个数据集模型
    """
    module_path = dirname(__file__)
    X, y, X_names, y_name, field = load_data(module_path, 'iris.csv')

    with open(join(module_path, 'data', 'iris.rst')) as rst_file:
        fdescr = rst_file.read()

    if return_X_y:
        return X, y

    return Bunch(X=X, y=y,
                 X_names=X_names,
                 DESCR=fdescr,
				 y_name=y_name,
                 field = field)


def load_boston_house_prices(return_X_y=False, X_names=[], y_name=None):
    """
    加载鸢尾花数据集
    :param return_X_y:该参数表示是否返回X和y
    :param X_names:数据集特征名
    :param y_name:数据集标签名
    :return:返回一个Bunch，这是一个数据集模型
    """
    module_path = dirname(__file__)
    X, y, X_names, y_name, field = load_data(module_path, 'boston_house_prices.csv', X_names, y_name)

    with open(join(module_path, 'data', 'boston_house_prices.rst')) as rst_file:
        fdescr = rst_file.read()

    if return_X_y:
        return X, y

    return Bunch(X=X, y=y,
                 X_names=X_names,
                 DESCR=fdescr,
				 y_name=y_name,
                 field = field)

