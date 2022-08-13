import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matlab.engine
from scipy.interpolate import interp1d
eng = matlab.engine.start_matlab()

config = {
    "font.family": 'Times New Roman',
}
rcParams.update(config)
data = np.loadtxt('smooth_YCW_5s.csv')
fs = 2302
time = 10
t = np.linspace(0, time, int(2302 * time))
data = data.reshape(-1)
upper = matlab.double(initializer=list(data), size=(1, len(data)), is_complex=False)
new_start, data_time, data_seg, _time, xcorr_value = eng.patterMatch(upper, 3, False, nargout=5)

t_t = t[::100]
xcorr_value = np.array(xcorr_value).astype(float).reshape(-1)
t_t = t_t[:len(xcorr_value)]
xx=np.linspace(t_t.min(), t_t.max(), int(2302 * time) - 1550)
f = interp1d(t_t, xcorr_value, kind='cubic')
y_new = f(xx)

fontdict = {
    'fontsize': 40,
    'fontweight': 'bold',
}
fontdict1 = {
    'fontsize': 40,
    # 'fontweight': 'bold',
    # 'color': '#1B679C'
}
fontdict2 = {
    'fontsize': 40,
    'fontweight': 'bold',
    'color': '#E0700C'
}
fig = plt.figure(figsize=(9.5, 6), dpi=150)
ax = fig.add_subplot(111)
data = (data - min(data)) / (max(data) - min(data))
lin1 = ax.plot(t, data, linewidth=5, color='#1B679C')

# ax2 = ax.twinx()
# lin2 = ax2.plot(xx, y_new, linewidth=5, color='#E0700C')

# plt.xticks(fontsize=35, weight=10)
# plt.yticks(fontsize=35, weight=10)
ax.set_ylabel('Norm. Voltage (V)', fontsize=40)
ax.set_xlabel('Time (s)', fontsize=40)
ax.set_yticks([0.0, 0.5, 1.0])
ax.set_ylim(-0.2, 1.2)
ax.set_yticklabels([0.0, 0.5, 1.0], fontdict=fontdict1)
ax.set_xlim(0, 10)
ax.set_xticklabels([0, 2, 4, 6, 8, 10], fontdict=fontdict1)
# loc_text_x=np.min(plt.xlim())+np.ptp(plt.xlim())*1.07
# loc_text_y=np.min(plt.ylim())+np.ptp(plt.ylim())*(-0.6)
# str_text='Correlation Coefficient'
# ax2.text(loc_text_x, loc_text_y, str_text,rotation=90,fontsize=35)
# ax2.spines["left"].set_color('#1B679C')
# ax2.spines["right"].set_color("#E0700C")
# ax2.spines["left"].set_linewidth(5)
# ax2.spines["right"].set_linewidth(5)
# ax2.set_xticks([0, 2, 4, 6, 8, 10])
# ax2.set_xlim(0, 10)
# ax2.set_xticklabels([0, 2, 4, 6, 8, 10], fontdict=fontdict)
# ax2.set_yticks([1])
# ax2.set_ylim(0.92, 1.04)
# ax2.set_yticklabels([1], fontdict=fontdict2)

# '''-----------------------'''
# plt.plot(xx, y_new, linewidth=5, color='#E0700C')
# '''-----------------------'''


# import peakdetect
# peaks = peakdetect.peakdetect(y_new, xx)
# p = None
# for idx in range(len(peaks)):
#     if p is None:
#         p = np.array(peaks[idx])
#     else:
#         p = np.concatenate([p, np.array(peaks[idx])], axis=0)
# p = np.array(sorted(p, key=lambda x: x[-1], reverse=True))
# plt.scatter(p[:4, 0], p[:4, 1], marker='.', color='g', s=1200, label='Touch Point')
# sca = ax2.scatter(p[:4, 0], p[:4, 1], marker='.', color='g', s=1200, label='Start Point')
# lines = lin1 + lin2
# ax.legend(lines, ['Smooth Signal', 'Correlation'], fontsize=26, loc='upper right')
# ax2.spines["left"].set_linewidth(5)
# ax2.spines["right"].set_linewidth(5)
# plt.xlim([0, xx[-1]])
# plt.ylim([0.95, 1.01])
# plt.ylabel('Correlation Value', fontsize=40)
# plt.xlabel('Time (s)', fontsize=40)
# plt.xticks([0, 2, 4, 6 , 8], fontsize=40)
# plt.yticks([0.96, 0.98, 1.00], fontsize=40)
# plt.legend(fontsize=35, loc='lower right')
plt.grid(axis='y', linewidth=2)
fig.align_labels()
plt.tight_layout()
plt.show()