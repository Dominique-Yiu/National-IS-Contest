import matlab.engine
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils.classifier import one_class_svm
from utils.filter import iir_design_filter
from utils.envelope_process import envelope
from utils.variance import window_var
from utils.modify_features import *
import os
import copy
import time
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def show(raw_time, raw_data,  start_time, start_seg):
    plt.figure(figsize=(16, 9))
    plt.plot(raw_time, raw_data)
    plt.draw()
    cnt = start_time.size[0]
    for idx in range(cnt):
        plt.plot(start_time[idx], start_seg[idx])
        plt.draw()
    plt.show()

root_1 = "three/LXY_两快一慢"
root_2 = "three/马爽_两慢一快"
root_3 = "six_seven/FIVELXY1"
root_4 = "six_seven/FIVELXY2"
root_5 = "six_seven/FIVEMS1"
root_6 = "six_seven/FIVEMS2"
# eng = matlab.engine.start_matlab()

# all_features = []
# all_index = []
# ''' 提取出所有原始特征 '''
# for idx in range(20):
#     if (idx + 1) < 10:
#         end = '0' + str(idx + 1)
#     else:
#         end = str(idx + 1)
#     path = root_3 + "/" + "FIVELXY1_" + str(idx + 1) + ".csv"
#     data = np.loadtxt(path, delimiter=",")
#     filter_module = iir_design_filter()
#     filtered_data = filter_module.filter_(raw_data=data)
#     upper, _ = envelope(filtered_data, 100).start()
#     upper = upper[int(2302 * 1):-int(2302 * 0.5)]
#     upper = upper.reshape(-1)
#     upper = matlab.double(initializer=list(upper), size=(1, len(upper)), is_complex=False)

#     current_time = time.time()
#     upper = eng.smoothdata(upper, 'gaussian', 200, nargout=1)
#     print(time.time() - current_time)
    
#     upper = upper[0]
#     np.savetxt(root_3 + "/" + "FIVELXY1_" + str(idx + 1) + "_smooth.csv", upper[::50])
#     var_upper = np.array(upper).astype(float)
#     rhythm_number = 6
    
#     current_time = time.time()
#     win = window_var(data=var_upper, head=rhythm_number, window=10)
#     end_points, _ = win.start()
#     # win.plot_()
#     end_points = np.sort(end_points)
#     end_points = end_points[1::2]
#     print(time.time() - current_time)
    
#     current_time = time.time()
#     start_points, data_time, data_seg, _time = eng.patterMatch(upper, rhythm_number, False, nargout=4)
#     # show(raw_time=_time[0], raw_data=upper, start_time=data_time, start_seg=data_seg)
#     if not isinstance(start_points, (float)):
#         start_points = np.array(start_points[0])
#     else:
#         start_points = np.array(start_points)
#     print(time.time() - current_time)

#     features = np.append(end_points, start_points)
#     features = np.sort(features)
#     features = np.sort(features) - features.min()
#     if len(features) == rhythm_number * 2:
#         all_features.append(features.tolist())
#         all_index.append(idx + 1)
# np.savetxt('./data/LXY_6_raw.csv', all_features)


from tslearn.preprocessing import TimeSeriesScalerMinMax
from tslearn.barycenters import softdtw_barycenter
from tslearn.utils import to_time_series_dataset
from tslearn.metrics import dtw, soft_dtw
import numpy as np
legal_user = np.loadtxt('./data/LXY_6_raw.csv')
#   随机选取八个作为训练样本
sample_index = []
while True:
    if len(sample_index) >= 8:
        break
    idx = np.random.randint(0, len(legal_user))
    if idx not in sample_index:
        sample_index.append(idx)
#   预测
train_data = legal_user[sample_index]
np.savetxt('./data/LXY_6_train.csv', train_data)
clf = one_class_svm(train_path='./data/LXY_6_train.csv')
clf.train_()
cnt = 0
for i in range(len(legal_user)):
    if clf.predict_(legal_user[i].reshape(1, -1)) == 1:
        cnt += 1
print('合法用户测试准确率： ', cnt/(len(legal_user)))
cnt = 0
attacker = np.loadtxt('./data/MS_3_raw.csv')
for i in range(len(attacker)):
    if clf.predict_(attacker[i].reshape(1, -1)) == -1:
        cnt += 1
print('非法用户测试准确率： ', cnt/(len(attacker)))

#   数据增强样本进行训练
# from utils.softdtw import SoftDBA
# from utils.modify_features import *
# eng = matlab.engine.start_matlab()
# rhythm_number = 6
# gross = []
# for idx in range(8):
#     if (idx + 1) < 10:
#         end = '0' + str(idx + 1)
#     else:
#         end = str(idx + 1)
#     path = root_3 + "/" + "FIVELXY1_" + str(idx + 1) + "_smooth.csv"
#     data = np.loadtxt(path, delimiter=",")
#     gross.append(data)
# G = SoftDBA(raw_data=gross, generate_num=20)
# generated_data = G.run()
# train_data = list(train_data)
# for upper in generated_data:
#     upper = upper.reshape(-1)
#     upper = matlab.double(initializer=list(upper), size=(1, len(upper)), is_complex=False)
#     upper = upper[0]
#     var_upper = np.array(upper).astype(float)
#     end_points, _ = window_var(data=var_upper, head=rhythm_number, window=5).start(distance=20)
#     end_points = np.sort(end_points)
#     end_points = end_points[1::2]
#     start_points, _, _, _ = eng.patterMatch(upper, rhythm_number, True, nargout=4)
#     if not isinstance(start_points, (float)):
#         start_points = np.array(start_points[0])
#     else:
#         start_points = np.array(start_points)
#     features = np.append(end_points, start_points)
#     features = np.sort(features) * 50
#     features = features - features.min()
#     if len(features) == rhythm_number * 2:
#         train_data.append(features)

# gross_data = np.array(train_data)
# np.savetxt('./data/LXY_6_ArgumentTrain.csv', train_data)

clf = one_class_svm(train_path='./data/LXY_6_ArgumentTrain.csv')
clf.train_()
cnt = 0
for i in range(len(legal_user)):
    if clf.predict_(legal_user[i].reshape(1, -1)) == 1:
        cnt += 1
print('合法用户测试准确率(数据增强): ', cnt/(len(legal_user)))
cnt = 0
attacker = np.loadtxt('./data/MS_3_raw.csv')
for i in range(len(attacker)):
    if clf.predict_(attacker[i].reshape(1, -1)) == -1:
        cnt += 1
print('非法用户测试准确率(数据增强): ', cnt/(len(attacker)))