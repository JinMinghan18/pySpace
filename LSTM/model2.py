import numpy as np
from sklearn.preprocessing import MinMaxScaler

from get_stock_info import get_stock_infos


def create_dataset(dataset, time_step):
    dataX, dataY = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), 0]
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])

    return dataX

# 设置步长为30
time_step = 30
# 得到训练集极值
dataMin = []
dataMax = []
ad_dataX = []
def get_min_max():
    data = get_stock_infos()
    df2 = data['收盘价']

    dataMat = create_dataset(df2, time_step)
    print(dataMat)
    for i in range(np.array(dataMat).shape[0]):
        datai = dataMat[i]
        print(type(dataMat))
        print(type(datai))
        datai = datai.reset_index(drop=True)
        dataMin.append(min(datai))
        dataMax.append(max(datai))
        resi = []
        for j in range(datai.shape[0]):
            resi.append((datai[j] - min(datai)) / (max(datai) - min(datai)))
        ad_dataX.append(resi)

    return dataMin, dataMax, ad_dataX

if __name__ == '__main__':
    # 得到数据集
    dataMin, dataMax, ad_dataX = get_min_max()
    result = np.array(ad_dataX)
    row = result.shape[0] - 100

    train = result[:row, :]
    print(train)
    np.random.shuffle(train)
    print(train)



