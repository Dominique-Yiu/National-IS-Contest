import matlab.engine
import matplotlib.pyplot as plt
import numpy as np

eng = matlab.engine.start_matlab()
ev_data = np.loadtxt('./output_data/smooth_data_LXY_20.csv')
# plt.plot(ev_data)
# plt.show()
ev_data = matlab.double(initializer=list(ev_data), size=(1, len(ev_data)), is_complex=False)
smoothData = eng.smoothdata(ev_data, 'gaussian', 400, nargout=1)
# plt.plot(smoothData[0])
# plt.show()
new_start, data_time, data_seg, time = eng.patterMatch(smoothData, 3, nargout=4)
print(new_start)
def show(raw_time, raw_data,  start_time, start_seg):
    plt.figure(figsize=(16, 9))
    plt.plot(raw_time, raw_data)
    plt.draw()
    cnt = start_time.size[0]
    for idx in range(cnt):
        plt.plot(start_time[idx], start_seg[idx])
        plt.draw()
    plt.show()
print(data_time.size)
show(raw_time=time[0], raw_data=smoothData[0], start_time=data_time, start_seg=data_seg)



# eng.eval("ev_data = csvread('envelope_data_3.csv');", nargout=0)
# eng.eval("time = 1/2302:1/2302:length(ev_data)/2302;", nargout=0)
# eng.eval("C = smoothdata(ev_data, 'gaussian', 400);", nargout=0)
# D = eng.workspace["C"]
# plt.plot(D)
# plt.show()

