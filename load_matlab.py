import matlab.engine
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from filter import iir_design_filter
from envelope_process import envelope
from variance import window_var
from modify_features import *
import os
import copy
import time

root_1 = "three/LXY_两快一慢"
root_2 = "three/马爽_两慢一快"
root_3 = "six_seven/FIVELXY1"
root_4 = "six_seven/FIVELXY2"
root_5 = "six_seven/FIVEMS1"
root_6 = "six_seven/FIVEMS2"
eng = matlab.engine.start_matlab()

all_features = []
all_index = []
for idx in range(1):
    if (idx + 1) < 10:
        end = '0' + str(idx + 1)
    else:
        end = str(idx + 1)
    path = root_1 + "/" + "LXY_" + end + ".csv"
    data = np.loadtxt(path, delimiter=",")
    filter_module = iir_design_filter()
    filtered_data = filter_module.filter_(raw_data=data)
    upper, _ = envelope(filtered_data, 100).start()
    upper = upper[int(2302 * 1):-int(2302 * 0.5)]
    upper = upper.reshape(-1)
    upper = matlab.double(initializer=list(upper), size=(1, len(upper)), is_complex=False)

    current_time = time.time()
    upper = eng.smoothdata(upper, 'gaussian', 400, nargout=1)
    print(time.time() - current_time)
    
    upper = upper[0]
    np.savetxt(root_1 + "/" + "LXY_" + end + "_smooth.csv", upper)
    var_upper = np.array(upper).astype(float)
    rhythm_number = 3
    
    current_time = time.time()
    end_points, _ = window_var(data=var_upper, head=rhythm_number).start()
    end_points = np.sort(end_points)
    end_points = end_points[1::2]
    print(time.time() - current_time)
    
    current_time = time.time()
    start_points, data_time, data_seg, _time = eng.patterMatch(upper, rhythm_number, False, nargout=4)
    if not isinstance(start_points, (float)):
        start_points = np.array(start_points[0])
    else:
        start_points = np.array(start_points)
    print(time.time() - current_time)

    features = np.append(end_points, start_points)
    features = np.sort(features)
    # features = np.sort(features) - features.min()
    if len(features) == rhythm_number * 2:
        all_features.append(features.tolist())
        all_index.append(idx + 1)
np.savetxt('LXY_3.csv', all_features)
np.savetxt('LXY_3_index.csv', all_index)

# from tslearn.preprocessing import TimeSeriesScalerMinMax
# from tslearn.barycenters import softdtw_barycenter
# from tslearn.utils import to_time_series_dataset
# from tslearn.metrics import dtw, soft_dtw
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False

# path = root_1 + "/" + "LXY_" + '10' + "_smooth.csv"
# plt.figure(figsize=(16, 8))
# data = np.loadtxt(path, delimiter=",")
# plt.subplot(1, 2, 1)
# plt.plot(data, label='原始数据')
# plt.xlabel("样本个数", fontsize=14)
# plt.ylabel("电磁强度", fontsize=14)  # fontsize=18为名字大小
# plt.legend()
# plt.tick_params(labelsize=12)  #刻度字体大小13
# sample_data = data[::50]
# plt.subplot(1, 2, 2)
# plt.plot(sample_data, label='采样数据')
# plt.xlabel("样本个数", fontsize=12)
# plt.ylabel("电磁强度", fontsize=12)  # fontsize=18为名字大小
# plt.tick_params(labelsize=12)  #刻度字体大小13
# plt.legend()
# plt.show()


# all_index = np.loadtxt('LXY_3_index.csv', dtype=int)
# all_features = np.loadtxt('LXY_3.csv', dtype=int)
# all_features = all_features[:,[0, -1]]
# num = 0
# gross = []
# for idx in range(55):
#     if (idx + 1) < 10:
#         end = '0' + str(idx + 1)
#     else:
#         end = str(idx + 1)
#     path = root_1 + "/" + "LXY_" + end + "_smooth.csv"
#     data = np.loadtxt(path, delimiter=",")
#     if (idx + 1) in all_index:
#         data = data[all_features[num][0]:all_features[num][1]]
#         num += 1
        
#         # np.savetxt(root_1 + "/" + "LXY_" + end + "_clip.csv", data)
#         data = data[::50].reshape(-1)
#         # print(data.shape)
#         gross.append(data)
# formatted_dataset = to_time_series_dataset(gross)
# scaled_dataset = TimeSeriesScalerMinMax().fit_transform(formatted_dataset)
# print(scaled_dataset[0].shape)

# plt.figure(figsize=(8, 2))
# for i, p in enumerate([-3, -1, 1]):
#     bar = softdtw_barycenter(X=scaled_dataset, gamma=10 ** p)
#     plt.subplot(1, 3, i + 1)
#     for ts in scaled_dataset:
#         plt.plot(ts.ravel(), "k-", alpha=.2)
#     plt.plot(bar.ravel(), "r-")

# plt.tight_layout()
# plt.show()



# ev_data = np.loadtxt(root_1 + "/" + "LXY_" + '40' + "_smooth.csv")
# plt.figure(figsize=(9,2))
# plt.subplot(1, 3, 1)
# plt.plot(ev_data)
# plt.subplot(1, 3, 2)
# sample_data = ev_data[::50]
# plt.plot(sample_data)
# plt.subplot(1, 3, 3)
# recover_data = np.zeros((len(sample_data), 50))
# for idx, item in enumerate(sample_data):
#     recover_data[idx][:] = item
# plt.plot(recover_data.ravel())
# plt.show()

# ev_data = matlab.double(initializer=list(ev_data), size=(1, len(ev_data)), is_complex=False)
# smoothData = eng.smoothdata(ev_data, 'gaussian', 400, nargout=1)
# new_start, data_time, data_seg, time = eng.patterMatch(smoothData, 3, nargout=4)

# def show(raw_time, raw_data,  start_time, start_seg):
#     plt.figure(figsize=(16, 9))
#     plt.plot(raw_time, raw_data)
#     plt.draw()
#     cnt = start_time.size[0]
#     for idx in range(cnt):
#         plt.plot(start_time[idx], start_seg[idx])
#         plt.draw()
#     plt.show()
# show(raw_time=time[0], raw_data=smoothData[0], start_time=data_time, start_seg=data_seg)



# eng.eval("ev_data = csvread('envelope_data_3.csv');", nargout=0)
# eng.eval("time = 1/2302:1/2302:length(ev_data)/2302;", nargout=0)
# eng.eval("C = smoothdata(ev_data, 'gaussian', 400);", nargout=0)
# D = eng.workspace["C"]
# plt.plot(D)
# plt.show()

