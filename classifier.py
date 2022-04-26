#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/19 1:01
# @Author  : Yiu
# @Site    : https://github.com/dominique-yiu
# @File    : classifier.py
# @Software: PyCharm
from sklearn import svm
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle


class one_class_svm:
    def __init__(self, train_path='gross_features.csv', test_path=None, nu=0.1, kernel="rbf", gamma=0.1, test_size=0.3, random_state=2021):
        self.train_path = train_path
        self.test_path = test_path
        self.df = pd.read_csv(self.train_path)
        self.clf = svm.OneClassSVM(nu=nu, kernel=kernel, gamma=gamma)
        self.x_train, self.x_valid = train_test_split(self.df, test_size=test_size, random_state=random_state)

    def train_(self):
        self.clf.fit(self.df)
        y_pred_train = self.clf.predict(self.df)
        # y_pred_test = self.clf.predict(self.x_valid)

        y_pred_train = pd.DataFrame(list(self.df), columns=['predict'])
        # y_pred_test = pd.DataFrame(list(y_pred_test), columns=['predict'])

        # legal visitors accuracy
        train_accuracy = y_pred_train[y_pred_train['predict'] == 1].shape[0] / y_pred_train.shape[0]
        # test_accuracy = y_pred_test[y_pred_test['predict'] == 1].shape[0] / y_pred_test.shape[0]
        print(f'Training Data Accuracy(Positive): {train_accuracy}')
        # print(f'Validation Data Accuracy(Positive): {test_accuracy}')
        with open('./model/clf.pickle', 'wb') as f:
            pickle.dump(self.clf, f)

    def predict_(self, uncertified_person):
        result = self.clf.predict(uncertified_person)
        return result
        # with open('./model/clf.pickle', 'rb') as f:
        #     self.clf = pickle.load(f)
        #     print(self.clf.predict(uncertified_person))
