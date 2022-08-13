import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
config = {
    "font.family": 'Times New Roman',
}
rcParams.update(config)
def add_modify(file_path='data/gross_name.csv', raw_path='data/gross_features.csv', data=None, add_data=None, add_name=None):
    name_list = np.loadtxt(file_path, dtype=str)
    if data is None:
        raw_data = np.loadtxt(raw_path)
    else:
        raw_data = data
    if raw_data.shape[0] == 0:
        result = add_data
    else:
        column = raw_data.shape[1] if raw_data.shape[1] > add_data.shape[1] else add_data.shape[1]
        result = np.zeros((raw_data.shape[0] + add_data.shape[0], column))
        result[0:raw_data.shape[0], 0:raw_data.shape[1]] = raw_data
        result[raw_data.shape[0]:, 0:add_data.shape[1]] = add_data
    if data is None and add_name is not None:
        name_list = np.append(name_list, add_name)
        np.savetxt(raw_path, result)
        np.savetxt(file_path, name_list, fmt='%s')
    elif data is None and add_name is None:
        np.savetxt(raw_path, result)
    else:
        return result
def normalize(arr):
    MAX = np.max(arr, axis=0)
    MIN = np.min(arr, axis=0)
    return (arr - int(MIN)) / (int(MAX) - int(MIN))

raw_data = None
for i in range(5):
    if i == 0:
        path = 'raw_data/four_rhythm/true/four_'
    elif i == 1:
        path = 'raw_data/five_rhythm/true/five_'
    elif i == 2:
        path = 'raw_data/one_rhythm/true/one_'
    elif i == 3:
        path = 'raw_data/six_rhythm/ms_sixtrue_data'
    elif i == 4:
        path = 'raw_data/three_rhythm/LXY_'
    for j in range(10):
        if i != 4:
            data = np.loadtxt(path + str(j + 1) + '.csv', delimiter=',').reshape(1, -1)
        else:
            data = np.loadtxt(path + str(j + 1).zfill(2) + '.csv', delimiter=',').reshape(1, -1)
        if raw_data is None:
            raw_data = data
        else:
            raw_data = np.concatenate([raw_data, data], axis=0)
label = np.zeros(10)
for i in range(1, 2):
    label = np.concatenate([label, np.zeros(10) + i], axis=0)

from sklearn.manifold import TSNE
tsne = TSNE(n_components=2, init='pca', random_state=0)
print(raw_data.shape)
X_tsne = tsne.fit_transform(raw_data)

color = ['black', 'lightcoral', 'peru', 'orange', 'gold', 'green', 'teal', 'skyblue', 'slategray', 'orchid']
mark = ['+', '2', 'p', 'X', 'o', 'H', '*', 'h', '1', '8']
def plot_embedding(X, y, title=None):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    plt.figure(figsize=(8, 7))
    plt.grid()
    for i in range(X.shape[0]):
        if i % 10 == 0:
            plt.scatter(X[i, 0], X[i, 1], color=color[int(y[i])], marker=mark[int(y[i])], s=100, label=f'User {int(y[i] + 1)}')
        else:
            plt.scatter(X[i, 0], X[i, 1], color=color[int(y[i])], marker=mark[int(y[i])], s=100)
    # plt.scatter(X[:, 0], X[:, 1])
    tick_marks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    plt.xticks(tick_marks, fontsize=20, weight=10)
    plt.yticks(tick_marks, fontsize=20, weight=10)
    plt.legend(fontsize=20, ncol = 2)
    plt.tight_layout()
    
     

plot_embedding(X_tsne, label)
plt.show()