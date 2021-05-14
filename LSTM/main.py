import math
import keras
import os
# from keras.losses import mean_squared_error
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from tensorflow.python.keras.layers import Dropout, Activation

from get_stock_info import get_stock_infos
import matplotlib.pyplot as plt
import numpy as np
from numpy import array
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM


# 将数组的值转换为矩阵
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
    X_train, Y_train = create_dataset(train_data, time_step)
    print(X_train)
    X_test, Y_test = create_dataset(test_data, time_step)
    # 将输入转换为[sample,步长,特征值features]
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
    # print(X_test)
    # 创建stack LSTM模型

    model = Sequential()
    model.add(LSTM(60, return_sequences=True, input_shape=(time_step, 1)))
    model.add(Dropout(0))
    # model.add(LSTM(5, return_sequences=True, input_shape=(time_step, 1)))
    model.add(LSTM(60, return_sequences=False))
    model.add(Dropout(0))
    model.add(Dense(1))
    model.add(Activation('tanh'))
    model.compile(loss='mse', optimizer='adam')
    # 训练模型
    history = model.fit(X_train, Y_train, validation_split=0.33, epochs=50, batch_size=50, verbose=2)
    # 预测并确认性能指标
    train_predict = model.predict(X_train)
    test_predict = model.predict(X_test)
    print(test_predict)

    # 转换回原始形态
    train_predict = scaler.inverse_transform(train_predict)
    test_predict = scaler.inverse_transform(test_predict)
    print(type(test_predict))
    # 计算训练集均方根误差\MAE\R2
    train_RMSE = math.sqrt(mean_squared_error(Y_train, train_predict))
    train_Mae = mean_absolute_error(Y_train, train_predict)
    train_R2 = r2_score(train_predict, Y_train)
    # 计算测试集均方根误差\MAE\R2
    test_RMSE = math.sqrt(mean_squared_error(Y_test, test_predict))
    test_Mae = mean_absolute_error(Y_test, test_predict)
    test_R2 = r2_score(test_predict, Y_test)

    #输出诊断数据和图
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('train and validation loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper right')
    plt.show()
    # print(test_RMSE)
    # print(train_RMSE)
    # print(test_Mae)
    print(test_R2)
    print(train_R2)

    # 作图
    # 绘制训练集曲线
    look_back = 30
    trainPredictPlot = np.empty_like(df2)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[look_back:len(train_predict) + look_back, :] = train_predict
    # 绘制测试集曲线
    testPredictPlot = np.empty_like(df2)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(train_predict) + (look_back * 2) + 1: len(df2) - 1, :] = test_predict
    # 绘制基线和预测
    plt.plot(scaler.inverse_transform(df2), 'blue')
    plt.plot(trainPredictPlot, 'red')
    plt.plot(testPredictPlot, 'green')
    # plt.savefig(fname="name.svg", format="svg")
    # plt.show()
    # plt.savefig("szzs.eps", dpi=600, format='eps')
    x_input = test_data[len(test_data)-look_back:].reshape(1, -1)
    x_input.shape
    temp_input = list(x_input)
    temp_input = temp_input[0].tolist()

    # 未来三日预测
    lst_output = []
    n_step = 30
    i = 0
    while(i<3):
        if(len(temp_input) > 30):
            x_input = np.array(temp_input[1:])
            print("{} day input {}".format(i, x_input))
            x_input = x_input.reshape(1, -1)
            x_input = x_input.reshape((1, n_step, 1))

            yhat = model.predict(x_input, verbose=0)
            print("{} day output {}".format(i, yhat))
            temp_input.extend(yhat[0].tolist())
            temp_input = temp_input[1:]
            lst_output.extend(yhat.tolist())
            i = i + 1
        else:
            x_input = x_input.reshape((1, n_step, 1))
            yhat = model.predict(x_input, verbose=0)
            # print(yhat[0])
            temp_input.extend(yhat[0].tolist())
            # print(len(temp_input))
            lst_output.extend(yhat.tolist())
            i = i + 1
    print(lst_output)
    print(scaler.inverse_transform(lst_output))
