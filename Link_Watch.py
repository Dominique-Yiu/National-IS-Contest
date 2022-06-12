#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/19 20:52
# @Author  : Yiu
# @Site    : https://github.com/dominique-yiu
# @File    : Link_Watch.py
# @Software: PyCharm

import bluetooth
from pprint import pprint
from threading import Thread
from utils.modify_features import *
from utils.envelope_process import envelope
from utils.classifier import one_class_svm
import numpy as np
from utils.variance import window_var
from utils.adc_collect import collect_data
import time
import matlab.engine
from utils.softdtw import SoftDBA
import matplotlib.pyplot as plt
eng = matlab.engine.start_matlab()

def get_features(collector: collect_data):
    while True:
        filtered_data = collector.start(m_time=13)  #   定义收集13秒的ADC数据
        upper, _ = envelope(filtered_data, 100).start() #   对数据进行包络，k=100
        upper = upper[int(2302 * 1):-int(2302 * 0.5)]   #   去除一些硬件原因的不稳定数据
        upper = upper.reshape(-1)
        upper = matlab.double(initializer=list(upper), size=(1, len(upper)), is_complex=False)  #   数据转换为matlab类型
        upper = eng.smoothdata(upper, 'gaussian', 400, nargout=1)   #   数据进行平滑处理
        upper = upper[0]
        var_upper = np.array(upper).astype(float)
        sample_data = var_upper[::50]
        rhythm_number = collector.get_rhythm_number(enveloped_data=var_upper)   #   获得节奏数
        # end_points, _ = window_var(data=var_upper, head=rhythm_number, window=10).start(distance=800)  #   最大值之间距离设置为800
        # end_points = np.sort(end_points)
        # end_points = end_points[1::2]
        # start_points, _, _, _ = eng.patterMatch(upper, rhythm_number, False, nargout=4)
        win = window_var(data=var_upper, head=rhythm_number, window=10)
        win.start(distance=800)
        features = win.all
        features = np.sort(features) - features.min()
        if len(features) == rhythm_number * 2:
            break
        else:
            collector.ser.write('F'.encode())
            print('重新输入.')
            time.sleep(3)

    return features, sample_data, rhythm_number

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
            if not self.collector.ser.isOpen():
                self.collector.ser.open()
            raw_data = self.collector.ser.readline()
            if not raw_data:
                break
            data = raw_data.decode()[:-2]
            print(data)
            #   注册消息
            if data == 'S':
                print(data)
                #   测量环境噪声
                self.collector.get_env_intensity()
                self.collector.ser.write('d'.encode())

                gross_data = []
                raw_data = []
                for _ in range(measure_cnt):
                    features, sample_data, rhythm_number = get_features(self.collector)
                    self.collector.ser.write('T'.encode())
                    gross_data.append(features)
                    raw_data.append(sample_data)

                G = SoftDBA(raw_data=raw_data, generate_num=10)
                generated_data = G.run()

                for upper in generated_data:
                    upper = upper.reshape(-1)
                    upper = matlab.double(initializer=list(upper), size=(1, len(upper)), is_complex=False)
                    upper = upper[0]
                    var_upper = np.array(upper).astype(float)
                    win = window_var(data=var_upper, head=rhythm_number, window=5)
                    win.start(distance=20)
                    features = win.all
                    features = np.sort(features) * 50
                    features = features - features.min()
                    if len(features) == rhythm_number * 2:
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
                yes_or_no = self.clf.predict_(uncertified_person=features.reshape(1, -1))
                if yes_or_no:
                    self.collector.ser.write('Y'.encode())
                else:
                    self.collector.ser.write('N'.encode())
            # print(data)
        self.collector.ser.close()



if __name__=='__main__':
    # print_devices()

    # addr = input('输入设备蓝牙地址：')
    # service_matches = bluetooth.find_service(address=addr)
    # first_match = service_matches[0]
    # port = first_match["port"]
    # name = first_match["name"]
    # host = first_match["host"]
    # print("Connecting to \"{}\" on {}, {}".format(name.decode(), host, port))
    # socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    # socket.connect((host, port))
    # socket.close()

    collector = collect_data(port='COM7',rate=115200, m_time=10)


    thread_1 = recieve_data(collector=collector)
    thread_1.start()
