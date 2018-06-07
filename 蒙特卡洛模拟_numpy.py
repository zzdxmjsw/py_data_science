from time import time
from math import exp, sqrt, log
import numpy as np
import math

np.random.seed(2000)
t0 = time()

s0 = 100
k = 105
T = 1.0
r = 0.05
sigma = 0.2
M = 50
dt = T / M
I = 250000

S = np.zeros((M + 1, I))
S[0] = s0
for t in range(1, M + 1):
    z = np.random.standard_normal(I)
    S[t] = S[t - 1] * np.exp((r - 0.5 * sigma**2) *
                             dt + sigma * math.sqrt(dt) * z)

c0 = math.exp(-r * T) * np.sum(np.maximum(S[-1] - k, 0)) / I
tnp = time() - t0
print(tnp)
