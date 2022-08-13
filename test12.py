import psutil
import os
import numpy as np
from sympy import arg
from utils.classifier import one_class_svm
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
import datetime
config = {
    "font.family": 'Times New Roman',
}
rcParams.update(config)
# # 获取逻辑cpu的数量
# count = psutil.cpu_count()
# print(f"逻辑cpu的数量是{count}")
# # Process实例化时不指定pid参数，默认使用当前进程PID，即
# print(os.getpid())
# p = psutil.Process()
# cpu_lst = p.cpu_affinity()
# print("cpu列表", cpu_lst)

# config = {
#     "font.family": 'Times New Roman',
# }
# rcParams.update(config)
# def process_features(data):
#     length = len(data)
#     for idx in range(length):
#         data[idx][np.where(data[idx] == 0)[0]] = data[idx][1]
#     return data



# acc = []
# cpu_usage = []
# arg_list = ['data/one_arg.csv', 'data/two_arg.csv', 'data/three_arg.csv', 'data/four_arg.csv', 'data/five_arg.csv']
# raw_list = ['data/one_raw.csv', 'data/two_raw.csv', 'data/three_raw.csv', 'data/four_raw.csv', 'data/five_raw.csv']
# # 将当前进程绑定到cpu0上运行，列表中也可以写多个cpu
# for cpu_num in range(len(cpu_lst)):

#     starttime = datetime.datetime.now()
#     p.cpu_affinity(cpu_lst[:cpu_num+1])

#     length = [0, 0, 0, 0, 0, 0]
#     X_test = None
#     y_test = None
#     for i in range(5):
#         if X_test is None:
#             X_test = pd.read_csv(arg_list[i], sep=' ', header=None)
#         else:
#             X_test = add_modify(data=X_test, add_data=pd.read_csv(arg_list[i], sep=' ', header=None))
#         length[i] = len(pd.read_csv(arg_list[i], sep=' ', header=None))
#         if y_test is None:
#             y_test = (-np.ones(len(X_test))).reshape(-1)
#         else:
#             y_test = np.r_[y_test, (-np.ones(length[i])).reshape(-1)]

#     clf = one_class_svm(train_path=arg_list[4])
#     # clf.train_(rand=np.random.randint(1, 3) * np.array([-1, 1])[np.random.randint(0, 2)])
#     clf.train_()


#     y_test[sum(length[:4]):] = 1
#     pred = []
#     couterfalse = 0
#     coutertrue = 0




#     for idx, item in enumerate(X_test):
#         pred.append(clf.predict_(X_test[idx][:].reshape(1, -1))[0])
#         if(clf.predict_(X_test[idx][:].reshape(1, -1))) == -1:
#             couterfalse += 1
#         else:
#             coutertrue += 1
#     # print(counttrue/(counttrue+countfalse))

#     endtime = datetime.datetime.now()
#     acc.append(sum(pred == np.array(y_test)) / len(pred))
#     cpu_usage.append((cpu_num+1) / len(cpu_lst))
#     print(f'Running time: {endtime-starttime} Seconds; CPU Usage: {(cpu_num+1) / len(cpu_lst)}')
# print(acc)
plt.figure(figsize=(9, 6))
# x = list(range(8))
x = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

acc = [95.35, 96.70, 95.81, 96.24, 94.13, 95.80, 95.32, 96.21, 95.20,  95.56]
plt.plot(x, acc, linewidth=5, marker='^', clip_on=False, markersize=18, linestyle='--')
plt.xticks(x, fontsize=26)
plt.yticks([90, 92, 94, 96, 98, 100], fontsize=30)
plt.xlabel('CPU Usage (%)',fontsize=30)
plt.ylabel('Authetication Accuracy (%)', fontsize=30)
plt.xlim([10, 100])
plt.ylim([90, 100])
plt.grid(axis='y', linewidth=2)
# plt.grid(linewidth=2)
plt.tight_layout()
plt.show()