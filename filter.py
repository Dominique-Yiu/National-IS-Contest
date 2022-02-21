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
import matplotlib.ticker
import csv


def data_loader(PATH):
    data = []
    with open(PATH, 'r') as f:
        line = csv.reader(f)
        for item in line:
            data = [int(x) for x in item]
        data = np.array(data)
    return data


def iir_design_filter(path: str, sample_rate: int, f_pass: float, f_stop: float, a_pass: float, a_stop: float) -> None:
    # load data
    data = data_loader(path)

    N = len(data)
    t = np.linspace(0, 1, N)

    # show the raw data picture
    plt.figure(figsize=(16, 9))
    plt.plot(t, data, label='Raw Data')

    # design the filter
    b, a = signal.iirdesign(wp=f_pass, ws=f_stop, gpass=a_pass, gstop=a_stop, analog=False, ftype='ellip', output='ba', fs=sample_rate)
    filtered = signal.lfilter(b, a, data)
    filtered = np.array(filtered, dtype=int)

    # save the filtered data
    save_path = 'filtered_' + path[2:]
    with open(save_path, 'w', newline='') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows([filtered])
    file.close()

    # show the filtered data
    plt.plot(t, filtered, label='Filtered Data')
    plt.legend(loc='upper left')
    plt.savefig('./picture.jpg')
    plt.show()


if __name__ == "__main__":
    iir_design_filter('./random_1.csv', 2800, 40.0, 48.0, 1.0, 80.0)
    iir_design_filter('./operator_1.csv', 2800, 40.0, 48.0, 1.0, 80.0)
    iir_design_filter('./operator_2.csv', 2800, 40.0, 48.0, 1.0, 80.0)
    iir_design_filter('./operator_3.csv', 2800, 40.0, 48.0, 1.0, 80.0)
    iir_design_filter('./operator_4.csv', 2800, 40.0, 48.0, 1.0, 80.0)