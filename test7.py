import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
from utils.envelope_process import envelope
from utils.filter import iir_design_filter

config = {
    "font.family": 'Times New Roman',
}
rcParams.update(config)

def process_data(data):
    data = data  * 5 / 1024
    F = iir_design_filter() # f_pass=40.0, f_stop=48.0, a_pass=1.0, a_stop=80.0
    filtered_data = F.filter_(raw_data=data)
    return filtered_data

def STFT(x, fs, n):
    f, t, amp = signal.stft(x, fs, nperseg=n)
    z = np.abs(amp.copy())
    return f, t, z


if __name__ == '__main__':
    x = np.loadtxt('raw_data/five_rhythm/true/five_1.csv', delimiter=',')
    fs = 2302
    time = 30
    t = np.linspace(0, time - 1/fs, int(time * fs))
    # fre, ts, amp = STFT(x, fs, 128)
    # print(fre)

    plt.figure(figsize=(9, 7))

    # plt.subplot(1, 2, 1)
    # plt.pcolormesh(ts, fre, amp)
    # plt.ylim(0,200)
    # plt.xticks(fontsize=25, weight=10)
    # plt.yticks(fontsize=25, weight=10)
    # plt.ylabel('Frequency (Hz)', fontsize=25)
    # plt.xlabel('Time (s)', fontsize=25)
    # cb = plt.colorbar()
    # cb.ax.tick_params(labelsize=20)
    # plt.tight_layout()

    processed_x = process_data(x)
    # plt.subplot(1, 2, 2)
    p_fre, p_ts, p_amp = STFT(processed_x, fs, 128)
    print(p_amp.shape, p_amp)
    plt.pcolormesh(p_ts, p_fre, p_amp)
    plt.ylim(0,200)
    plt.xticks(fontsize=25, weight=10)
    plt.yticks(fontsize=25, weight=10)
    plt.ylabel('Frequency (Hz)', fontsize=25)
    plt.xlabel('Time (s)', fontsize=25)
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=20)
    plt.tight_layout()

    plt.show()
