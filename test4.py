import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import matlab.engine
from utils.envelope_process import envelope
from utils.filter import iir_design_filter
# eng = matlab.engine.start_matlab()

config = {
    "font.family": 'Times New Roman',
}
rcParams.update(config)

def process_data(data, flag=False):
    data = data  * 5 / 1024
    F = iir_design_filter() # f_pass=40.0, f_stop=48.0, a_pass=1.0, a_stop=80.0
    filtered_data = F.filter_(raw_data=data)
    if flag:
        return filtered_data[int(2302 * 2):]
    else:
        return filtered_data[int(2302 * 1):-int(2302 * 1)]

xtick_marks = [0,7,14,21,28]
ytick_marks = [0.8,1.2,1.6]
time = np.linspace(0, 28, int(2302 * 28))
plt.figure(figsize=(9, 6))

raw_data = np.loadtxt('office.csv', delimiter=',')
smooth_data = process_data(raw_data)
plt.plot(time, smooth_data, label='Office', linewidth=3)

raw_data = np.loadtxt('lab.csv', delimiter=',')
smooth_data = process_data(raw_data, True)
plt.plot(time, smooth_data, label='Laboratory', linewidth=3)

raw_data = np.loadtxt('outside.csv', delimiter=',')
smooth_data = process_data(raw_data)
plt.plot(time, smooth_data, label='Outdoor', linewidth=3)

plt.xticks(xtick_marks, fontsize=30, weight=10)
plt.yticks(ytick_marks, fontsize=30, weight=10)
plt.ylabel('Voltage (V)', fontsize=30)
plt.xlabel('Time (s)', fontsize=30)
plt.legend(fontsize=22, ncol=3, loc='upper center')
plt.xlim([0, 28])
plt.ylim([0.7, 1.6])
plt.tight_layout()

plt.show()