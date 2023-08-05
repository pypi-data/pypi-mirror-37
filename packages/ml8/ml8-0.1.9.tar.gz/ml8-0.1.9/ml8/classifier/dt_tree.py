"""

"""

from sklearn import tree
from .. import metrics
import pydot
from sklearn.externals.six import StringIO
import os


class DecisionTreeClassifier(object):
    """

    """

    def __init__(self,
                 criterion="gini",
                 splitter="best",
                 max_depth=None,
                 min_samples_split=2,
                 min_samples_leaf=1,
                 min_weight_fraction_leaf=0.,
                 max_features=None,
                 random_state=None,
                 max_leaf_nodes=None,
                 min_impurity_decrease=0.,
                 min_impurity_split=None,
                 class_weight=None,
                 presort=False):
        self.criterion = criterion
        self.splitter = splitter
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.min_weight_fraction_leaf = min_weight_fraction_leaf
        self.max_features = max_features
        self.random_state = random_state
        self.max_leaf_nodes = max_leaf_nodes
        self.min_impurity_decrease = min_impurity_decrease
        self.min_impurity_split = min_impurity_split
        self.class_weight = class_weight
        self.presort = presort

        self.model = self.get_model()

    def get_model(self):
        """
        初始化的时候通过这里调用sklearn的方法获得DT模型
        :return: 返回sklearn中的决策树模型
        """
        self.model = tree.DecisionTreeClassifier(criterion=self.criterion,
                                                 splitter=self.splitter,
                                                 max_depth=self.max_depth,
                                                 min_samples_split=self.min_samples_split,
                                                 min_samples_leaf=self.min_samples_leaf,
                                                 min_weight_fraction_leaf=self.min_weight_fraction_leaf,
                                                 max_features=self.max_features,
                                                 random_state=self.random_state,
                                                 max_leaf_nodes=self.max_leaf_nodes,
                                                 min_impurity_decrease=self.min_impurity_decrease,
                                                 min_impurity_split=self.min_impurity_split,
                                                 class_weight=self.class_weight,
                                                 presort=self.presort)
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

    def predict(self, X_test):
        """
        预测
        :param X_test: 测试集
        :return: 预测的结果
        """
        return self.model.predict(X_test)

    def test(self, X_test, y_test, target_names=None):
        """
        性能评估
        :param X_test: 测试集
        :param y_test: 测试集的标签
        :param target_names:样本的类别
        :return:
        """
        y_predict = self.predict(X_test)
        accuracy_score = metrics.accuracy_score(y_predict, y_test)
        confusion_matrix = metrics.confusion_matrix(y_test, y_predict)
        classification_report = metrics.classification_report(y_test, y_predict, target_names=target_names)
        return {"accuracy_score":accuracy_score, "confusion_matrix":confusion_matrix, "classification_report":classification_report}

    def plot2file(self, path='.', name='DT.pdf'):
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


