from time import time
from math import exp, sqrt, log
from random import gauss, seed
from scipy import stats


def bsm_call_value(s0, k, T, r, sigma):
    s0 = float(s0)
    d1 = (log(s0 / k) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = (log(s0 / k) + (r - 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    value = (s0 * stats.norm.cdf(d1, 0.0, 1.0) - k *
             exp(-r * T) * stats.norm.cdf(d2, 0.0, 1.0))
    return value


s0 = 100
k = 105
T = 1.0
r = 0.05
sigma = 0.2
M = 50  # 小区间个数
dt = T / M  # 微元区间
I = 250000  # 25w条路径

seed(20000)
t0 = time()
S = []
for i in range(I):
    path = []  # 空路径列表
    for t in range(M + 1):  # 原始价格s0和其他50个时间步
        if t == 0:  # 若为原始价格
            path.append(s0)  # 路径列表添加s0
        else:  # 否则
            z = gauss(0.0, 1.0)  # 按高斯分布的随机数
            # 今日价格等于上一日价格的欧拉离散
            st = path[t - 1] * exp((r - 0.5 * sigma**2)
                                   * dt + sigma * sqrt(dt) * z)
            path.append(st)  # 添加到路径中
    S.append(path)

c0 = exp(-r * T) * sum([max(path[-1] - k, 0) for path in S]) / I  # 蒙特卡洛模拟

tpy = time() - t0
print(tpy)
