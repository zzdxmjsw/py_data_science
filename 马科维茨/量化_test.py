import numpy as np
import time
import random
import numba
# 生成测试用的数据
data = []
data_length = 100000    # 总数据量
ma_length = 500         # 移动均线的窗口
test_times = 100        # 测试次数
for i in range(data_length):
    data.append(random.randint(1, 100))


def ma_numpy_wrong(data, ma_length):
    ma = []
    data_window = data[:ma_length]
    test_data = data[ma_length:]

    for new_tick in test_data:
        data_window.pop(0)
        data_window.append(new_tick)

        # 使用numpy求均线，注意这里本质上每次循环
        # 都在创建一个新的numpy数组对象，开销很大
        data_array = np.array(data_window)
        ma.append(data_array.mean())

    return ma


# @numba.jit
def ma_online_numba(data, ma_length):
    ma = []
    data_window = data[:ma_length]
    test_data = data[ma_length:]

    sum_buffer = 0

    for new_tick in test_data:
        old_tick = data_window.pop(0)
        data_window.append(new_tick)

        if not sum_buffer:
            sum_tick = 0
            for tick in data_window:
                sum_tick += tick
            ma.append(sum_tick/ma_length)
            sum_buffer = sum_tick
        else:
            sum_buffer = sum_buffer - old_tick + new_tick
            ma.append(sum_buffer/ma_length)

    return ma


start = time.time()
for i in range(test_times):
    result = ma_online_numba(data, ma_length)


time_per_test = (time.time()-start)/test_times
time_per_point = time_per_test/(data_length - ma_length)

print('单次耗时：%s秒' % time_per_test)
print('单个数据点耗时：%s微秒' % (time_per_point*1000000))
print('最后10个移动平均值：', result[-10:])
