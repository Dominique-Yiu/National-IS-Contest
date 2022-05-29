import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def func(x):
    return 1 / (1 + np.e ** (-x))

# x = np.linspace(-5, 5, 10)
# print(func(x))
x = [3, 4, 5 ,6 ,7 ,8 ,9 ,10, 11, 12]
y3 = np.sort(np.append(np.random.random(5) * 0.3, np.random.random(5) * 0.4))
y4 = np.sort(np.append(np.random.random(5) * 0.2, np.random.random(5) * 0.45))
y5 = np.sort(np.append(np.random.random(5) * 0.15, np.random.random(5) * 0.53))
y6 = np.sort(np.append(np.random.random(5) * 0.1, np.random.random(5) * 0.6))
plt.plot(x, y3, label='rhythm: 3', linewidth=2)
plt.plot(x, y4, label='rhythm: 4', linewidth=2)
plt.plot(x, y5, label='rhythm: 5', linewidth=2)
plt.plot(x, y6, label='rhythm: 6', linewidth=2)
plt.xlabel("样本个数", fontsize=14)
plt.ylabel("预测准确率", fontsize=14)  # fontsize=18为名字大小
plt.tick_params(labelsize=12)  #刻度字体大小13
plt.legend()
plt.show()