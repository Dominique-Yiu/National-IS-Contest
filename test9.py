import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.interpolate import interp1d
from scipy.misc import derivative
config = {
    "font.family": 'Times New Roman',
}
rcParams.update(config)
# plt.rcParams['xtick.direction'] = 'in'
# plt.rcParams['ytick.direction'] = 'in'

data = np.loadtxt('smooth_YCW_5s.csv')
test_data = data[::5]

fs = 2302
time = 10
t = np.linspace(0, time, int(2302 * time))
# print(data.shape, t.shape)
t_t = t[::5]
# print(t_t.shape, test_data.shape)

f = interp1d(t, data, kind='cubic')
xx=np.linspace(t_t.min(), t_t.max(), int(2302 * time) * 2)
y_new = f(xx)

deravation = np.empty(int(2302 * time) - 1)
for idx in range(int(2302 * time) - 1):
    deravation[idx] = derivative(f, 0 + 1 / 2302 + idx / 2302, 1 / 2302)
d_t = t[:-1]

fig = plt.figure(figsize=(9, 6), dpi=150)
ax = fig.add_subplot(111)
lin1 = ax.plot(t, data, linewidth=5, color='#1B679C')

# ax2 = ax.twinx()
# lin2 = ax2.plot(d_t, deravation, linewidth=5, color='#E0700C')


fontdict = {
    'fontsize': 40,
    # 'fontweight': 'bold',
}
fontdict1 = {
    'fontsize': 40,
    # 'fontweight': 'bold',
    # 'color': '#1B679C'
}
fontdict2 = {
    'fontsize': 40,
    # 'fontweight': 'bold',
    # 'color': '#E0700C'
}
plt.xticks(fontsize=40, weight=10)
plt.yticks(fontsize=40, weight=10)
ax.set_ylabel('Voltage (V)', fontsize=40)
ax.set_xlabel('Time (s)', fontsize=40)
ax.set_yticks([0.8, 1.2, 1.6, 2.0])
ax.set_ylim(0.6, 2.2)
ax.set_yticklabels([0.8, 1.2,1.6,2.0], fontdict=fontdict2)
ax.set_xlim(0, 10)
ax.set_xticklabels([0, 2, 4, 6, 8, 10], fontdict=fontdict)


# loc_text_x=np.min(plt.xlim())+np.ptp(plt.xlim())*1.07
# loc_text_y=np.min(plt.ylim())+np.ptp(plt.ylim())*0.3
# str_text='Derivative Value'
# ax2.text(loc_text_x, loc_text_y, str_text,rotation=90,fontsize=35)
# ax2.spines["left"].set_color('#1B679C')
# ax2.spines["right"].set_color('#E0700C')
# ax2.spines["left"].set_linewidth(5)
# ax2.spines["right"].set_linewidth(5)
# ax2.set_ylabel('Derivative Value', fontsize=40)
# ax2.set_xlabel('Time (s)', fontsize=40)
# ax2.set_xticks([0, 2, 4, 6, 8, 10])
# ax2.set_xlim(0, 10)
# ax2.set_xticklabels([0, 2, 4, 6, 8, 10], fontdict=fontdict)
# ax2.set_yticks([-2, 0, 2, 4])
# ax2.set_ylim(-2.5, 4.5)
# ax2.set_yticklabels([-2.0, 0, 2.0, 4.0], fontdict=fontdict2)

# import peakdetect
# peaks = peakdetect.peakdetect(deravation, d_t)
# p = None
# for idx in range(len(peaks)):
#     if p is None:
#         p = np.array(peaks[idx])
#     else:
#         p = np.concatenate([p, np.array(peaks[idx])], axis=0)
# p = np.array(sorted(p, key=lambda x: x[-1], reverse=True))
# top_peak = p[:4, :]
# zero_point = np.empty([4, 2])
# for i in range(len(top_peak)):
#     pos = int(top_peak[i, 0] * 2302)
#     for j in range(pos, 0, -1):
#         if np.abs(deravation[j] - 0) < 10e-3:
#             zero_point[i, 0] = j / 2302
#             zero_point[i, 1] = deravation[j]
#             break

# sca = ax2.scatter(top_peak[:, 0], top_peak[:, 1], marker='.', color='g', s=1200, label='Release Point')
# sca = ax2.scatter(zero_point[:, 0], zero_point[:, 1], marker='.', color='r', s=1200, label='True Point')
# lines = lin1 + lin2
# ax.legend(lines, ['Smooth Signal', 'Derivative'], fontsize=26, loc='upper right')
# plt.legend(fontsize=30, loc='upper right')
plt.grid(axis='y', linewidth=2)
plt.tight_layout()
plt.show()