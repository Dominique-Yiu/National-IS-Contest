#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/18 22:56
# @Author  : Yiu
# @Site    : https://github.com/dominique-yiu
# @File    : variance.py
# @Software: PyCharm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


class window_var:
    def __init__(self, path=None, data=None, head=12, window=10):
        self.load_path = path
        self.head = head * 2
        if path is None:
            self.data = data
        else:
            self.data = np.loadtxt(self.load_path)
        self.peaks = None
        self.biggest_peaks_index = None
        self.biggest_peaks = None
        self.peaks_index = None
        self.move_var = np.squeeze(pd.DataFrame(self.data).rolling(window=window).var().values)

    def start(self, distance=800):
        self.peaks_index = find_peaks(self.move_var, distance=distance)[0]
        self.peaks = self.move_var[self.peaks_index]
        self.biggest_peaks_index = np.argsort(self.peaks)[::-1][0:self.head]
        self.biggest_peaks = self.peaks[self.biggest_peaks_index]
        self.biggest_peaks_index = self.peaks_index[self.biggest_peaks_index]
        half = np.argsort(self.biggest_peaks_index)[1::2]
        self.end_points  = self.biggest_peaks[half]
        self.end_points_index  = self.biggest_peaks_index[half]

        return self.biggest_peaks_index, self.biggest_peaks

    def plot_(self):
        fig = plt.figure(figsize=(10, 8), dpi=80)
        ax = fig.add_subplot(111)
        lin1 = ax.plot(self.data)

        ax2 = ax.twinx()
        lin2 = ax2.plot(self.move_var, color='r')
        ax2.scatter(self.end_points_index, self.end_points, marker='+', color='g', s=200)

        lines = lin1 + lin2
        ax.legend(lines, ['envelope data', 'variance'])
        ax.grid()
        plt.show()


# var = window_var('envelope_data_3.csv', head=3)
# var.start()
# var.plot_()