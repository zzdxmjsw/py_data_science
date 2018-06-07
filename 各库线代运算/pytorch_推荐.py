import torch
import numpy as np

a = np.random.random([10000,5000]).astype(np.float32)
b = np.random.random([5000,10000]).astype(np.float32)
c = a.dot(b)
a2 = torch.Tensor(a).cuda()  # 或a2 = torch.from_numpy(a).cuda()
b2 = torch.Tensor(b).cuda()  # b2 = torch.from_numpy(b).cuda()
c1 = torch.matmul(a2,b2)  # 能计算一维
c2 = torch.mm(a2,b2)  #  计算矩阵不能计算向量,但矩阵结果一致

# ====测试：
c1_n = c1.cpu().numpy()  # cuda的gpu数组，先转化为cpu数组再转numpy数组，有差异但很小
c2_n = c2.cpu().numpy()

# c1_n、c2_n和c基本一致
