"""

"""
from sklearn import metrics
import pandas as pd
import numpy as np

def accuracy_score(y_true, y_pred, normalize=True, sample_weight=None):
    return metrics.accuracy_score(y_true, y_pred, normalize=normalize, sample_weight=sample_weight)

def confusion_matrix(y_true, y_pred, labels=None, sample_weight=None):
    return metrics.confusion_matrix(y_true, y_pred, labels=labels, sample_weight=sample_weight)

def classification_report(y_true, y_pred, labels=None, target_names=None,
                          sample_weight=None, digits=2):
    return metrics.classification_report(y_true, y_pred, labels=labels, target_names=target_names,
                                         sample_weight=sample_weight, digits=digits)

def print_confusion_matrix(y_true, y_pred, classes=None,labels= None, sample_weight=None):
    matrix_base = metrics.confusion_matrix(y_true, y_pred, labels=labels, sample_weight=sample_weight)
    df_matrix = pd.DataFrame(matrix_base)
    if classes != None:
        df_matrix = pd.DataFrame(index=classes, columns=classes, data = matrix_base)
    return df_matrix
