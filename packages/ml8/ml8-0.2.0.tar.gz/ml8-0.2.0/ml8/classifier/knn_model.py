"""

"""

from sklearn import tree
from sklearn import metrics
import pydot
from sklearn.externals.six import StringIO
import os
from sklearn.neighbors import KNeighborsClassifier


class KNN(object):
    """

    """

    def __init__(self,
                 n_neighbors=5,
                 weights='uniform',
                 algorithm='auto',
                 leaf_size=30,
                 p=2,
                 metric='minkowski',
                 metric_params=None,
                 n_jobs=1):
        self.n_neighbors = n_neighbors
        self.weights = weights
        self.algorithm = algorithm
        self.leaf_size = leaf_size
        self.p = p
        self.metric = metric
        self.metric_params = metric_params
        self.n_jobs = n_jobs

        self.model = self.get_model()

        # self.X_train = None
        # self.y_train = None

    def get_model(self):
        """
        初始化的时候通过这里调用sklearn的方法获得DT模型
        :return: 返回sklearn中的决策树模型
        """
        self.model = KNeighborsClassifier(n_neighbors=self.n_neighbors,
                                          weights=self.weights,
                                          algorithm=self.algorithm,
                                          leaf_size=self.leaf_size,
                                          p=self.p,
                                          metric=self.metric,
                                          metric_params=self.metric_params,
                                          n_jobs=self.n_jobs)
        return self.model


    def fit(self, X_train, y_train,
            sample_weight=None, check_input=True, X_idx_sorted=None):
        """
        训练模型，通过传入不同参数进行不同的模型训练
        :return:返回训练好的模型
        """
        self.model.fit(X_train, y_train,
                       sample_weight, check_input, X_idx_sorted)
        print (self.model)
        # return self

    def predict(self, X_test):
        """
        预测
        :param X_test: 测试集
        :return: 预测的结果
        """
        y_predict = self.model.predict(X_test)
        # self.y_predict = y_predict
        return y_predict

    def test(self, X_test, y_test, target_names=None):
        """
        性能评估
        :param X_test: 测试集
        :param y_test: 测试集的标签
        :param target_names:样本的类别
        :return:
        """
        # y_predict = self.predict(X_test)
        # self.accuracy_score = metrics.accuracy_score(y_predict, y_test)
        # self.confusion_matrix = metrics.confusion_matrix(y_test, y_predict)
        # self.classification_report = metrics.classification_report(y_test, y_predict, target_names=target_names)
        y_predict = self.predict(X_test)
        accuracy_score = metrics.accuracy_score(y_predict, y_test)
        confusion_matrix = metrics.confusion_matrix(y_test, y_predict)
        classification_report = metrics.classification_report(y_test, y_predict, target_names=target_names)
        self.accuracy_score = accuracy_score
        self.confusion_matrix = confusion_matrix
        self.classification_report = classification_report

        return {"accuracy_score":accuracy_score, "confusion_matrix":confusion_matrix, "classification_report":classification_report}

    def generate_tree(self, path='.', name='DT.pdf'):
        """
        打印决策树模型生成的决策树，保存成pdf格式
        :param path: 保存文件的路径
        :param name: 需要保存的文件名
        :return:
        """
        dot_data = StringIO()
        tree.export_graphviz(self.model, out_file=dot_data)
        graph = pydot.graph_from_dot_data(dot_data.getvalue())
        path = os.path.join(path, name)
        graph[0].write_pdf(path)
        print (path)


