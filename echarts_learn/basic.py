import pyecharts
import pandas as pd
import numpy as np

title = 'bar chart'
index = pd.date_range('1/1/2017',periods=6, freq='M')
df1 = pd.DataFrame(np.random.randn(6),index = index)
df2 = pd.DataFrame(-np.random.randn(6),index = index)

dt_value1 = [i[0] for i in df1.values]
dt_value2 = [i[0] for i in df2.values]

_index = [i for i in index.format()]
bar = pyecharts.Bar()
bar.add('profit',_index,dt_value1,is_stack=True,mark_line=['average'],mark_point=['min','max'])
bar.add('loss',_index,dt_value2,is_stack=True,mark_line=['average'],mark_point=['min','max'])
bar.render()
