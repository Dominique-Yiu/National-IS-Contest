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
    def __init__(self, port='COM3', rate=115200, m_time=20):
        self.env_intensity = None
        self.serial_port = port
        self.serial_rate = rate
        self.measuring_time = m_time * 2302
        self.ser = serial.Serial(self.serial_port, self.serial_rate, timeout=5)
        self.filter = iir_design_filter()
        self.ser.close()

    '''get environment's intensity'''

    def get_env_intensity(self, m_time=10):
        if not self.ser.isOpen():
            self.ser.open()
        print('Please guarantee your environment in  a stable status. Waiting......')
        time.sleep(1)

        for i in range(3):
            print(f"\r{3 - i} seconds later, start collecting.", end="")
            time.sleep(1)
        print('\nStart collecting average intensity of environment magnetic field.')
        average_series_length = m_time * 2302
        average_series = np.zeros(average_series_length)
        for i in range(average_series_length):
            try:
                average_series[i] = self.ser.readline()
            except:
                pass
        # self.ser.close()

        average_series = self.filter.filter_(env_data=average_series)
        result = average_series.mean()
        self.env_intensity = result
        print('Calculate Complete.', f'the average intensity is {result}')

    def get_rhythm_number(self, enveloped_data):
        env_threshold = self.env_intensity * 0.75
        last_status = False
        status = last_status
        rhythm_number = 0

        for item in enveloped_data:
            if item < env_threshold:
                last_status = status
                status = True
                if not last_status:
                    rhythm_number += 1
            else:
                last_status = status
                status = False
        return rhythm_number

    def start(self, load_path=None, save_path=None, m_time=10):
        self.measuring_time = m_time * 2302
        if not self.ser.isOpen():
            self.ser.open()
        print('Please guarantee your environment in  a stable status. Waiting......')
        time.sleep(1)

        for i in range(3):
            print(f"\r{3 - i} seconds later, start collecting.", end="")
            time.sleep(1)
        print('\nStart collecting average intensity of environment magnetic field.', end="\n")

        string_a = np.zeros(shape=self.measuring_time)
        string_a_list = []

        print("start collecting!")
        for i in range(0, self.measuring_time):
            try:
                string_a[i] = self.ser.readline()
            except:
                pass
        if load_path is not None:
            with open(load_path, 'w', newline='') as t:
                writer = csv.writer(t, lineterminator='\n')
                for item in string_a:
                    string_a_list.append(int(item))
                writer.writerows([string_a_list])
            t.close()
        time.sleep(0.2)
        print('Collect Complete!')
        # self.ser.close()
        # return filtered data
        return self.filter.filter_(raw_data=string_a, load_path=load_path, save_path=save_path)

if __name__=='__main__':
    L_path = 'YCW4_20.csv'
    S_path = 'filtered_random_data.csv'
    adc = collect_data()
    adc.start(load_path=L_path, save_path=S_path, m_time=15)
    # adc.get_env_intensity()
    adc.filter.plot_()
