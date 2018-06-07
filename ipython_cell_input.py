import pandas as pd
import json
import matplotlib
import numpy as np
import statsmodels.api as sm
import scipy.stats as scs
import matplotlib.pyplot as plt
import tushare as ts
import scipy.optimize as sco
from numba import jit
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
    port_returns = pd.Series(np.zeros(num))
    port_variance = pd.Series(np.zeros(num))
    for p in range(num):
        weights = np.random.random(len(stock_set))
        weights /= np.sum(weights)
        port_returns[p] = np.sum(returns.mean() * 252 * weights)
        adj_returns = np.dot(returns.cov() * 252, weights)
        port_variance[p] = np.sqrt(np.dot(weights.T, adj_returns))

    return port_returns, port_variance
monte_carlo(4000)