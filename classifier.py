from sklearn import svm
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
import numpy as np


class one_class_svm:
    def __init__(self, train_path='gross_features.csv', test_path=None, nu=0.1, kernel="rbf", gamma='scale', test_size=0.3, random_state=2021):
        self.y_train = None
        self.y_pred_train = None
        self.train_path = train_path
        self.test_path = test_path
        self.df = pd.read_csv(self.train_path, sep=' ', header=None)
        self.clf = svm.OneClassSVM(nu=nu, kernel=kernel, gamma=gamma)
        self.columns = self.df.shape[1]

    def train_(self):
        self.clf.fit(self.df)
        self.y_train = np.ones(len(self.df))
        self.y_pred_train = self.clf.predict(self.df)
        y_pred_train = pd.DataFrame(list(self.y_pred_train), columns=['predict'])

        # legal visitors accuracy
        train_accuracy = y_pred_train[y_pred_train['predict'] == 1].shape[0] / y_pred_train.shape[0]
        print(f'Training Data Accuracy(Positive): {train_accuracy}')
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