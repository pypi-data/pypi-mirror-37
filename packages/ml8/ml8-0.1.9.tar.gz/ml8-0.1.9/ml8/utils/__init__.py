"""

"""

from imblearn.combine import SMOTEENN
import math

class Bunch(dict):
    """
    """
    def __init__(self, **kwargs):
        super(Bunch, self).__init__(kwargs)

    def __setattr__(self, key, value):
        self[key] = value

    def __dir__(self):
        return self.keys()

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setstate__(self, state):
        pass

    def blance(self):
        """
        样本采样方法，该方法是一个集成算法，包含smote算法和enn算法
        :return:
        """
        sm = SMOTEENN()
        self.X, self.y = sm.fit_sample(self.X, self.y)
        return self.get_imblance()

    def get_imblance(self):
        """
        获得平衡度，这里用标准差来衡量，该参数只在样本具有分类属性时有意义，因为计算的是不同类型的样本的偏差
        计算公式为：s = sqrt(∑(X-M)^2 / (n-1))
        :return:返回一个浮点数字，该数字越小，数据平衡度越强，表示数据越均衡
        """
        y_list = list(self.y)

        y_dict = {}
        for i in y_list:
            if i not in y_dict:
                y_dict[i] = 1
            else:
                y_dict[i] += 1
        sum = 0
        for i in y_dict:
            sum += y_dict[i]
        m = sum / len(y_dict)

        # get s
        sig = 0.
        for i in y_dict:
            sig += (y_dict[i] - m) ** 2
        s = math.sqrt(sig / len(y_list))

        return s

