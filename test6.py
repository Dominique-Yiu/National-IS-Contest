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

def process_data(data):
    data = data  * 5 / 1024
    F = iir_design_filter() # f_pass=40.0, f_stop=48.0, a_pass=1.0, a_stop=80.0
    filtered_data = F.filter_(raw_data=data)

    return filtered_data[int(2302 * 2):]
plt.figure(figsize=(6, 4))
time = np.linspace(0, 8, int(2302 * 8))
raw_data = np.loadtxt('open_speaker.csv', delimiter=',')
smooth_data = process_data(raw_data)
plt.plot(time, smooth_data, label='Smart Speaker', linewidth=3)

xtick_marks = [0, 2, 4, 6 ,8]
ytick_marks = [0.4, 0.6, 0.8, 1.0,  1.2]
plt.xlim([0, 8])
plt.xticks(xtick_marks, fontsize=25, weight=10)
plt.yticks(ytick_marks, fontsize=25, weight=10)
plt.ylabel('Voltage (V)', fontsize=25)
plt.xlabel('Time (s)', fontsize=25)
plt.legend(fontsize=18, ncol=3, loc='upper left')
plt.tight_layout()

plt.show()