import matlab.engine
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils.classifier import one_class_svm
from utils.filter import iir_design_filter
from utils.envelope_process import envelope
from utils.variance import window_var
from utils.modify_features import *
import os
import copy
import time
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def show(raw_time, raw_data,  start_time, start_seg):
    plt.figure(figsize=(16, 9))
    plt.plot(raw_time, raw_data)
    plt.draw()
    cnt = start_time.size[0]
    for idx in range(cnt):
        plt.plot(start_time[idx], start_seg[idx])
        plt.draw()
    plt.show()

root_1 = "raw_data/one_rhythm/true"
root_2 = "raw_data/two_rhythm/true"
root_3 = "raw_data/three_rhythm"
root_4 = "raw_data/four_rhythm/true"
root_5 = "raw_data/five_rhythm/true"
root_6 = "raw_data/six_rhythm"


eng = matlab.engine.start_matlab()



def extract_feature(root, num, indent='', head=None, rhythm_number=None, output_file=None):
    all_features = []
    for idx in range(num):
        if (idx + 1) < 10:
            end = indent + str(idx + 1)
        else:
            end = str(idx + 1)
        path = root + "/" + head + end + ".csv"
        data = np.loadtxt(path, delimiter=",")
        filter_module = iir_design_filter(f_pass=40.0, f_stop=48.0, a_pass=1.0, a_stop=80.0)
        filtered_data = filter_module.filter_(raw_data=data)
        # filter_module.plot_()
        upper, _ = envelope(filtered_data, 100).start()
        upper = upper[int(2302 * 1.25):-int(2302 * 0.5)]
        upper = upper.reshape(-1)
        upper = matlab.double(initializer=list(upper), size=(1, len(upper)), is_complex=False)
        upper = eng.smoothdata(upper, 'gaussian', 10, nargout=1)
        upper = upper[0]
        np.savetxt(root + "/" + head + end + "_smooth.csv", upper[::50])
        var_upper = np.array(upper).astype(float)
    
        win = window_var(data=var_upper, head=rhythm_number, window=10)
        end_points, _ = win.start(distance=800)
        # win.plot_()
        end_points = np.sort(end_points)
        end_points = end_points[1::2]
        start_points, data_time, data_seg, _time = eng.patterMatch(upper, rhythm_number, False, nargout=4)
        # show(raw_time=_time[0], raw_data=upper,  start_time=data_time, start_seg=data_seg)
        if not isinstance(start_points, (float)):
            start_points = np.array(start_points[0])
        features = np.append(end_points, start_points)
        features = np.sort(features) - features.min()
        if len(features) == rhythm_number * 2:
            all_features.append(features.tolist())
    np.savetxt(output_file, all_features)

# extract_feature(root=root_1, num=55, head='one_', rhythm_number=1, output_file='data/one_raw.csv')
# extract_feature(root=root_2, num=55, head='two_', rhythm_number=2, output_file='data/two_raw.csv')
# extract_feature(root=root_3, num=55, head='LXY_', indent='0', rhythm_number=3, output_file='data/three_raw.csv')
# extract_feature(root=root_4, num=60, head='four_', rhythm_number=4, output_file='data/four_raw.csv')
# extract_feature(root=root_5, num=55, head='five_', rhythm_number=5, output_file='data/five_raw.csv')
# extract_feature(root=root_6, num=55, head='ms_sixtrue_data', rhythm_number=6, output_file='data/six_raw.csv')


from tslearn.preprocessing import TimeSeriesScalerMinMax
from tslearn.barycenters import softdtw_barycenter
from tslearn.utils import to_time_series_dataset
from tslearn.metrics import dtw, soft_dtw
import numpy as np
from utils.softdtw import SoftDBA
from utils.modify_features import *
import random

