# -*- coding: utf-8 -*-
# pd定义
import pandas as pd
import numpy as np

# pd.DataFrame
data = {'apple': [1, 2], 'banana': [3, 4], 'orange': [5, 6]}
data = pd.DataFrame(data)

# 打印 列apple
# print(data['apple'])

# 更改下标
data.index = [2, 1]
# 重置下标 drop = True 丢弃原来的下标
data = data.reset_index(drop=True)
# np 转换为DataFrame

# reshape(3,3) 3行3列
np_data = np.arange(1, 10).reshape(3, 3)
# 将np_data 转换为9行一列
# np_data = np_data.reshape(9, 1)
# 将np_data 转换为 DataFrame
np_data = pd.DataFrame(np_data, columns=['a', 'b', 'c'])
# 取出values
np_data = np_data.values
# 打印一行三列值
# print(np_data[0, 0:2])

# 将DataFrame 转换为 np
np_data = np.array(np_data)
print(np_data)
