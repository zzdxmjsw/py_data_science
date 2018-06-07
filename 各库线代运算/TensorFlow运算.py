import tensorflow as tf
import numpy as np

config = tf.ConfigProto()
config.gpu_options.allow_growth=True
s = tf.Session(config=config)
a = np.random.normal(50,25,[10000,5000]).astype(np.float32)
b = np.random.normal(50,25,[5000,10000]).astype(np.float32)

# ===方法1
a1 = tf.random_normal([10000,5000],50,5)  # 要使用tensorflow的数据结构，原生的Python或numpy结构会导致崩溃
b1 = tf.random_normal([5000,10000],50,5)
c = tf.matmul(a1,b1)
s.run(c)

# ===方法2  但似乎结果不一致,emmmmm
x = tf.placeholder(tf.float32,shape=(10000,5000))
y = tf.placeholder(tf.float32,shape=(5000,10000))
dot = tf.matmul(x,y)
s.run(dot,feed_dict={x:a,y:b})

# 测试方法2：
data = np.linspace(1,48,48)
m1 = data.reshape(6,8)
m2 = data.reshape(8,6)
result_n = m1.dot(m2)
x1 = tf.placeholder(tf.float32,shape=(6,8))
y1 = tf.placeholder(tf.float32,shape=(8,6))
dot_2 = tf.matmul(x1,y1)
result_t = s.run(dot_2,feed_dict={x1:m1,y1:m2})  # 结果一致


# 浮点数测试方法2：
data2 = np.linspace(1,48,50).astype(np.float32)
m3 = data2.reshape(5,10)
m4 = data2.reshape(10,5)
result_n2 = m3.dot(m4)
x2 = tf.placeholder(tf.float32,shape=(5,10))
y2 = tf.placeholder(tf.float32,shape=(10,5))
dot_3 = tf.matmul(x2,y2)
result_t2 = s.run(dot_3,feed_dict={x2:m3,y2:m4})  # 结果也一致

# 错误方法：
a2 = tf.convert_to_tensor(a)
b2 = tf.convert_to_tensor(b)
c2 = tf.matmul(a2,b2)
# 或：
a3 = tf.constant(a)
b3 = tf.constant(b)
c3 = tf.matmul(a3,b3)


