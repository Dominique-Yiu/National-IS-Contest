import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
from utils.envelope_process import envelope
from utils.filter import iir_design_filter
import matlab.engine
eng = matlab.engine.start_matlab()
config = {
    "font.family": 'Times New Roman',
}
rcParams.update(config)

def process_data(data):
    data = data  * 5 / 1024
    # data = (data - min(data)) / (max(data) - min(data))
    F = iir_design_filter(f_pass=40.0, f_stop=48.0, a_pass=1.0, a_stop=80.0) # f_pass=40.0, f_stop=48.0, a_pass=1.0, a_stop=80.0
    filtered_data = F.filter_(raw_data=data)
    upper, _ = envelope(filtered_data, 100).start()
    upper = upper.reshape(-1)
    smooth = matlab.double(initializer=list(upper), size=(1, len(upper)), is_complex=False)
    smooth = eng.smoothdata(smooth, 'gaussian', 300, nargout=1)
    smooth = smooth[0]
    
    return data[int(2302 * 2):], filtered_data[int(2302 * 2):], upper[int(2302 * 2):], smooth[int(2302 * 2):]
raw_data = np.loadtxt('YCW_8s_1.csv', delimiter=',')

import matplotlib.pyplot as plt
data, filtered_data, upper, smooth = process_data(raw_data)
# np.savetxt('smooth_YCW_5s.csv', smooth)
fs = 2302
time = 10
t = np.linspace(0, time, int(2302 * time))
plt.figure(figsize=(9, 6), dpi=150)
# plt.subplot(1, 2, 2)
# plt.plot(t, data, label='Original Signal', linewidth=5)
# plt.plot(t, filtered_data, label='Filtered Signal', linewidth=4)
# plt.plot(t, upper, label='Envelope Signal', linewidth=4)
# smooth = np.array(smooth).astype(float).reshape(-1)
# smooth = (smooth - min(smooth)) / (max(smooth) - min(smooth))
# plt.plot(t, smooth, color='#1B679C', linewidth=5)
# plt.xlim([0, 10])
# plt.ylim([-0.2, 3.2])
# plt.xticks([0, 2, 4, 6 ,8 ,10], fontsize=40)
# plt.yticks([0, 1, 2, 3],fontsize=40)
# plt.ylabel('Voltage (V)', fontsize=40)
# plt.xlabel('Time (s)', fontsize=40)
# plt.legend(fontsize=25)



# plt.subplot(1, 2, 2)
# plt.plot(t[:int(0.51 * 2302)], data[:int(0.51 * 2302)], label='No Human Coupling Effect', linewidth=3)
# plt.draw()
# plt.plot(t[int(0.51 * 2302) - 1:int(1 * 2302)], data[int(0.51 * 2302) - 1:int(1 * 2302)], label='With Human Coupling Effect', linewidth=3)
plt.plot(t, filtered_data, label='Filtered Signal', linewidth=3, color='#ff7f0e')
plt.yticks([0.8, 1.3, 1.8], fontsize=40, weight=10)
plt.xticks([0, 2, 4, 6 ,8 ,10], fontsize=40, weight=10)
plt.ylabel('Voltage (V)', fontsize=40)
plt.xlabel('Time (s)', fontsize=40)
# plt.legend(fontsize=25, loc='upper right')
plt.ylim([0.6, 2.0])
plt.xlim([0,10])
plt.tight_layout()

# plt.subplot(1, 2, 2)
# plt.plot(t, filtered_data, label='Filtered Signal', linewidth=2, color='#ff7f0e')
# plt.plot(t, upper, label='Envelope Signal', linewidth=3, color='#2ca02c')
# plt.yticks([1], fontsize=25, weight=10)
# plt.xticks([3, 4, 5], fontsize=25, weight=10)
# plt.ylabel('Voltage (V)', fontsize=30)
# plt.xlabel('Time (s)', fontsize=30)
# plt.legend(fontsize=25, loc='upper right')
# plt.ylim([0.9, 1.7])
# plt.xlim([3, 5])
# plt.tight_layout()


plt.show()