from sklearn import svm
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
import numpy as np
import os


def process_features(data):
    length = len(data)
    for idx in range(length):
        data[idx][np.where(data[idx] == 0)[0]] = data[idx][1]
    return data


class one_class_svm:
    def __init__(self, train_path='gross_features.csv', test_path=None, nu=0.1, kernel="rbf", gamma='scale',
                 test_size=0.3, random_state=2021):
        self.y_train = None
        self.y_pred_train = None
        self.train_path = train_path
        self.test_path = test_path
        self.df = None
        self.clf = svm.OneClassSVM(nu=nu, kernel=kernel, gamma=gamma)
        self.columns = None

    def train_(self):
        self.df = pd.read_csv(self.train_path, sep=' ', header=None)
        self.columns = self.df.shape[1]
        # 训练之前需要将zero特征进行修改
        x_train = process_features(self.df.values)
        self.clf.fit(x_train)
        self.y_train = np.ones(len(x_train))
        self.y_pred_train = self.clf.predict(x_train)
        y_pred_train = pd.DataFrame(list(self.y_pred_train), columns=['predict'])

        # legal visitors accuracy
        train_accuracy = y_pred_train[y_pred_train['predict'] == 1].shape[0] / y_pred_train.shape[0]
        print(f'Training Data Accuracy(Positive): {train_accuracy}')
        path = './model'
        os.makedirs(path, exist_ok=True)
        with open('./model/clf.pickle', 'wb') as f:
            pickle.dump(self.clf, f)

    def predict_(self, uncertified_person):
        # data with a length which is bigger than self.columns is an illegal user
        if len(uncertified_person) > self.columns:
            return -1

        processed_data = np.zeros(self.columns)
        processed_data[:uncertified_person.shape[1]] = uncertified_person
        processed_data = processed_data.reshape(1, -1)
        return self.clf.predict(processed_data)
        # with open('./model/clf.pickle', 'rb') as f:
        #     self.clf = pickle.load(f)
        #     print(self.clf.predict(uncertified_person))
