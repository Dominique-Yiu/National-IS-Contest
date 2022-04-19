#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/12 20:00
# @Author  : Yiu
# @Site    : 
# @File    : adc_collect.py
# @Software: PyCharm
import csv
import time
import numpy as np
import serial
from filter import iir_design_filter


class collect_data:
    def __init__(self, port='COM3', rate=115200, m_time=20, load_path=None, save_path=None):
        self.serial_port = port
        self.serial_rate = rate
        self.measuring_time = m_time * 2302
        self.ser = serial.Serial(self.serial_port, self.serial_rate, timeout=5)
        self.filter = iir_design_filter(load_path, save_path)

    def get_env_intensity(self, m_time=10):
        print('Please guarantee your environment in  a stable status. Waiting......')
        time.sleep(1)

        for i in range(3):
            print(f"\r{3 - i} seconds later, start collecting.", end="")
            time.sleep(1)
        print('\nStart collecting average intensity of environment magnetic field.', end="")
        average_series_length = m_time * 2302
        average_series = np.zeros(average_series_length)
        for i in range(average_series_length):
            try:
                average_series[i] = self.ser.readline()
            except:
                pass
        self.ser.close()

        average_series = self.filter.filter_(average_series)
        print('Calculate Complete.')
        return average_series.mean()

    def start(self):
        self.ser.open()
        print('Please guarantee your environment in  a stable status. Waiting......')
        time.sleep(1)

        for i in range(3):
            print(f"\r{3 - i} seconds later, start collecting.", end="")
            time.sleep(1)
        print('\nStart collecting average intensity of environment magnetic field.', end="")

        string_a = np.zeros(shape=self.measuring_time)
        string_a_list = []

        print("start collecting!")
        for i in range(0, self.measuring_time):
            try:
                string_a[i] = self.ser.readline()
            except:
                pass
        with open(r"./ycw/ycw_1.csv", 'w', newline='') as t:
            writer = csv.writer(t, lineterminator='\n')
            for item in string_a:
                string_a_list.append(int(item))
            writer.writerows([string_a_list])
        t.close()
        time.sleep(0.2)
        string_a = np.zeros(shape=self.measuring_time)
        print('Collect Complete!')
        self.ser.close()

        self.filter.filter_()
