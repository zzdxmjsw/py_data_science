import pandas as pd
import json
import matplotlib
import scipy as sc
import numpy as np
# import statsmodels.api as sm
import scipy.stats as scs
import matplotlib.pyplot as plt
import tushare as ts
import scipy.optimize as sco
from numba import jit,cuda
import time
# import minpy



def get_lager_one(df_a, df_b):
    if len(df_a) > len(df_b):
        return 'left'
    else:
        return 'right'


# f = open('code_name.json', encoding='utf-8')
# text = f.read()
# d = json.loads(text)


stock_set = ['000413', '000725', '600798', '600549', '600111']
noa = len(stock_set)
df = []
for i in range(noa):
    if i == 0:
        df = ts.get_k_data(
            stock_set[i], start='2015-01-01', end='2017-09-24')[['date', 'close']]
        # df.columns = ['date', d[stock_set[i]]]
        df.columns = ['date', stock_set[i]]
    else:
        df_single = ts.get_k_data(
            stock_set[i], start='2015-01-01', end='2017-09-24')[['date', 'close']]
        # df_single.columns = ['date', d[stock_set[i]]]
        df_single.columns = ['date', stock_set[i]]
        df = pd.merge(left=df, right=df_single, on='date')


df_final = df.iloc[:, 1:]
df_final.index = df.iloc[:, 0]

df_final = df_final / df_final.ix[0] * 100

returns = np.log(df_final / df_final.shift(1))
cov = returns.cov() * 252

weight = np.random.random(noa)
weight /= np.sum(weight)

porto_return = np.sum(returns.mean() * weight) * 252
porto_var = np.dot(weight.T, np.dot(cov, weight))
std = np.sqrt(porto_var)


# ========Monte Carlo=======
# 多线程并没有改善


def monte_carlo(num):
    port_returns = []
    port_variance = []
    for p in range(num):
        returns_array = np.array(returns)
        cov_array = np.array(returns.cov())
        weights = np.random.random(len(stock_set))
        weights /= np.sum(weights)
        port_returns.append(np.sum(returns_array.mean() * 252 * weights))
        port_variance.append(np.sqrt(np.dot(weights.T,np.dot(cov_array * 252, weights))))


t0 = time.time()
monte_carlo(4000)
t1 = time.time()
print(t1-t0)

'''risk_free = 0.04
    plt.figure(figsize=(12, 8))
    plt.scatter(port_variance, port_returns, c=(
        port_returns - risk_free) / port_variance, marker='o')
    plt.grid(True)
    plt.xlabel('excepted volatility')
    plt.ylabel('expected return')
    plt.colorbar(label='Sharpe ratio')'''

# ===========最小夏普比率=============


def statistics(weights):
    weights = np.array(weights)
    port_returns = np.sum(returns.mean() * weights) * 252
    port_variance = np.sqrt(
        np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    return np.array([port_returns, port_variance,
                     port_returns / port_variance])


def min_sharpe(weights):
    return -statistics(weights)[2]


# 约束是所有参数(权重)的总和为1。这可以用minimize函数的约定表达如下
cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

# 我们还将参数值(权重)限制在0和1之间。这些值以多个元组组成的一个元组形式提供给最小化函数
bnds = tuple((0, 1) for x in range(noa))

# 优化函数调用中忽略的唯一输入是起始参数列表(对权重的初始猜测)。我们简单的使用平均分布。
opts = sco.minimize(min_sharpe, noa * [1. / noa,],
                    method='SLSQP',
                    bounds=bnds,
                    constraints=cons)

