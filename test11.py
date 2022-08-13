from copy import copy, deepcopy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import StratifiedKFold
from utils.classifier import one_class_svm
from utils.filter import iir_design_filter
from utils.envelope_process import envelope
from utils.variance import window_var
from utils.modify_features import *
from matplotlib import rcParams, artist
config = {
    "font.family": 'Times New Roman',
}
rcParams.update(config)
def process_features(data):
    length = len(data)
    for idx in range(length):
        data[idx][np.where(data[idx] == 0)[0]] = data[idx][1]
    return data

arg_list = ['data/one_arg.csv', 'data/two_arg.csv', 'data/three_arg.csv', 'data/four_arg.csv', 'data/five_arg.csv']
raw_list = ['data/one_raw.csv', 'data/two_raw.csv', 'data/three_raw.csv', 'data/four_raw.csv', 'data/five_raw.csv']


length = [0, 0, 0, 0, 0, 0]
X_test = None
y_test = None
for i in range(5):
    if X_test is None:
        X_test = pd.read_csv(arg_list[i], sep=' ', header=None)
    else:
        X_test = add_modify(data=X_test, add_data=pd.read_csv(arg_list[i], sep=' ', header=None))
    length[i] = len(pd.read_csv(arg_list[i], sep=' ', header=None))
    if y_test is None:
        y_test = (-np.ones(len(X_test))).reshape(-1)
    else:
        y_test = np.r_[y_test, (-np.ones(length[i])).reshape(-1)]
# X_test = add_modify(data=X_test, add_data=pd.read_csv(raw_list[1], sep=' ', header=None))
# length[5] = len(pd.read_csv(raw_list[1], sep=' ', header=None))
# y_test = np.r_[y_test, (-np.ones(length[5])).reshape(-1)]

fig = plt.figure(figsize=(9, 6))
marker= ['X', 'D', 'P', 'H', 'o', '^']
legend = ['Arduino Mega', 'M5StickC PLUS', 'Arduino Nano & Smart Speaker', 'Arduino Nano & Smart Camera','Arduino Nano & Printer', 'Arduino Nano & Rice Cooker']
max_value = 0
for i in range(6):
    j = i if i < 5 else 5
    i = i % 5
    begin = sum(length[:i])
    y_test[:] = -1
    
    cnt = np.random.randint(1, 3) * np.array([-1, 1])[np.random.randint(0, 2)]
    
    end = begin+length[i]+cnt if begin+length[i]+cnt <= 81 else 81
    begin = begin+cnt if begin + cnt >= 0 else 0
    print(cnt, begin, end)
    y_test[begin:end] = 1
    X_train = X_test[begin:end, :]
    y_train = np.ones(len(X_train)).reshape(-1)
    n_samples, n_features = X_train.shape
    classifier = svm.OneClassSVM(kernel='rbf', gamma='scale')
    print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)
    print(y_test)
    classifier.fit(X_train, y_train)
    # classifier.fit(X_test, y_test)
    fpr, tpr, thresholds = roc_curve(y_test, classifier.decision_function(X_test))
    pos = np.where(fpr <= 0.5)[0][-1]
    fpr = fpr[:pos]
    max_value = fpr[-1] if fpr[-1] > max_value else max_value
    tpr = tpr[:pos]
    plt.plot(fpr, tpr, marker=marker[j], label=legend[j], linewidth=4, clip_on=False, markersize=13)


# str_text='True Positive Rate'
# loc_text_x=np.min(plt.xlim())-np.ptp(plt.xlim())*(0.08)
# loc_text_y=np.min(plt.ylim())+np.ptp(plt.ylim())*(0.22)
# plt.text(loc_text_x, loc_text_y, str_text, rotation=90, fontsize=30)
plt.xlabel('False Positive Rate', fontsize=30)
plt.ylabel('True Positive Rate', fontsize=30)    
plt.legend(loc="lower right", fontsize=25)
plt.ylim(0,1)
plt.xlim(0, max_value)
plt.xticks([0, 0.1, 0.2 ,0.3, 0.4], fontsize=30)
plt.yticks(fontsize=30)
plt.tight_layout()
plt.show()