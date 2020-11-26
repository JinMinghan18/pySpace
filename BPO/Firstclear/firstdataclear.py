import pandas as pd
import numpy as np
import os

def clear1():
    data = pd.read_csv(r'D:\大学\大三\数据挖掘\数据\交通时空大数据分析挖掘系统-数据\服创大赛-原始数据.csv', engine='python', usecols=['timestamp','imsi','lac_id','cell_id'])
    # 删除空值
    data = data.dropna(axis=0,how='any')
# 删除异常值
    data_imsi = data['imsi']

    for j,indexs in data_imsi.iteritems():
        for i in indexs:
            if(i == '#' or i == '*' or i == '^'):
                data = data.drop(j)
                print(i)
                break
    data.to_csv(r'D:\大学\大三\数据挖掘\数据\交通时空大数据分析挖掘系统-数据\deleteType\testCleaned1.csv')

    # data.to_csv(r'D:\大学\大三\数据挖掘\数据\交通时空大数据分析挖掘系统-数据\testCleaned0.csv')

def statistic():
    data = pd.read_csv(r'D:\大学\大三\数据挖掘\数据\交通时空大数据分析挖掘系统-数据\testCleaned1.csv', engine='python',
                       usecols=['timestamp', 'imsi', 'lac_id', 'cell_id'])
    groups = data.groupby('imsi')
    i=0
    for group_name, group_data in groups:
        print(group_name, '+', group_data)
        i+=1
        basepath="D:\大学\大三\数据挖掘\数据\交通时空大数据分析挖掘系统-数据\group"
        path=basepath+"\grouped"+str(i)+".csv"
        group_data.to_csv(path)

