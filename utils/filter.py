#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/5 22:46
# @Author  : Yiu
# @Site    :
# @File    : filter.py
# @Software: PyCharm
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


class iir_design_filter:
    def __init__(self, sample_rate=2302, f_pass=10.0, f_stop=100.0, a_pass=1.0, a_stop=100.0):
        self.sample_rate = sample_rate
        self.f_pass = f_pass
        self.f_stop = f_stop
        self.a_pass = a_pass
        self.a_stop = a_stop

        self.raw_data = None
        self.filtered_data = None
        self.length = None

    def filter_(self, env_data=None, raw_data=None, load_path=None, save_path=None):

        b, a = signal.iirdesign(wp=self.f_pass, ws=self.f_stop, gpass=self.a_pass, gstop=self.a_stop, analog=False,
                                ftype='ellip',
                                output='ba', fs=self.sample_rate)

        if env_data is None:
            if load_path is not None:
                self.raw_data = np.loadtxt(load_path, delimiter=',')
            else:
                self.raw_data = raw_data
            self.length = len(self.raw_data)
            self.filtered_data = signal.filtfilt(b, a, self.raw_data)
            if save_path is not None:
                np.savetxt(fname=save_path, X=self.filtered_data)
        else:
            return signal.filtfilt(b, a, env_data)

        return self.filtered_data

    def plot_(self):
        t = np.linspace(0, 1, self.length)
        plt.figure(figsize=(16, 9))
        plt.plot(t, self.raw_data, label='Raw Data')
        plt.plot(t, self.filtered_data, label='Filtered Data')
        plt.legend(loc='upper left')
        plt.grid()
        plt.show()

if __name__=='__main__':
    L_path = 'raw_data/three_rhythm/LXY_01.csv'
    S_path = 'filtered_.csv'
    _filter = iir_design_filter()
    filtered_data = _filter.filter_(load_path=L_path, save_path=S_path)
    filtered_data = filtered_data * 5 / 1024
    # _filter.plot_()
    sampled_filterd_data = filtered_data[::50]
    plt.figure(figsize=(16, 8))

    plt.subplot(2, 1, 1)
    plt.plot(filtered_data, label='原始数据')
    plt.xlabel("样本个数", fontsize=25)
    plt.ylabel("电压/V", fontsize=25)
    plt.tick_params(labelsize=25) 
    plt.legend(fontsize=25, loc='upper right')
    plt.tight_layout()

    plt.subplot(2, 1, 2)
    plt.plot(sampled_filterd_data, label='重采样数据')
    plt.xlabel("样本个数", fontsize=25)
    plt.ylabel("电压/V", fontsize=25)
    plt.tick_params(labelsize=25) 
    plt.legend(fontsize=25, loc='upper right')
    plt.tight_layout()
    plt.show()
