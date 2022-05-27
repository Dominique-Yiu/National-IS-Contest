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

root_1 = "three/LXY_两快一慢"
root_2 = "three/马爽_两慢一快"
root_3 = "six_seven/FIVELXY1"
root_4 = "six_seven/FIVELXY2"
root_5 = "six_seven/FIVEMS1"
root_6 = "six_seven/FIVEMS2"
eng = matlab.engine.start_matlab()

# all_features = []
# for idx in range(55):
#     if (idx + 1) < 10:
#         end = '0' + str(idx + 1)
#     else:
#         end = str(idx + 1)
#     path = root_1 + "/" + "LXY_" + end + ".csv"
#     data = np.loadtxt(path, delimiter=",")
#     filter_module = iir_design_filter()
#     filtered_data = filter_module.filter_(raw_data=data)
#     upper, _ = envelope(filtered_data, 100).start()
#     upper = upper[int(2302 * 1):-int(2302 * 0.5)]
#     upper = upper.reshape(-1)
#     upper = matlab.double(initializer=list(upper), size=(1, len(upper)), is_complex=False)
#     upper = eng.smoothdata(upper, 'gaussian', 400, nargout=1)
#     upper = upper[0]
#     var_upper = np.array(upper).astype(float)
#     rhythm_number = 3
#     end_points, _ = window_var(data=var_upper, head=rhythm_number).start()
#     end_points = np.sort(end_points)
#     end_points = end_points[1::2]
#     start_points, data_time, data_seg, _time = eng.patterMatch(upper, rhythm_number, nargout=4)
#     start_points = np.array(start_points[0])
#     features = np.append(end_points, start_points)
#     features = np.sort(features) - features.min()
#     all_features.append(features.tolist())
# print(all_features)


ev_data = np.loadtxt('./output_data/smoothed_LXY_01.csv')
# plt.plot(ev_data)
# plt.show()
ev_data = matlab.double(initializer=list(ev_data), size=(1, len(ev_data)), is_complex=False)
smoothData = eng.smoothdata(ev_data, 'gaussian', 400, nargout=1)
# plt.plot(smoothData[0])
# plt.show()
new_start, data_time, data_seg, time = eng.patterMatch(smoothData, 3, nargout=4)
print(new_start)
def show(raw_time, raw_data,  start_time, start_seg):
    plt.figure(figsize=(16, 9))
    plt.plot(raw_time, raw_data)
    plt.draw()
    cnt = start_time.size[0]
    for idx in range(cnt):
        plt.plot(start_time[idx], start_seg[idx])
        plt.draw()
    plt.show()
print(data_time.size)
show(raw_time=time[0], raw_data=smoothData[0], start_time=data_time, start_seg=data_seg)



# eng.eval("ev_data = csvread('envelope_data_3.csv');", nargout=0)
# eng.eval("time = 1/2302:1/2302:length(ev_data)/2302;", nargout=0)
# eng.eval("C = smoothdata(ev_data, 'gaussian', 400);", nargout=0)
# D = eng.workspace["C"]
# plt.plot(D)
# plt.show()