def generate_argTrain_data(path, num=5, rhythm_number=None, root=None, head=None, indent='', save_path=None):
    legal_user = np.loadtxt(path)
    sample_index = []
    while True:
        if len(sample_index) >= num:
            break
        idx = np.random.randint(0, len(legal_user))
        if idx not in sample_index:
            sample_index.append(idx)

    train_data = legal_user[sample_index]
    #   数据增强样本进行训练
    gross = []
    for idx in sample_index:
        if (idx + 1) < 10:
            end = indent + str(idx + 1)
        else:
            end = str(idx + 1)
        path = root + "/" + head + end + "_smooth.csv"
        data = np.loadtxt(path, delimiter=",")
        gross.append(data)

    G = SoftDBA(raw_data=gross, generate_num=20)

    for idx, ts in enumerate(G.data):
        if idx == 0:
            plt.plot(ts.ravel(), "k-", label='原始数据', alpha=.2)
        else:
            plt.plot(ts.ravel(), "k-", alpha=.2)

    generated_data = G.run()

    for idx, bar in enumerate(generated_data):
        if idx == 0:
            plt.plot(bar.ravel(), "r-", label='合成数据', alpha=.5)
        else:
            plt.plot(bar.ravel(), "r-", alpha=.5)

    # plt.show()

    train_data = list(train_data)
    for upper in generated_data:
        upper = upper.reshape(-1)
        upper = matlab.double(initializer=list(upper), size=(1, len(upper)), is_complex=False)
        upper = upper[0]

        var_upper = np.array(upper).astype(float)
    
        win = window_var(data=var_upper, head=rhythm_number, window=5)
        end_points, _ = win.start(distance=20)
        end_points = np.sort(end_points)
        end_points = end_points[1::2]
        start_points, data_time, data_seg, _time = eng.patterMatch(upper, rhythm_number, True, nargout=4)
        if not isinstance(start_points, (float)):
            start_points = np.array(start_points[0])
        features = np.append(end_points, start_points)
        features = np.sort(features) * 50
        features = features - features.min()
        if len(features) == rhythm_number * 2:
            train_data.append(features)

    gross_data = np.array(train_data)
    np.savetxt(save_path, gross_data)

# generate_argTrain_data(path='data/one_raw.csv', num=8, rhythm_number=1, root=root_1, head='one_', save_path='data/one_arg.csv')
# generate_argTrain_data(path='data/two_raw.csv', num=8, rhythm_number=2, root=root_2, head='two_', save_path='data/two_arg.csv')
# generate_argTrain_data(path='data/three_raw.csv', num=8, rhythm_number=3, root=root_3, head='LXY_', indent='0', save_path='data/three_arg.csv')
# generate_argTrain_data(path='data/four_raw.csv',  num=8, rhythm_number=4, root=root_4, head='four_', save_path='data/four_arg.csv')
# generate_argTrain_data(path='data/five_raw.csv', num=8, rhythm_number=5, root=root_5, head='five_', save_path='data/five_arg.csv')



arg_list = ['data/one_arg.csv', 'data/two_arg.csv', 'data/three_arg.csv', 'data/four_arg.csv', 'data/five_arg.csv']
raw_list = ['data/one_raw.csv', 'data/two_raw.csv', 'data/three_raw.csv', 'data/four_raw.csv', 'data/five_raw.csv']
def show_result(idx):

    clf = one_class_svm(train_path=arg_list[idx])
    clf.train_()
    cnt = 0
    legal_user = np.loadtxt(raw_list[idx])
    for i in range(len(legal_user)):
        if clf.predict_(legal_user[i].reshape(1, -1)) == 1:
            cnt += 1
    print('合法用户测试准确率(数据增强): ', cnt / len(legal_user))

    cnt = 0
    SUM = 0
    for i in range(5):
        if i != idx:
            attacker = np.loadtxt(raw_list[i])
            SUM += len(attacker)
            for i in range(len(attacker)):
                if clf.predict_(attacker[i].reshape(1, -1)) == -1:
                    cnt += 1
    print('非法用户测试准确率(数据增强): ', cnt/SUM)

# show_result(0)
# show_result(1)
# show_result(2)
# show_result(3)
# show_result(4)

