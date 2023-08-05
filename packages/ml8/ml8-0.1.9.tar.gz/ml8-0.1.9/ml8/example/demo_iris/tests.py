"""
tests
"""

def test_datasets():
    from ml8.datasets import describe
    from ml8.datasets import load
    from ml8.datasets import model_selection
    print(describe("iris"))
    iris = load("iris")
    print (iris.df.head())
    X = iris.X
    y = iris.y
    print(X[:5])
    print(y[:5])
    print(X.shape)
    print(y.shape)

    X_train, X_test, y_train, y_test = model_selection.train_test_split(X=X, y=y, test_size=0.25)
    print (X_train[0:3])
    print(X_test[0:3])
    print(y_train[0:3])
    print(y_test[0:3])


def test_classifier():
    from ml8.datasets import load
    from ml8.classifier import DecisionTreeClassifier
    from ml8.datasets import model_selection
    from ml8 import metrics
    iris = load("iris")
    X = iris.X
    y = iris.y
    print("X的维度是：", X.shape)
    print("y的维度是：", y.shape)

    print("样本的不平衡度为：", iris.get_imblance())
    print("样本经过平衡处理后的不平衡度为：", iris.blance())

    dt = DecisionTreeClassifier(max_depth=3)
    print(dt)

    X_train, X_test, y_train, y_test = model_selection.train_test_split(X=X, y=y, test_size=0.25)
    dt.fit(X_train, y_train)
    print("测试集的预测结果为：\n", dt.predict(X_test))

    res = dt.test(X_test, y_test)

    print("第一种准确率评价方式：", res['accuracy_score'])
    print("第二种准确率评价方式：", metrics.accuracy_score(y_test, dt.predict(X_test)))

    print("第一种混淆矩阵评价方式:", res['confusion_matrix'])
    print("第二种混淆矩阵评价方式：", metrics.confusion_matrix(y_test, dt.predict(X_test)))

    print("第一种F1评价方式：", res['classification_report'])
    print("第二种F1评价方式：", metrics.classification_report(y_test, dt.predict(X_test)))


def test_metrics():
    from ml8.datasets import load
    from ml8.classifier import DecisionTreeClassifier
    from ml8.datasets import model_selection
    from ml8 import metrics
    iris = load("iris")
    X = iris.X
    y = iris.y
    print("X的维度是：", X.shape)
    print("y的维度是：", y.shape)

    dt = DecisionTreeClassifier(max_depth=3)
    print(dt)

    X_train, X_test, y_train, y_test = model_selection.train_test_split(X=X, y=y, test_size=0.25)
    dt.fit(X_train, y_train)
    print("测试集的预测结果为：\n", dt.predict(X_test))

    print("准确率：", metrics.accuracy_score(y_test, dt.predict(X_test)))

    print("混淆矩阵：", metrics.confusion_matrix(y_test, dt.predict(X_test)))

    print("F1：", metrics.classification_report(y_test, dt.predict(X_test)))

def test_demo(name="iris"):
    """
    运行demo模块中的程序，默认是运行demo中的"iris"
    param name: 要运行的程序
    """
    from ml8 import demo
    demo(name)


def main():
    test_demo("iris")     # 运行鸢尾花测试样例
    # test_demo("face")   # 人脸识别的demo


if __name__ == "__main__":
    main()

