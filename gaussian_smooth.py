# from scipy.ndimage.filters import gaussian_filter1d
# from scipy.ndimage.filters import gaussian_filter
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
data = pd.read_csv('envelope_data_3.csv')
#下面这行可删去，试运行1000个数据
# data=data.iloc[0:1000,]
from math import pi, sqrt, exp

#Define a function that generate gauss kernel
def gauss_kernal(n,sigma):#核函数的定义
    r = range(-int(n/2),int(n/2)+1)
    arr=np.array([1 / (sigma * sqrt(2*pi)) * exp(-float(x)**2/(2*sigma**2)) for x in r])
    return  arr/sum(arr)

def gauss_filter_my(window_size,sigma,data):
    kernel=gauss_kernal(window_size,sigma)
    kernel=kernel.reshape(window_size,1)
    blurred_data=np.zeros((len(data),1))
    #按照windowsize计算高斯核函数对数据加权
    for i in range(len(data)):
        cur_arr=np.zeros((window_size,1))
        for dist in range(window_size//2):
            if i-dist>=0:
                cur_arr[window_size//2-dist,0]=data[i-dist,0]
            else:
                cur_arr[window_size // 2 - dist, 0] = data[0, 0]
            if i+dist<len(data):
                cur_arr[window_size // 2 + dist,0] = data[i + dist,0]
            else:
                cur_arr[window_size // 2 - dist, 0] = data[-1, 0]
            #Otherwise it is filled up with 0
        cur_sum=sum(kernel*cur_arr)
        blurred_data[i,0]=cur_sum
    return blurred_data

origin=data.to_numpy()
# origin=origin/origin.max()
#下面这里第一个参数是window个数，第二个是sigma大小，这两个值越大越平滑,建议改动window即可
blurred_data = gauss_filter_my(1111,1000,origin)

plt.plot(origin,'k',color="red")
plt.show()
seconds=np.arange(0,len(blurred_data)/2302,1/2302)
plt.plot(seconds,blurred_data,'-',color="blue")
plt.show()
np.savetxt('new.csv',blurred_data , delimiter = ',')