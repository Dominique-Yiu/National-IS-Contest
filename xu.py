import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.interpolate import interp1d
from scipy.misc import derivative
from utils.envelope_process import envelope
from utils.filter import iir_design_filter
import matlab.engine
eng = matlab.engine.start_matlab()
config = {
    "font.family": 'Times New Roman',
}
rcParams.update(config)
# plt.rcParams['xtick.direction'] = 'in'
# plt.rcParams['ytick.direction'] = 'in'
def process_data(data):
    data = data  * 5 / 1024
    F = iir_design_filter(f_pass=40.0, f_stop=48.0, a_pass=1.0, a_stop=80.0) # f_pass=40.0, f_stop=48.0, a_pass=1.0, a_stop=80.0
    filtered_data = F.filter_(raw_data=data)
    upper, _ = envelope(filtered_data, 100).start()
    upper = upper.reshape(-1)
    smooth = matlab.double(initializer=list(upper), size=(1, len(upper)), is_complex=False)
    smooth = eng.smoothdata(smooth, 'gaussian', 800, nargout=1)
    smooth = smooth[0]
    
    return data[int(2302 * 0.5):-int(2302 * 0.5)], filtered_data[int(2302 * 0.5):-int(2302 * 0.5)], upper[int(2302 * 0.5):-int(2302 * 0.5)], smooth[int(2302 * 0.5):-int(2302 * 0.5)]
data = np.loadtxt('data_jin.csv', delimiter=',')
_, _, _, smooth_data = process_data(data)
smooth_data = np.array(smooth_data).astype(float).reshape(-1)
np.savetxt('xu_data.csv', smooth_data,delimiter=',')


fs = 2302
time = 120
t = np.linspace(0, time, int(2302 * time))
smooth_data = smooth_data[:int(2302 * time)]
# print(data.shape, t.shape)
# t_t = t[::5]
# t_data = smooth_data[::5]
# print(t_t.shape, test_data.shape)

f = interp1d(t, smooth_data, kind='cubic')
xx=np.linspace(t.min(), t.max(), int(2302 * time) * 2)
y_new = f(xx)

deravation = np.empty(int(2302 * time) - 1)
for idx in range(int(2302 * time) - 1):
    deravation[idx] = derivative(f, 0 + 1 / 2302 + idx / 2302, 1 / 2302)
d_t = t[:-1]
np.savetxt('xu_derivative.csv', deravation, delimiter=',')
fig = plt.figure(figsize=(10, 6), dpi=80)
ax = fig.add_subplot(111)
lin1 = ax.plot(t, smooth_data, linewidth=3, color='#1f77b4')

ax2 = ax.twinx()
lin2 = ax2.plot(d_t, deravation, linewidth=3, color='#ff7f0e')


fontdict = {
    'fontsize': 30,
    'weight': 10,
}
fontdict1 = {
    'fontsize': 30,
    'weight': 10,
    'color': '#1f77b4'
}
fontdict2 = {
    'fontsize': 30,
    'weight': 10,
    'color': '#ff7f0e'
}
# plt.xticks(fontsize=30, weight=10)
# plt.yticks(fontsize=30, weight=10)
# ax.set_ylabel('Voltage (V)', fontsize=30)
# ax.set_xlabel('Time (s)', fontsize=30)
# ax.set_yticks([1.2,1.6,2.0,2.4,2.8])
# ax.set_ylim(1.2, 2.8)
# ax.set_yticklabels([1.2,1.6,2.0,2.4,2.8], fontdict=fontdict1)
# ax.set_xlim(0, 14)
# ax.set_xticklabels([0, 2, 4, 6, 8, 10, 12, 14], fontdict=fontdict)
# loc_text_x=np.min(plt.xlim())+np.ptp(plt.xlim())*1.07
# loc_text_y=np.min(plt.ylim())+np.ptp(plt.ylim())*0.28
# str_text='Derivative Value'
# ax2.text(loc_text_x, loc_text_y, str_text,rotation=90,fontsize=30)
# ax2.spines["left"].set_color("#1f77b4")
# ax2.spines["right"].set_color("#ff7f0e")
# ax2.spines["left"].set_linewidth(3)
# ax2.spines["right"].set_linewidth(3)
# ax2.set_xticks([0, 2, 4, 6, 8, 10, 12, 14])
# ax2.set_xlim(0, 14)
# ax2.set_xticklabels([0, 2, 4, 6, 8, 10, 12, 14], fontdict=fontdict)
# ax2.set_yticks([-2, 0, 2, 4 ,6 ,8])
# ax2.set_ylim(-2, 8)
# ax2.set_yticklabels([-2, 0, 2, 4 ,6 ,8], fontdict=fontdict2)

import peakdetect
peaks = peakdetect.peakdetect(deravation, d_t)
p = None
for idx in range(len(peaks)):
    if p is None:
        p = np.array(peaks[idx])
    else:
        p = np.concatenate([p, np.array(peaks[idx])], axis=0)
p = np.array(sorted(p, key=lambda x: x[-1], reverse=True))
sca = ax2.scatter(p[:3, 0], p[:3, 1], marker='.', color='g', s=800, label='End Point')
lines = lin1 + lin2
ax.legend(lines, ['Smooth Signal', 'Derivative'], fontsize=25, loc='upper right')
plt.legend(fontsize=25, loc='upper left')
plt.tight_layout()
plt.show()