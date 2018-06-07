import numpy as np
import pandas as pd
from numba import jit
def calculate_value(red, green):
    while green >= 1 or red >= 1:
        if green == 0:  # (red,0)
            value = red
            return value
        if red == 0:  # (0,green)
            value = 0
            return value
        value = max(0, red / (red + green) * (1 + calculate_value(red - 1, green)) +
                    green / (red + green) * (-1 + calculate_value(red, green - 1)))
        return value


def tail_recursion(red, green, num):  # 和一般递归没有区别  不是尾递归
    if num == 0:
        if red == 0:  # (0,green,0)
            return 0
        elif green == 0:  # (red,0,0)
            return red
        else:  # (red,green,0)
            value = max(0,
                       red / (red + green) * (1 + tail_recursion(red - 1,
                                                                 green,
                                                                 num)) + green / (red + green) * (-1 + tail_recursion(red,
                                                                                                                      green - 1,
                                                                                                                      num)))
            return value
    else:  # n != 0
        if red == 0:  # (0,green,n)
            return 0
        elif green == 0:  # (red,0,n)
            return num
        else:  #(red,green,n)
            value = max(0,red / (red + green) * (1 + tail_recursion(red - 1,green,num - 1)) +
                        green / (red + green) * (-1 + tail_recursion(red,green - 1,num - 1)))
            return value

tail_recursion(2,2,2)


#  矩阵
#  对于n red m green 需要2^(n+m-1)个状态节点，n+m-1个时间状态
n = 50
m = 50

direct_arr = np.zeros([n+1,m+1])
direct_arr[:,0] = range(n+1)
for i in range(1,n+1):  # 行
    for j in range(1,m+1):  # 列
        left_value = direct_arr[i,j-1]
        up_value = direct_arr[i-1,j]
        direct_arr[i,j] = max(0,i/(i+j)*(1+up_value)+j/(i+j)*(-1+left_value))




def func(x):
    print(x.index)
# TODO: 1、改写成矩阵形式(for)
# TODO: 2、参考贝尔曼方程代码
# TODO: 3、最后尝试迭代器生成器
# TODO: 4、尾递归写法


