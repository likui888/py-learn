# 设置编码
# -*- coding: utf-8 -*-
# 引入np
import numpy as np
# 引入pd
import pandas as pd

# 1.创建DataFrame
dataFrame = pd.date_range('20200101', periods=30, freq='M')
# print(dataFrame)
# 定义30行3列的正数随机数
dataFrame = pd.DataFrame(np.random.rand(30, 3), index=dataFrame, columns=list('ABC'))
# print(dataFrame)
# 打印头部数据
# print(dataFrame.tail())

# 合并头部一条数据和尾部一条数据
# print(pd.concat([dataFrame.head(1), dataFrame.tail(1)]))
# 打印索引数据
# print(dataFrame.index)

# 打印列数据
# print(dataFrame.columns)

# 打印数据值
# print(dataFrame.values)

# 转换为 numpy 类型
# print(dataFrame.to_numpy())
# 查看统计摘要
# print(dataFrame.describe())

# 展示 AB两列数据
# print(dataFrame[['A', 'B']][0:5])

# 打印
# print(dataFrame.loc['2020-01-31':'2020-03-31', ['A', 'B']])

# 按值筛选
# 将值保留两位小数
dataFrame = dataFrame.round(2)
# print(dataFrame)
# 打印A列大于0.5的数据
# print(dataFrame[dataFrame['A'] > 0.5])

# dataFrame = dataFrame[dataFrame > 0.5]

# print(dataFrame)
# 去除无效数据
# print(dataFrame.dropna())
# 去除重复数据
# print(dataFrame.drop_duplicates())

# 将A列正序排列，B列倒序排列
dataFrame['A'] = dataFrame['A'].sort_values(ascending=True)
dataFrame['B'] = dataFrame['B'].sort_values(ascending=False)
dataFrame.plot()
# print(dataFrame)
# 将dataFrame数据写入xlsx文件
# dataFrame.to_excel('dataFrame.xlsx')
