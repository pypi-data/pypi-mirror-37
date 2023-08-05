"""

"""

def demo_iris():
    import pandas as pd
    name="iris"
    from .... import datasets
    print("\n### 0 数据集描述---------------------\n")
    datasets.describe(name) 
    print("\n### 1 数据集加载---------------------\n")
    dst_iris = datasets.load(name)
    df_iris = dst_iris.df
    print ("数据集前五条数据：\n")
    print (df_iris.head())
    print ("数据集后五条数据：\n")
    print (df_iris.tail())
    print("\n### 2 特征选择---------------------\n")
    X_names = ["SepalLength","SepalWidth","PetalLength","PetalWidth"]
    y_name  = ["class"]
    X = df_iris[X_names]
    y = df_iris[y_name ]
    print("\n### 3 数据集分割---------------------\n")
    X_train, X_test, y_train, y_test = datasets.train_test_split(X=X, y=y, test_size=0.25)   # 划分训练集和测试集
    #print ("将数据划分为训练集和测试集，其中\n\
    #        X_train:训练集\n\
    #        X_test:测试集\n\
    #        y_train:训练集的标签\n\
    #        y_test:测试集的标签\n")
    
    from ....classifier import DecisionTreeClassifier
    print("\n### 4 构建决策树模型---------------------\n")
    dt = DecisionTreeClassifier(max_depth=3)    
    dt.fit(X_train, y_train)    
    print("\n### 5 验证测试集---------------------\n")
    y_pred = dt.predict(X_test)
    res = pd.concat([X_test, y_test], axis=1)
    res['pred'] = y_pred
    print (res)
    print("\n### 6 评价模型---------------------\n")

    from .... import metrics
    print("准确率：\n", metrics.accuracy_score(y_test, y_pred)) # 输出模型准确率
    print("\n")

    print (metrics.print_confusion_matrix(y_test, y_pred,["山鸢尾","变色鸢尾","维基利亚鸢尾"]))
    print("混淆矩阵：\n", metrics.confusion_matrix(y_test, y_pred))  # 输出混淆矩阵
    print("\n")

    print("精确率、召回率和f1值：\n", metrics.classification_report(y_test, y_pred))  # 输出精确率、召回率和F1的值
    print("\n")

def run_demo_boston():
    pass

def run_demo_galton():
    pass

