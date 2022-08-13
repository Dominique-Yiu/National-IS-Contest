import numpy as np
arr1 = []
arr2 = []
# for idx in range(5):
#     rhythm = np.random.randint(5, 11)
#     person_1 = sorted(20 * np.random.random(2 * rhythm - 1))
#     person_2 = person_1 + np.random.random(2 * rhythm - 1) / 2
#     person_1 = np.append(0, person_1).reshape(1, -1)
#     person_2= np.append(0, person_2).reshape(1, -1)
    
#     arr1.append(person_1)
#     arr2.append(person_2)
arr1.append(np.loadtxt('raw_data/three_rhythm/LXY_01_smooth.csv'))
arr2.append(np.loadtxt('raw_data/three_rhythm/LXY_02_smooth.csv'))
arr1.append(np.loadtxt('raw_data/four_rhythm/true/four_1_smooth.csv'))
arr2.append(np.loadtxt('raw_data/four_rhythm/true/four_2_smooth.csv'))
arr1.append(np.loadtxt('raw_data/five_rhythm/true/five_1_smooth.csv'))
arr2.append(np.loadtxt('raw_data/five_rhythm/true/five_2_smooth.csv'))
arr1.append(np.loadtxt('raw_data/six_rhythm/ms_sixtrue_data1_smooth.csv'))
arr2.append(np.loadtxt('raw_data/six_rhythm/ms_sixtrue_data2_smooth.csv'))
arr1.append(np.loadtxt('raw_data/two_rhythm/true/two_3_smooth.csv'))
arr2.append(np.loadtxt('raw_data/two_rhythm/true/two_4_smooth.csv'))

from tslearn.metrics import dtw, soft_dtw
classes = ['1', '2', '3', '4', '5']
metrix = np.zeros([5, 5])
for i in range(5):
    for j in range(5):
        # print(arr1[i], arr2[j])
        metrix[4 - i][j] = dtw(arr1[i], arr2[j])
max_value = int(np.max(np.max(metrix, axis=0), axis=0))
min_value = int(np.min(np.min(metrix, axis=0), axis=0))
np.clip(metrix, a_min=min_value, a_max=max_value, out=metrix)
# metrix = 1 / metrix
np.savetxt('metrix.csv', metrix)

# print(max_value)
import matplotlib.pyplot as plt
from matplotlib import rcParams
# plt.matshow(metrix, cmap=plt.get_cmap('Greens'), alpha=0.5)  # , alpha=0.3
# for i in range(10):
#     for j in range(10):
#         plt.text(i, j, format(metrix[i][j], '.2f'), va='center', ha='center')
# plt.show()
config = {
    "font.family": 'Times New Roman',  # 设置字体类型
}
rcParams.update(config)
plt.figure(figsize=(3 * 2.7, 2 * 2.7))
plt.imshow(metrix, interpolation='nearest', cmap=plt.cm.Blues_r, vmin=min_value, vmax=max_value / 2, aspect="auto")  # 按照像素显示出矩阵
# (改变颜色：'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds','YlOrBr', 'YlOrRd',
# 'OrRd', 'PuRd', 'RdPu', 'BuPu','GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn')
# plt.title('DTW Similarity ($\mathdefault{\\frac{1}{DTW_{Dist}(U_i, U_j)}}$) Matrix', fontsize=25, weight=10)
# plt.colorbar()
tick_marks = np.arange(len(classes))
xtick_marks = ['U1', 'U2', 'U3', 'U4', 'U5']
# ytick_marks = reversed(['U0\'','U1\'', 'U2\'', 'U3\'', 'U4\'', 'U5\'', 'U6\'', 'U7\'', 'U8\'', 'U9\''])
ytick_marks = reversed(xtick_marks)
plt.xticks(tick_marks, xtick_marks, fontsize=30, weight=10)
plt.yticks(tick_marks, ytick_marks, fontsize=30, weight=10)
for i in range(5):
    for j in range(5):
        if (i == 4 - j):
            plt.text(j, i, format(metrix[i][j], '.2f'), va='center', ha='center', fontsize=30, color='white', weight=10)
        else:
            plt.text(j, i, format(metrix[i][j], '.2f'), va='center', ha='center', fontsize=30, weight=10)
# plt.xlabel('First Sample of Users', fontsize=30)
# plt.ylabel('Second Sample of Users', fontsize=30)
plt.tight_layout()
plt.show()
