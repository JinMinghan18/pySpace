import pandas as pd
import numpy as np

# 删除空值
def handlempty():
    data = pd.read_csv(r'D:\大学\大三\数据挖掘\数据\交通时空大数据分析挖掘系统-数据\服创大赛-原始数据.csv', engine='python',
                       usecols=['timestamp', 'imsi', 'lac_id', 'cell_id','timestamp1'])
    data = data.fillna(value=None,method='ffill',axis=0,limit=None)
    # data = data.dropna()
    return data
# 处理错误数据
def clean2():
    data2 = handlempty()
    for j, indexs in data2['imsi'].iteritems():
        for i in indexs:
            if (i == '#' or i == '*' or i == '^' or i == '-'):
                data2['imsi'][j] = data2['imsi'][j-1]

                break
    data2.to_csv(r'D:\大学\大三\数据挖掘\数据\交通时空大数据分析挖掘系统-数据\fillCleaned.csv')



# 按照imsi归类
def statistic():
    data = pd.read_csv(r'D:\大学\大三\数据挖掘\数据\交通时空大数据分析挖掘系统-数据\fillCleaned.csv', engine='python',
                       usecols=['timestamp', 'imsi', 'lac_id', 'cell_id','timestamp1'])
    groups = data.groupby('imsi')
    i=0
    for group_name, group_data in groups:
        print(group_name, '+', group_data)
        i+=1
        basepath="D:\大学\大三\数据挖掘\数据\交通时空大数据分析挖掘系统-数据\group"
        path=basepath+"\grouped"+str(i)+".csv"
        group_data.to_csv(path)


