#Wikicivi Crawler Client SDK
import os,time
import datetime

#LOG,INFO,WARN,ERROR,

from .demo import *
from .datasets import describe 

def intro():
    print("这是TechYoung课程的机器学习辅助工具包")
    return True

def demo(name="iris"):
    #加载数据集的json描述文件
    print("### 1 数据集描述---------------------")
    describe(name) 
    
    if name == "iris": run_demo_iris()
    elif name == "boston":run_demo_boston()
    elif name == "galton":run_demo_galton()
    else:
        print("仅仅支持iris/boston/galton")


# demo()

