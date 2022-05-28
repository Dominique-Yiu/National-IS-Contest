from tslearn.datasets import CachedDatasets
from tslearn.preprocessing import TimeSeriesScalerMinMax
from tslearn.barycenters import softdtw_barycenter
import matplotlib.pyplot as plt
import numpy as np
from filter import iir_design_filter
from envelope_process import envelope
from variance import window_var
from modify_features import *
'''
#   直接SoftDTW生成不行 换一个思路 复杂度是n方 空间资源也是n方 权值的生成
'''
root_1 = "three/LXY_两快一慢"

plt.figure(figsize=(8, 2))
gross = []
for idx in range(2):
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
    gross.append(upper)
    # raw_data = TimeSeriesScalerMinMax().fit_transform(upper)
gross = np.array(gross)
gross = gross.reshape(gross.shape[0], gross.shape[1], 1)
gross = TimeSeriesScalerMinMax().fit_transform(gross)


for i, p in enumerate([-3, -1, 1]):
    bar = softdtw_barycenter(X=gross, gamma=10 ** p)
    plt.subplot(1, 3, i + 1)
    for ts in gross:
        plt.plot(ts.ravel(), "k-", alpha=.2)
    plt.plot(bar.ravel(), "r-")
plt.tight_layout()
plt.show()