import matlab.engine
import matplotlib.pyplot as plt
import numpy as np

eng = matlab.engine.start_matlab()
ev_data = np.loadtxt('envelope_data_3.csv')
ev_data = matlab.double(initializer=list(ev_data), size=(1, len(ev_data)), is_complex=False)
# new_start, data_time, data_seg = eng.patterMatch(ev_data, 3, nargout=3)
# y = np.array(new_start[0])
# print(y)

# print(np.squeeze(np.array(new_start)))



C = eng.smoothdata(ev_data, 'gaussian', 400, nargout=1)
plt.plot(C[0])
plt.show()




# eng.eval("ev_data = csvread('envelope_data_3.csv');", nargout=0)
# eng.eval("time = 1/2302:1/2302:length(ev_data)/2302;", nargout=0)
# eng.eval("C = smoothdata(ev_data, 'gaussian', 400);", nargout=0)
# D = eng.workspace["C"]
# plt.plot(D)
# plt.show()

