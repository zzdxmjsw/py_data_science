import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

player_num = 500
init_money = 250
array = np.ones(player_num) * init_money


def update(j):
    for i in range(5000):
        donor = np.random.choice(player_num, size=200, replace=False)  # 选择一个玩家支付
        invalid = np.argwhere(array < 1)
        donor = np.setdiff1d(donor, invalid, assume_unique=True)
        acceptor = np.random.choice(player_num, size=len(donor), replace=False)
        array[donor] -= 1
        array[acceptor] += 1
    fig.clear()
    x = np.linspace(0, 500, 500)
    plt.vlines(x, 0, array, colors="b", alpha=0.6)
    plt.xlim(0, 500)
    plt.ylim(0, 2000)
    plt.draw()


fig = plt.figure()
anim = animation.FuncAnimation(fig, update, 200)

