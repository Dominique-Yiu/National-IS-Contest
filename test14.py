import datetime
import time
import psutil
p = psutil.Process()
cpu_lst = p.cpu_affinity()
print("cpu列表", cpu_lst)
# 将当前进程绑定到cpu0上运行，列表中也可以写多个cpu
p.cpu_affinity([0,1,2,3,4,5,6,7])
while True:
    start = time.perf_counter()
    while (time.perf_counter() - start) * 1000  < 100000:
        pass
    time.sleep(0.001)