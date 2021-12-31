import math

import pandas as pd
import numpy as np
import time
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.models import Sequential
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import MinMaxScaler
from get_stock_info import get_stock_infos
from sklearn.model_selection import train_test_split

def create_dataset(dataset, time_step):
    dataX, dataY = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), 0]
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])

    return np.array(dataX), np.array(dataY)

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    # 获取特征值数量n_vars
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    # 创建31个v(t-1)作为列名,30->0,步长-1
    for i in range(n_in, 0, -1):
        # 向列表cols中添加一个df.shift(1)的数据
        cols.append(df.shift(i))
        # print(cols)
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]


    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        # 向列表cols中添加一个df.shift(-1)的数据
        cols.append(df.shift(-i))
        # print(cols)
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # print(cols)
    # 将列表中两个张量按照列拼接起来，list(v1,v2)->[v1,v2],其中v1向下移动了一行，此时v1,v2是监督学习型数据
    agg = pd.concat(cols, axis=1)
    # print(agg)
    # 重定义列名
    agg.columns = names
    # print(agg)
    # 删除空值
    if dropnan:
        agg.dropna(inplace=True)
    return agg

if __name__ == '__main__':
    df = get_stock_infos()
    # 绘制图形
    # plt.plot(df['日期'], df['收盘价'])
    # 数据归一化
    # 设置步长
    time_step = 30
    features = 2

    df.drop(["交易时间"], axis=1, inplace=True)
    reframed = series_to_supervised(df, time_step, 1)
    reframed = reframed.iloc[:, :features * time_step + 1]
    reframed = reframed.values
    X = reframed[:, :-1]
    Y = reframed[:, -1]
    Y = Y.reshape(-1, 1)
    # 将所有数据缩放到（0，1）之间
    X_scaler = MinMaxScaler(feature_range=(0, 1))
    X = X_scaler.fit_transform(X)
    X_input = X[-1, :]
    X_input = X_input.reshape(1, 30, 2)
    print(X_input)
    # print("change x.shape")
    # print(X.shape)
    Y_scaler = MinMaxScaler(feature_range=(0, 1))
    Y = Y_scaler.fit_transform(Y)
    # print("change Y.shape")
    # print(Y.shape)
    train_x, test_x, train_y, test_y = train_test_split(X, Y, test_size=0.1)
    # print("test_x.shape")
    # print(test_x.shape)
    # print("test_x")
    # print(test_x)
    # 将输入转换为[sample,步长,特征值features]
    train_x = train_x.reshape(train_x.shape[0], time_step, 2)
    train_y = train_y.reshape(-1, 1)
    test_x = test_x.reshape(test_x.shape[0], time_step, 2)
    test_y = test_y.reshape(-1, 1)
    # print("change test_x.shape")
    # print(test_x.shape)
    # print("change test_x")
    # print(test_x)
    # df = pd.read_csv('http://quotes.money.163.com/service/chddata.html?code=0000001&start=19901219&end=&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER', encoding='GBK')
    # data = df['收盘价']
    # scaler = MinMaxScaler(feature_range=(0, 1))
    #
    # train = data[0 : 6000]
    #
    # test = data[6000 : ]
    # seq_len = 30
    # res = []
    # for i in range(len(data) - seq_len - 1 + 1):
    #     res.append(data[i : i+seq_len + 1])
    # data_min = []
    # data_max = []
    # ad_res = []
    # for i in range(np.array(res).shape[0]):
    #     datai = res[i]
    #     datai = datai.reset_index(drop=True)
    #     data_min.append(min(datai))
    #     data_max.append(max(datai))
    #     resi = []
    #     # for j in range(datai.shape[0]):
    #     #     resi.append((datai[j] - min(datai)) / (max(datai) - min(datai)))
    #     #按组归一化处理
    #     resi = scaler.fit_transform(np.array(datai).reshape((-1, 1)))
    #     ad_res.append(resi)
    #
    # result = np.array(ad_res)
    # row = result.shape[0] - 100
    # train = result[:row, :]
    # np.random.shuffle(train)
    # train_x = train[:, :-1]
    # train_y = train[:, -1]
    # test = result[row:, :]
    # test_x = test[:, :-1]
    # test_y = test[:, -1]
    #
    # train_x = np.reshape(train_x, (train_x.shape[0], train_x.shape[1], 1))
    # test_x = np.reshape(test_x, (test_x.shape[0], test_x.shape[1], 1))
    # print(train_x)

    model = Sequential()

    model.add(LSTM(400, input_shape=(train_x.shape[1], train_x.shape[2]), return_sequences=True))
    model.add(Dropout(0.1))
    model.add(LSTM(400, input_shape=(train_x.shape[1], train_x.shape[2]), return_sequences=True))
    model.add(Dropout(0.1))
    model.add(LSTM(400, return_sequences=False))
    model.add(Dense(1))
    # model.add(Activation('tanh'))
    start = time.time()
    model.compile(loss='mse', optimizer='adam')
    history = model.fit(train_x, train_y, batch_size=1000, epochs=100, validation_split=0.1, verbose=2)
    # train_predict = model.predict(train_x)
    test_predict = model.predict(test_x)


    # 输出诊断数据和图
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('train and validation loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper right')
    plt.show()

    # 反归一化
    # train_predict = X_scaler.inverse_transform(train_predict)
    # train_y = Y_scaler.inverse_transform(train_y)
    test_predict = Y_scaler.inverse_transform(test_predict)
    test_y = Y_scaler.inverse_transform(test_y)

    # train_RMSE = math.sqrt(mean_squared_error(train_y, train_predict))
    # train_Mae = mean_absolute_error(train_y, train_predict)

    test_RMSE = math.sqrt(mean_squared_error(test_y, test_predict))
    test_Mae = mean_absolute_error(test_y, test_predict)

    # train_R2 = r2_score(train_predict, train_y)
    test_R2 = r2_score(test_predict, test_y)

    test_Mape = np.mean(np.abs(test_predict - test_y)/test_y) * 100
    print("测试mape")
    print(test_Mape)
    # print("训练R2")
    # print(train_R2)
    print("测试R2")
    print(test_R2)
    # print("训练mae")
    # print(train_Mae)

    print("测试mae")
    print(test_Mae)
    print("测试mse")
    print(test_RMSE)
    # print("训练mse")
    # print(train_RMSE)

    

    # 绘制图像
    # trainPredictPlot = np.empty_like(df2)
    # trainPredictPlot[:, :] = np.nan
    # trainPredictPlot[30:len(train_predict) + 30, :] = train_predict

    plt.plot(test_predict, label='real')
    plt.plot(test_y, label='pre')
    plt.legend()
    plt.show()

    # plt.plot(trainPredictPlot, 'red')
    # plt.savefig(fname="szzs.svg", format="svg")
    # plt.show()

    #未来预测
    X_pre = model.predict(X_input)
    print(Y_scaler.inverse_transform(X_pre))

