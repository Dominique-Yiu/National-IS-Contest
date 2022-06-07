#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/21 8:39
# @Author  : Yiu
# @Site    : https://github.com/dominique-yiu
# @File    : envelope_process.py
# @Software: PyCharm

import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


class envelope:
    def __init__(self, raw_data, n=100):
        self.raw_data = raw_data
        self.n = n

        # pre-allocate space for results
        self.raw_data = self.raw_data.reshape(-1, 1)
        self.nx = self.raw_data.shape[0]

        self.y_upper = np.zeros(self.raw_data.shape, dtype=type(self.raw_data))
        self.y_lower = np.zeros(self.raw_data.shape, dtype=type(self.raw_data))

    def start(self):
        # handle default case where not enough input is given
        if self.nx < 2:
            self.y_upper = self.raw_data
            self.y_lower = self.raw_data
            print('The number of input is not enough that is less than 2.')
            return self.y_upper, self.y_lower

        # compute upper envelope
        for idx in range(self.raw_data.shape[1]):
            if self.nx > self.n + 1:
                # find local maxima separated by at least N samples
                iPk, _ = find_peaks(np.squeeze(np.array(self.raw_data[:, idx], dtype=np.float64)), distance=self.n)
            else:
                iPk = np.array([])

            if len(iPk) < 2:
                # include the first and last points
                iLocs = np.append(np.append(0, iPk), self.nx - 1)
            else:
                iLocs = iPk

            f = interp1d(iLocs, self.raw_data[iLocs, idx], kind='cubic', fill_value="extrapolate")
            x_new = np.linspace(0, self.nx, self.nx, endpoint=False)
            self.y_upper[:, idx] = f(x_new)

        # compute the lower envelope
        for idx in range(self.raw_data.shape[1]):
            if self.nx > self.n + 1:
                # find local maxima separated by at least N samples
                iPk, _ = find_peaks(-np.squeeze(np.array(self.raw_data[:, idx], dtype=np.float64)), distance=self.n)
            else:
                iPk = np.array([])

            if len(iPk) < 2:
                # include the first and last points
                iLocs = np.append(np.append(0, iPk), self.nx - 1)
            else:
                iLocs = iPk

            f = interp1d(iLocs, self.raw_data[iLocs, idx], kind='cubic', fill_value="extrapolate")
            x_new_ = np.linspace(0, self.nx, self.nx, endpoint=False)
            self.y_lower[:, idx] = f(x_new_)

        return self.y_upper, self.y_lower

if __name__=='__main__':
    data = np.loadtxt('random_data.csv', delimiter=',').reshape(1, -1)
    nx = data.shape[1]
    x = np.linspace(0, nx, nx, endpoint=False)
    env = envelope(data, 100)
    upper, lower = env.start()
    plt.plot(x, np.squeeze(data))
    plt.plot(x, upper)
    plt.grid()
    plt.show()
    np.savetxt('./envelope_data_3.csv', upper)
