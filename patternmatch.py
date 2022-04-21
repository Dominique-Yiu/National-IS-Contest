#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/19 0:40
# @Author  : Yiu
# @Site    : https://github.com/dominique-yiu
# @File    : patternmatch.py
# @Software: PyCharm
import numpy as np
import matplotlib.pyplot as plt
std_values = np.loadtxt('standard_value.csv', delimiter=',')[:-1]


def normalize(x, y, c):
    cxx = np.sum(np.abs(x) ** 2)
    cyy = np.sum(np.abs(y) ** 2)
    scale_coeff_cross = np.sqrt(cxx * cyy)
    return c / scale_coeff_cross


class pattern_match:
    def __init__(self, path):
        self.data = np.loadtxt(path, delimiter=',')
        self.length = len(self.data)
        self.start_point = []
        self.new_start = []
        self.data_seg = []
        self.data_time = []
        global std_values
        a1 = 15.93
        b1 = 5.726
        c1 = 0.0453
        a2 = 28.79
        b2 = 5.765
        c2 = 0.1749
        a3 = 56.32
        b3 = 5.804
        c3 = 0.3934
        a4 = 743
        b4 = 0.7234
        c4 = 6.066
        self.L = a1 * np.exp(-((std_values - b1) / c1) ** 2) + \
            a2 * np.exp(-((std_values - b2) / c2) ** 2) + \
            a3 * np.exp(-((std_values - b3) / c3) ** 2) + \
            a4 * np.exp(-((std_values - b4) / c4) ** 2)

    def start(self):
        x_coordinate = []
        y_coordinate = None
        c_gross = []
        for idx in range(0, self.length - 2500, 100):
            x_coordinate.append([item for item in range(idx, idx + 2500)])
            y_coordinate = self.data[x_coordinate[-1]]
            c = np.correlate(self.L, y_coordinate, 'full')
            c = normalize(self.L, y_coordinate, c)
            c_gross.append(c)

        c_gross = np.array(c_gross)
        max_value_axis_1 = np.max(c_gross, 1)

        sorted_max_index = np.argsort(max_value_axis_1)
        selected_index = sorted_max_index[-21:-1]

        for item in selected_index:
            self.start_point.append(x_coordinate[item][0])
        self.start_point = np.sort(self.start_point)

        avg = []
        start_point_avg = []
        for it in self.start_point:
            if len(avg) == 0 or np.abs(avg[-1] - it) < 500:
                avg.append(it)
            else:
                start_point_avg.append(round(np.mean(avg)))
                avg = [it]
        if len(avg) > 0:
            start_point_avg.append(round(np.mean(avg)))

        x_coordinate = []
        y_coordinate = []
        for it in start_point_avg:
            if it - 450 > 0:
                x_coordinate.append([item for item in range(it - 450, it + 50)])
            else:
                x_coordinate.append([0 for _ in range(500 - (it + 50))] +
                                    [item for item in range(it + 50)])
            y_coordinate.append(self.data[x_coordinate[-1]])

        min_index = np.argsort(y_coordinate, 1)[:, 0]
        modify_start_point_avg = []
        for idx, it in enumerate(min_index):
            modify_start_point_avg.append(x_coordinate[idx][it])
        # unique
        modify_start_point_avg = list(dict.fromkeys(modify_start_point_avg))

        avg = []
        for it in modify_start_point_avg:
            if len(avg) == 0 or np.abs(avg[-1] - it) < 500:
                avg.append(it)
            else:
                self.new_start.append(round(np.mean(avg)))
                avg = [it]
        if len(avg) > 0:
            self.new_start.append(round(np.mean(avg)))

        return self.new_start

    def plot_(self):
        plt.figure()
        plt.plot(self.data)
        for idx in self.new_start:
            self.data_time.append([item for item in range(idx, idx + 2500)])
            self.data_seg.append(self.data[self.data_time[-1]])
        for idx in range(len(self.data_seg)):
            plt.plot(self.data_time[idx], self.data_seg[idx])
        plt.show()


match = pattern_match('LXY_两快一慢/enveloped_data_01.csv')
match.start()
match.plot_()