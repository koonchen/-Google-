# coding:utf8
import tensorflow as tf
from numpy.random import RandomState

# 定义训练数据 batch 的大小
batch_size = 8

# 定义神经网络的参数，这里还是沿用 3.4.2 小节中给出的神经网络数据。
w1 = tf.Variable(tf.random_normal([2,3],stddev=1,seed=1))
w2 = tf.Variable(tf.random_normal([3,1],stddev=1,seed=1))

# 在 shape 的一个维度上使用 None 可以方便使用不大的 batch 大小。
# 在训练时需把数据分成较小的 batch ,在测试时可以一次使用全部数据。
# 当数据集较小时这样比较方便测试。但数据集较大时，可能会导致内存溢出。
x = tf.placeholder(tf.float32,shape=(None,2),name='x-input')
y_ = tf.placeholder(tf.float32,shape=(None,1),name='y-input')

# 定义神经网络前向传播
a = tf.matmul(x,w1)
y = tf.matmul(a,w2)

# 定义损失函数和反向传播算法
# 定义损失函数来刻画预测值与真实值之间的差距
cross_entropy = -tf.reduce_mean(y_ * tf.log(tf.clip_by_value(y,1e-10,1.0)))

# 定义反向传播法来优化神经网络中的参数
# 0.001 是学习率
# 反向传播
train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)

# 通过随机数生成一个模拟数据集
rdm = RandomState(1)
dataset_size = 128
X = rdm.rand(dataset_size,2)

# 定义规则来给出样本的标签
Y = [[int(x1 + x2 < 1)] for (x1,x2) in X]

# 创建一个会话来运行程序
with tf.Session() as sess:
  # 初始化所有变量，但没有运行
  init_op = tf.global_variables_initializer()

  # 现在运行初始化的变量
  sess.run(init_op)
  print("w1:", sess.run(w1))
  print("w2:", sess.run(w2))

  # 设定训练的轮数
  STEPS = 5000
  for i in range(STEPS):
    # 每次选取 batch_size 个样本进行训练
    start = (i * batch_size) % dataset_size
    end = min(start + batch_size,dataset_size)

    # 通过选取的样本训练神经网络并更新参数
    sess.run(train_step,feed_dict={x:X[start:end],y_:Y[start:end]})

    if i % 1000 == 0:
      # 每隔一段时间计算所有数据的交叉熵
      total_cross_entropy = sess.run(cross_entropy,feed_dict={x:X,y_:Y})
      print("After %d training step(s), cross entropy on all data is %g" % (i, total_cross_entropy))

  print("w1:", sess.run(w1))
  print("w2:", sess.run(w2))
