#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/19 1:01
# @Author  : Yiu
# @Site    : https://github.com/dominique-yiu
# @File    : classifier.py
# @Software: PyCharm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
from sklearn import svm
import pandas as pd
from sklearn.model_selection import train_test_split


class one_class_svm:
    def __init__(self, train_path, test_path, nu=0.1, kernel="rbf", gamma=0.1, test_size=0.3, random_state=2021):
        self.train_path = train_path
        self.test_path = test_path
        self.df = pd.read_csv(self.train_path)
        self.clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
        self.x_train, self.x_valid = train_test_split(self.df, test_size=0.3, random_state=2021)

    def train(self):
        self.clf.fit(self.x_train)
        y_pred_train = self.clf.predict(self.x_train)
        y_pred_test = self.clf.predict(self.x_valid)

        y_pred_train = pd.DataFrame(list(y_pred_train), columns=['predict'])
        y_pred_test = pd.DataFrame(list(y_pred_test), columns=['predict'])

        # legal visitors accuracy
        print(y_pred_train[y_pred_train['predict'] == 1].shape[0] / y_pred_train.shape[0],
              y_pred_test[y_pred_test['predict'] == 1].shape[0] / y_pred_test.shape[0])

        # illegal visitors accuracy

