import sympy as sy
import numpy as np
import matplotlib.pyplot as plt
from sympy import *

sy.init_printing(pretty_print=False,use_latex=True)
x = sy.Symbol('x')
f = x**2 + 3 + 0.5 * x**2
a = Integral(sy.sin(x)+0.5*x,(x,2,10))