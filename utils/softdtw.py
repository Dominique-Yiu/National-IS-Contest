from mimetypes import init
from tslearn.preprocessing import TimeSeriesScalerMinMax
from tslearn.barycenters import softdtw_barycenter
from tslearn.utils import to_time_series_dataset, to_time_series
from tslearn.metrics import dtw, soft_dtw
import matplotlib.pyplot as plt
import numpy as np
from .modify_features import *
import matlab.engine
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def generate_weights(timeSeries, gamma=10 ** -1):
    num_dim = timeSeries[0].shape[1]
    n = timeSeries.shape[0]
    max_k = 5
    max_subk = 2
    k = min(max_k, n - 1)
    subk = min(max_subk,k)
    weight_center = 0.5 + np.random.rand() / 10.0
    weight_neighbors = (1 - weight_center) * 0.6
    weight_remaining = 1.0 - weight_center - weight_neighbors
    n_others = n - 1 - subk
    if n_others == 0 : 
        fill_value = 0.0
    else:
        fill_value = weight_remaining/n_others

    idx_center = np.random.randint(0,n-1)
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

class SoftDBA:

    def __init__(self, raw_data, generate_num=10, gamma=10 ** -1) -> None:
        self.data = TimeSeriesScalerMinMax().fit_transform(to_time_series_dataset(raw_data))
        self.generate_num = generate_num
        self.gamma = gamma

    def run(self):
        generated_data = []

        for _ in range(self.generate_num):
            weights = generate_weights(self.data)
            bar = softdtw_barycenter(X=self.data, gamma=self.gamma, weights=weights)
            generated_data.append(bar) 
        
        return generated_data

def show(raw_time, raw_data,  start_time, start_seg):
    plt.figure(figsize=(16, 9))
    plt.plot(raw_time, raw_data)
    plt.draw()
    cnt = start_time.size[0]
    for idx in range(cnt):
        plt.plot(start_time[idx], start_seg[idx])
        plt.draw()
    plt.show()

if __name__=='__main__':
    eng = matlab.engine.start_matlab()
    root_1 = "three/LXY_两快一慢"
    gross = []
    for idx in range(8):
        if (idx + 1) < 10:
            end = '0' + str(idx + 1)
        else:
            end = str(idx + 1)
        path = root_1 + "/" + "LXY_" + end + "_smooth.csv"
        data = np.loadtxt(path, delimiter=",")
        gross.append(data)
    G = SoftDBA(raw_data=gross, generate_num=10)
    for upper in G.data:
        upper = upper.reshape(-1)
        upper = matlab.double(initializer=list(upper), size=(1, len(upper)), is_complex=False)
        start_points, data_time, data_seg, _time = eng.patterMatch(upper, 3, True, nargout=4)
        show(raw_time=_time[0], raw_data=upper[0], start_time=data_time, start_seg=data_seg)
    generated_data = G.run()
    for upper in generated_data:
        upper = upper.reshape(-1)
        upper = matlab.double(initializer=list(upper), size=(1, len(upper)), is_complex=False)
        start_points, data_time, data_seg, _time = eng.patterMatch(upper, 3, True, nargout=4)
        show(raw_time=_time[0], raw_data=upper[0], start_time=data_time, start_seg=data_seg)
    # plt.figure(figsize=(16, 8))
    # for ts in G.data:
    #     plt.plot(ts.ravel(), "k-", alpha=.2)
    # generated_data = G.run()
    # for bar in generated_data:
    #     plt.plot(bar.ravel(), "r-", alpha=.5)
    # plt.xlabel("样本个数", fontsize=18)
    # plt.ylabel("归一化的电磁强度", fontsize=18)  # fontsize=18为名字大小
    # plt.tick_params(labelsize=15)  #刻度字体大小13
    # plt.tight_layout()
    # plt.show()