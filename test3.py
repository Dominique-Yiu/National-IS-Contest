import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import matlab.engine
from utils.envelope_process import envelope
from utils.filter import iir_design_filter
eng = matlab.engine.start_matlab()

config = {
    "font.family": 'Times New Roman',
}
rcParams.update(config)

def process_data(data):
    data = data  * 5 / 1024
    F = iir_design_filter() # f_pass=40.0, f_stop=48.0, a_pass=1.0, a_stop=80.0
    filtered_data = F.filter_(raw_data=data)
    upper, _ = envelope(filtered_data, 100).start()
    upper = upper.reshape(-1)
    upper = matlab.double(initializer=list(upper), size=(1, len(upper)), is_complex=False)
    upper = eng.smoothdata(upper, 'gaussian', 300, nargout=1)
    upper = upper[0]

    return np.array(upper).astype(float)[int(2302 * 1):-int(2302 * 0.5)]

time = np.linspace(0, 13.5, int(2302 * 13.5))
plt.figure(figsize=(9, 7))


ytick_marks = [0.9,1.3,1.7,2.1]
xtick_marks = [0, 4, 8, 12]
plt.subplot(2, 2, 1)
raw_data = np.loadtxt('raw_data/four_rhythm/true/four_1.csv', delimiter=',')
smooth_data = process_data(raw_data)
plt.plot(time, smooth_data, label='06:00', linewidth=4, color='#1f77b4')
plt.xticks(xtick_marks,fontsize=35, weight=10)
plt.yticks(ytick_marks, fontsize=35, weight=10)
plt.ylabel('Voltage (V)', fontsize=35)
plt.xlabel('Time (s)', fontsize=35)
plt.legend(fontsize=22, ncol=1, loc='upper right')
plt.xlim([0, 13.5])
plt.tight_layout()

plt.subplot(2, 2, 2)
raw_data = np.loadtxt('raw_data/four_rhythm/true/four_2.csv', delimiter=',')
smooth_data = process_data(raw_data)
plt.plot(time, smooth_data, label='12:00', linewidth=4, color='#ff7f0e')
plt.xticks(xtick_marks,fontsize=35, weight=10)
plt.yticks(ytick_marks, fontsize=35, weight=10)
plt.ylabel('Voltage (V)', fontsize=35)
plt.xlabel('Time (s)', fontsize=35)
plt.legend(fontsize=22, ncol=1, loc='upper right')
plt.xlim([0, 13.5])
plt.tight_layout()

plt.subplot(2, 2, 3)
raw_data = np.loadtxt('raw_data/four_rhythm/true/four_5.csv', delimiter=',')
smooth_data = process_data(raw_data)
plt.plot(time, smooth_data, label='18:00', linewidth=4, color='#2ca02c')
plt.xticks(xtick_marks, fontsize=35, weight=10)
plt.yticks(ytick_marks, fontsize=35, weight=10)
plt.ylabel('Voltage (V)', fontsize=35)
plt.xlabel('Time (s)', fontsize=35)
plt.legend(fontsize=22, ncol=1, loc='upper right')
plt.xlim([0, 13.5])
plt.tight_layout()

plt.subplot(2, 2, 4)
raw_data = np.loadtxt('raw_data/four_rhythm/true/four_4.csv', delimiter=',')
smooth_data = process_data(raw_data)
plt.plot(time, smooth_data, label='24:00', linewidth=4, color='#d62728')
plt.xticks(xtick_marks, fontsize=35, weight=10)
plt.yticks(ytick_marks, fontsize=35, weight=10)
plt.ylabel('Voltage (V)', fontsize=35)
plt.xlabel('Time (s)', fontsize=35)
plt.legend(fontsize=22, ncol=1, loc='upper right')
plt.xlim([0, 13.5])
plt.tight_layout()

plt.show()