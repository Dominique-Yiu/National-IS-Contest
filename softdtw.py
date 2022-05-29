from mimetypes import init
from tslearn.preprocessing import TimeSeriesScalerMinMax
from tslearn.barycenters import softdtw_barycenter
from tslearn.utils import to_time_series_dataset, to_time_series
from tslearn.metrics import dtw, soft_dtw
import random
import matplotlib.pyplot as plt
import numpy as np
from filter import iir_design_filter
from envelope_process import envelope
from variance import window_var
from modify_features import *
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def generate_weights(timeSeries, gamma=10 ** -1):
    num_dim = timeSeries[0].shape[1]
    n = timeSeries.shape[0]
    max_k = 5
    max_subk = 2
    k = min(max_k, n - 1)
    subk = min(max_subk,k)
    weight_center = 0.5 + random.random() * 3 / 10.0
    weight_neighbors = (1 - weight_center) * 0.6
    weight_remaining = 1.0 - weight_center - weight_neighbors
    n_others = n - 1 - subk
    if n_others == 0 : 
        fill_value = 0.0
    else:
        fill_value = weight_remaining/n_others

    idx_center = random.randint(0,n-1)
    init_dba = timeSeries[idx_center]

    weights = np.full((n, num_dim), fill_value, dtype=np.float64)
    weights[idx_center] = weight_center
    dict = {}
    for idx in range(n):
        if idx != idx_center:
            distance = soft_dtw(ts1=init_dba, ts2=timeSeries[idx], gamma=gamma)
            dict[idx] = distance
    selected_dict = sorted(dict.items(), key=lambda x:x[1], reverse=False)[:k]
    final_neighbors_idx = np.random.permutation(k).astype(int)[:subk]
    final_neighbors = np.array(selected_dict, dtype=object)[final_neighbors_idx]
    weights[[item[0] for item in final_neighbors]] = weight_neighbors / subk
    return weights.reshape(-1)


root_1 = "three/LXY_两快一慢"
all_index = np.loadtxt('LXY_3_index.csv', dtype=int)
all_features = np.loadtxt('LXY_3.csv', dtype=int)
all_features = all_features[:,[0, -1]]
num = 0
gross = []
for idx in range(8):
    if (idx + 1) < 10:
        end = '0' + str(idx + 1)
    else:
        end = str(idx + 1)
    path = root_1 + "/" + "LXY_" + end + "_smooth.csv"
    data = np.loadtxt(path, delimiter=",")
    if (idx + 1) in all_index:
        data = data[all_features[num][0]:all_features[num][1]]
        num += 1
        
        # np.savetxt(root_1 + "/" + "LXY_" + end + "_clip.csv", data)
        data = data[::50].reshape(-1)
        # print(data.shape)
        gross.append(data)
formatted_dataset = to_time_series_dataset(gross)
scaled_dataset = TimeSeriesScalerMinMax().fit_transform(formatted_dataset)
print(scaled_dataset.shape)
plt.figure(figsize=(16, 8))
for ts in scaled_dataset:
    plt.plot(ts.ravel(), "k-", alpha=.2)
for i in range(10):
    weights = generate_weights(scaled_dataset)
    bar = softdtw_barycenter(X=scaled_dataset, gamma=10 ** -1, weights=weights)
    plt.plot(bar.ravel(), "r-", alpha=.5)
plt.xlabel("样本个数", fontsize=14)
plt.ylabel("归一化的电磁强度", fontsize=14)  # fontsize=18为名字大小
plt.tick_params(labelsize=12)  #刻度字体大小13
plt.legend()
plt.tight_layout()
plt.show()