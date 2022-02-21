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

# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = 'COM6'
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 115200

# give an vector to store the incoming samples
max_length = 11520


def main():
    string_a = np.zeros(shape=max_length)
    string_a_list = []

    ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)
    time.sleep(3)

    for i in range(0, max_length):
        try:
            string_a[i] = ser.readline()
        except:
            pass
    with open(r"./random_1.csv", 'w', newline='') as t:
        writer = csv.writer(t, lineterminator='\n')
        for item in string_a:
            string_a_list.append(int(item))
        writer.writerows([string_a_list])
    t.close()
    time.sleep(0.2)
    string_a = np.zeros(shape=max_length)


if __name__ == "__main__":
    main()
