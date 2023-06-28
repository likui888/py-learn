# uft -8 设置
# coding = utf-8
import pandas as pd
# 引入pandasReader 库
import pandas_datareader as pdr

# 1.时间序列
data = pdr.get_data_fred('GS10')
data.plot()
# 使用
# print(type(data.resample('3M').mean()))
