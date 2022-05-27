#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/19 20:52
# @Author  : Yiu
# @Site    : https://github.com/dominique-yiu
# @File    : Link_Watch.py
# @Software: PyCharm

import bluetooth
import os
from pprint import pprint
import sys
from threading import Thread
import serial
from modify_features import *
from envelope_process import envelope
from classifier import one_class_svm
import numpy as np
from variance import window_var
from patternmatch import pattern_match
from adc_collect import collect_data
import time
import matlab.engine
eng = matlab.engine.start_matlab()

def get_features(collector: collect_data):
    while True:
        filtered_data = collector.start(m_time=13)
        upper, _ = envelope(filtered_data, 100).start()
        upper = upper[int(2302 * 1):-int(2302 * 0.5)]
        upper = upper.reshape(-1)
        upper = matlab.double(initializer=list(upper), size=(1, len(upper)), is_complex=False)
        upper = eng.smoothdata(upper, 'gaussian', 400, nargout=1)
        upper = upper[0]
        var_upper = np.array(upper).astype(float)
        rhythm_number = collector.get_rhythm_number(enveloped_data=var_upper)
        end_points, _ = window_var(data=var_upper, head=rhythm_number).start()
        end_points = np.sort(end_points)
        end_points = end_points[1::2]
        start_points, _, _, _ = eng.patterMatch(upper, rhythm_number, nargout=4)
        start_points = np.array(start_points[0])
        features = np.append(end_points, start_points)
        features = np.sort(features) - features.min()
        if len(features) == rhythm_number * 2:
            break
        else:
            collector.ser.write('F'.decode())
            print('重新输入.')
            time.sleep(3)

    return features

# Find devices with bluetooth opening nearby
def print_devices():
    print("Performing inquiry...")
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True,
                                                flush_cache=True, lookup_class=False)
    print("Found {} devices".format(len(nearby_devices)))
    for addr, name in nearby_devices:
        try:
            print("   {} - {}".format(addr, name))
        except UnicodeEncodeError:
            print("   {} - {}".format(addr, name.encode("utf-8", "replace")))

# # Listen port thread
# class send_data(Thread):
#     def __init__(self, socket):
#         super(send_data, self).__init__()
#         self.sock = socket
    
#     def run(self):
#         print("Connected. Type something...\n")
#         while True:
#             data = input()
#             if not data:
#                 break
#             self.sock.send(data)
#             print("Send successfully.")
#         self.sock.close()


# # Recieve Data thread
# class recieve_data(Thread):
#     def __init__(self, socket):
#         super(recieve_data, self).__init__()
#         self.sock = socket
    
#     def run(self):
#         while True:
#             data = self.sock.recv(1024).decode()
#             if not data:
#                 break
#             print(data)
#         self.sock.close()

class recieve_data(Thread):
    def __init__(self, collector: collect_data):
        super(recieve_data, self).__init__()
        self.collector = collector
        self.clf = one_class_svm()
        if not self.collector.ser.isOpen():
            self.collector.ser.open()
    
    def run(self):
        while True:
            raw_data = self.collector.ser.readline()
            if not raw_data:
                break
            data = raw_data.decode()[:-1]
            #   注册消息
            if data == 'S':
                #   测量环境噪声
                self.collector.get_env_intensity()
                self.collector.ser.write('d'.encode())

                gross_data = []
                for _ in range(measure_cnt):
                    features = get_features(self.collector)
                    self.collector.ser.write('T'.encode())
                    gross_data.append(features)
                gross_data = np.array(gross_data)
                add_modify(add_data=gross_data, add_name=self.name)

                self.collector.ser.write('W'.encode())
                self.clf.train_()
            #   登录消息
            elif data == 'L':
                #   测量环境噪声
                self.collector.get_env_intensity()
                self.collector.ser.write('e'.encode())

                features = get_features(self.collector)
                yes_or_no = self.clf.predict_(uncertified_person=features)
                if yes_or_no:
                    self.collector.ser.write('Y'.encode())
                else:
                    self.collector.ser.write('N'.encode())
            # print(data)
        self.collector.ser.close()



if __name__=='__main__':
    print_devices()

    addr = input('输入设备蓝牙地址：')
    service_matches = bluetooth.find_service(address=addr)
    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]
    print("Connecting to \"{}\" on {}, {}".format(name.decode(), host, port))
    # socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    # socket.connect((host, port))
    # socket.close()

    collector = collect_data(port='COM7',rate=115200, m_time=10)


    thread_1 = recieve_data(collector=collector)
    thread_1.start()