def show_legal_user_result(idx):

    clf = one_class_svm(train_path=arg_list[idx])
    clf.train_()
    cnt = 0
    legal_user = np.loadtxt(raw_list[idx])

    idx = [item for item in range(len(legal_user))]
    random.shuffle(idx)
    idx = idx[:30]
    sample_legal_user = legal_user[idx]
    reshaped_sample = [[item for item in sample_legal_user[i * 3:i * 3 + 3]]for i in range(10)]
    result = np.zeros((10, 3))
    for i in range(10):
        for j in range(3):
            result[i, j] = clf.predict_(reshaped_sample[i][j].reshape(1, -1))
    
    one_time = result[:, :1].reshape(-1, 1)
    two_time = result[:, :2].reshape(-1, 2)
    three_time = result[:, :3].reshape(-1, 3)

    cnt_1 = 0
    cnt_2 = 0
    cnt_3 = 0
    for i in range(10):
        if 1 in one_time[i]:
                cnt_1 += 1
        if 1 in two_time[i]:
                cnt_2 += 1
        if 1 in three_time[i]:
                cnt_3 += 1
    print(f'一次成功的概率{cnt_1 * 10}%')
    print(f'两次成功的概率{cnt_2 * 10}%')
    print(f'三次成功的概率{cnt_3 * 10}%')

# show_legal_user_result(0)
# show_legal_user_result(1)
# show_legal_user_result(2)
# show_legal_user_result(3)
# show_legal_user_result(4)

# %%
'''shouder attack'''
def shoulder_attack_result(train_path, test_path, distance):
    clf = one_class_svm(train_path=train_path)
    clf.train_()
    cnt = 0
    illegal_user = np.loadtxt(test_path)
    for i in range(len(illegal_user)):
        if clf.predict_(illegal_user[i].reshape(1, -1)) == 1:
            cnt += 1
    print(f'在{distance}m距离下, 肩窥攻击的成功率{100 * cnt / len(illegal_user)}%')

# extract_feature(root="raw_data/shoulder_attack", num=5, head='shoulder_true_', indent='0', rhythm_number=4, output_file='data/four_shoulder_true.csv')
# extract_feature(root="raw_data/shoulder_attack", num=5, head='shoulder1_true_', indent='0', rhythm_number=4, output_file='data/four_shoulder1_true.csv')
# extract_feature(root="raw_data/shoulder_attack", num=5, head='shoulder2_true_', indent='0', rhythm_number=4, output_file='data/four_shoulder2_true.csv')
# extract_feature(root="raw_data/shoulder_attack", num=4, head='shoulder4_true_', indent='0', rhythm_number=4, output_file='data/four_shoulder4_true.csv')

# extract_feature(root="raw_data/shoulder_attack", num=3, head='shoulder_false_', indent='0', rhythm_number=4, output_file='data/four_shoulder_false.csv')
# extract_feature(root="raw_data/shoulder_attack", num=3, head='shoulder1_false_', indent='0', rhythm_number=4, output_file='data/four_shoulder1_false.csv')
# extract_feature(root="raw_data/shoulder_attack", num=3, head='shoulder2_false_', indent='0', rhythm_number=4, output_file='data/four_shoulder2_false.csv')
# extract_feature(root="raw_data/shoulder_attack", num=3, head='shoulder4_false_', indent='0', rhythm_number=4, output_file='data/four_shoulder4_false.csv')

generate_argTrain_data(path='data/four_shoulder_true.csv', num=5, rhythm_number=4, root="raw_data/shoulder_attack", head='shoulder_true_', indent='0', save_path='data/four_shoulder_true_arg.csv')
generate_argTrain_data(path='data/four_shoulder1_true.csv', num=5, rhythm_number=4, root="raw_data/shoulder_attack", head='shoulder1_true_', indent='0', save_path='data/four_shoulder1_true_arg.csv')
generate_argTrain_data(path='data/four_shoulder2_true.csv', num=5, rhythm_number=4, root="raw_data/shoulder_attack", head='shoulder2_true_', indent='0', save_path='data/four_shoulder2_true_arg.csv')
generate_argTrain_data(path='data/four_shoulder4_true.csv', num=4, rhythm_number=4, root="raw_data/shoulder_attack", head='shoulder4_true_', indent='0', save_path='data/four_shoulder4_true_arg.csv')

shoulder_attack_result('data/four_shoulder_true_arg.csv', 'data/four_shoulder_false.csv', 0.5)
shoulder_attack_result('data/four_shoulder1_true_arg.csv', 'data/four_shoulder1_false.csv', 1)
shoulder_attack_result('data/four_shoulder2_true_arg.csv', 'data/four_shoulder2_false.csv', 2)
shoulder_attack_result('data/four_shoulder4_true_arg.csv', 'data/four_shoulder4_false.csv', 4)