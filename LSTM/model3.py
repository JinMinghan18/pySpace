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


def create_dataset(dataset, time_step):
    dataX, dataY = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), 0]
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])

    return np.array(dataX), np.array(dataY)


if __name__ == '__main__':
    df = get_stock_infos()
    # 绘制图形
    # plt.plot(df['日期'], df['收盘价'])
    # 数据归一化
    scaler = MinMaxScaler(feature_range=(0, 1))
    df2 = scaler.fit_transform(np.array(df["收盘价"]).reshape((-1, 1)))
    # 分割出训练集和测试集(0.9,0.1)
    training_size = int(len(df2) * 0.9)
    test_size = len(df2) - training_size
    train_data, test_data = df2[0:training_size, :], df2[training_size:len(df2), :1]

    # 转换训练集、测试集
    # 设置步长
    time_step = 30
    train_x, train_y = create_dataset(train_data, time_step)

    test_x, test_y = create_dataset(test_data, time_step)
    # 将输入转换为[sample,步长,特征值features]
    train_x = train_x.reshape(train_x.shape[0], train_x.shape[1], 1)
    train_y = train_y.reshape((-1, 1))
    test_x = test_x.reshape(test_x.shape[0], test_x.shape[1], 1)
    test_y = test_y.reshape((-1, 1))

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

    model.add(LSTM(60, input_shape=(train_x.shape[1], train_x.shape[2]), return_sequences=True))
    model.add(Dropout(0))
    model.add(LSTM(60, return_sequences=False))
    model.add(Dropout(0))
    model.add(Dense(1))
    model.add(Activation('tanh'))
    start = time.time()
    model.compile(loss='mse', optimizer='adam')
    history = model.fit(train_x, train_y, batch_size=70, epochs=70, validation_split=0.33, verbose=2)
    train_predict = model.predict(train_x)
    test_predict = model.predict(test_x)


    # 反归一化
    train_predict = scaler.inverse_transform(train_predict)
    test_predict = scaler.inverse_transform(test_predict)
    test_y = scaler.inverse_transform(test_y)
    train_y = scaler.inverse_transform(train_y)

    train_RMSE = math.sqrt(mean_squared_error(train_y, train_predict))
    train_Mae = mean_absolute_error(train_y, train_predict)


    test_RMSE = math.sqrt(mean_squared_error(test_y, test_predict))
    test_Mae = mean_absolute_error(test_y, test_predict)

    train_R2 = r2_score(train_predict, train_y)
    test_R2 = r2_score(test_predict, test_y)

    test_Mape = np.mean(np.abs(test_predict - test_y)/test_y) * 100
    print("测试mape")
    print(test_Mape)
    print("训练R2")
    print(train_R2)
    print("测试R2")
    print(test_R2)
    print("训练mae")
    print(train_Mae)

    print("测试mae")
    print(test_Mae)
    print("测试mse")
    print(test_RMSE)
    print("训练mse")
    print(train_RMSE)

    # 输出诊断数据和图
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('train and validation loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper right')
    plt.show()

    # 绘制图像
    # trainPredictPlot = np.empty_like(df2)
    # trainPredictPlot[:, :] = np.nan
    # trainPredictPlot[30:len(train_predict) + 30, :] = train_predict

    # testPredictPlot = np.empty_like(df2)
    # testPredictPlot[:, :] = np.nan
    # test_show = test_predict[682:712, :]
    # testPredictPlot[0:30, :] = test_show
    #
    # base = scaler.inverse_transform(df2)
    # base = base[7396:7426, :]
    # plt.plot(base, 'blue')


    # plt.plot(trainPredictPlot, 'red')
    # plt.plot(testPredictPlot, 'green')
    # plt.savefig(fname="szzs.svg", format="svg")
    # plt.show()


