import matplotlib.pyplot as plt

time = [i for i in range(0, 19)]
number = [9.6, 18.3, 29, 47.2, 71.1, 119.1, 174.6, 257.3,
          350.7, 441.0, 513.3, 559.7, 594.8, 629.4, 640.8,
          651.1, 655.9, 659.6, 661.8]

plt.title('Relationship between time and number')  # 创建标题
plt.xlabel('time')  # X轴标签
plt.ylabel('number')  # Y轴标签
plt.plot(time, number)  # 画图
plt.show()  # 显示

