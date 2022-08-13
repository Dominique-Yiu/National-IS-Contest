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

def process_data(data, flag=False):
    data = data  * 5 / 1024
    F = iir_design_filter() # f_pass=40.0, f_stop=48.0, a_pass=1.0, a_stop=80.0
    filtered_data = F.filter_(raw_data=data)
    upper, _ = envelope(filtered_data, 100).start()
    upper = upper.reshape(-1)
    upper = matlab.double(initializer=list(upper), size=(1, len(upper)), is_complex=False)
    upper = eng.smoothdata(upper, 'gaussian', 200, nargout=1)
    upper = upper[0]
    upper = np.array(upper).astype(float)

    # return upper[int(2302 * 1):-int(2302 * 0.5)]
    if flag:
        return upper[int(2302 * 1):-int(2302 * 0.5)]
    else:
        return upper[int(2302 * 0.5):-int(2302 * 1)]

# xtick_marks = [0, 5, 10, 15, 20, 25, 30]
# time = np.linspace(0, 28.5, int(2302 * 28.5))
# plt.figure(figsize=(9, 7))
# plt.subplot(2, 2, 1)
# raw_data = np.loadtxt('voice.csv', delimiter=',')
# smooth_data = process_data(raw_data)
# plt.plot(time, smooth_data)
# plt.xticks(xtick_marks, fontsize=18, weight=10)
# ytick_marks = np.round(np.array([50, 100, 150, 200, 250, 300, 350]) * 5 / 1024, 2)
# plt.yticks(ytick_marks, fontsize=18, weight=10)
# plt.ylabel('Voltage(V)', fontsize=18)
# plt.xlabel('time (s)', fontsize=18)
# plt.tight_layout()

# plt.subplot(2, 2, 2)
# raw_data = np.loadtxt('printer.csv', delimiter=',')
# smooth_data = process_data(raw_data)
# plt.plot(time, smooth_data)
# plt.xticks(xtick_marks, fontsize=18, weight=10)
# ytick_marks = np.round(np.array([100, 150, 200, 250, 300, 350, 400]) * 5 / 1024, 2)
# plt.yticks(ytick_marks, fontsize=18, weight=10)
# plt.ylabel('Voltage(V)', fontsize=18)
# plt.xlabel('time (s)', fontsize=18)
# plt.tight_layout()

# plt.subplot(2, 2, 3)
# raw_data = np.loadtxt('cooker.csv', delimiter=',')
# smooth_data = process_data(raw_data)
# plt.plot(time, smooth_data)
# plt.xticks(xtick_marks, fontsize=18, weight=10)
# ytick_marks = np.round(np.array([100, 130, 160, 190, 220, 250, 280]) * 5 / 1024, 2)
# plt.yticks(ytick_marks, fontsize=18, weight=10)
# plt.ylabel('Voltage(V)', fontsize=18)
# plt.xlabel('time (s)', fontsize=18)
# plt.tight_layout()

# plt.subplot(2, 2, 4)
# raw_data = np.loadtxt('camera.csv', delimiter=',')
# smooth_data = process_data(raw_data)
# plt.plot(time, smooth_data)
# plt.xticks(xtick_marks, fontsize=18, weight=10)
# ytick_marks = np.round(np.array([130, 150, 170, 190, 210, 230, 250]) * 5 / 1024, 2)
# plt.yticks(ytick_marks, fontsize=18, weight=10)
# plt.ylabel('Voltage(V)', fontsize=18)
# plt.xlabel('time (s)', fontsize=18)
# plt.tight_layout()



xtick_marks = [0, 7, 14, 21, 28]
time = np.linspace(0, 28.5, int(2302 * 28.5))
plt.figure(figsize=(9, 7))

raw_data = np.loadtxt('voice.csv', delimiter=',')
smooth_data = process_data(raw_data)
plt.plot(time, smooth_data, label='Smart Speaker', linewidth=4)

raw_data = np.loadtxt('printer.csv', delimiter=',')
smooth_data = process_data(raw_data)
plt.plot(time, smooth_data, label='Printer', linewidth=4)

raw_data = np.loadtxt('cooker.csv', delimiter=',')
smooth_data = process_data(raw_data)
plt.plot(time, smooth_data, label='Rice Cooker', linewidth=4)

raw_data = np.loadtxt('camera.csv', delimiter=',')
smooth_data = process_data(raw_data, True)
plt.plot(time, smooth_data, label='Smart Camera', linewidth=4)
plt.xticks(xtick_marks, fontsize=35)
ytick_marks = [0.6,1.0,1.4,1.8]
plt.yticks(ytick_marks, fontsize=35, weight=10)
plt.ylabel('Voltage (V)', fontsize=35)
plt.xlabel('Time (s)', fontsize=35)
plt.legend(fontsize=25, ncol=2, loc='upper center')
plt.xlim([0, 28.5])
plt.tight_layout()

plt.show()