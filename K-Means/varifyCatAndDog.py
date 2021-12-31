import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import pylab
import tensorflow as tf
from tensorflow import keras
from keras.utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator, load_img
from PIL import Image
import random

# 引入训练数据
filenames = os.listdir(r'C:\test\train')
categories = []
for f_name in filenames:
    category = f_name.split('.')[0]
    if category == 'dog':
        categories.append(1)
    else:
        categories.append(0)
df = pd.DataFrame({
    'filenames': filenames,
    'category': categories
})

# 导入测试数据
path = os.listdir(r'C:\test\test2')
count = 0
name = []
for i in path:
    count += 1
    name.append(i)
print("totally %d test example" % count)
# print(df)
cwd = 'C:/test/train/'
data = []
label = []
for i in range(25000):
    image = Image.open(cwd + df.filenames[i])
    image = image.resize((128, 128))
    image = np.array(image)
    data.append(image)
    label.append(df.category[i])

data = np.array(data)
label = np.array(label)

# 测试图片处理
test_img = []
for i in range(800):
    image = Image.open('C:/test/test2/'+name[i])
    image = image.resize((128, 128))
    image = np.array(image)
    test_img.append(image)

test_img = np.array(test_img).reshape(-1, 128, 128, 3)
print(test_img)
print(test_img.shape)
print(type(test_img))


X_train, X_test, Y_train, Y_test = train_test_split(data, label, test_size=0.4, train_size=0.6)
print(X_test)
print(X_test.shape)
print(type(X_test))
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(128, 128, 3)),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(2048, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(1024, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(2, activation='sigmoid')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
mod = model.fit(X_train, Y_train, epochs=1, batch_size=200, verbose=2)

# 测试集准确度测试
# model.evaluate(X_test, Y_test)
# 测试集精确度曲线绘制
plt.figure(figsize=(15, 8))
plt.plot(mod.history['acc'], label='accuracy')
plt.xlabel("epochs")
plt.ylabel("accuracy")
plt.legend()
plt.show()




# 预测
y_predicted = model.predict(test_img)
print(y_predicted)
y_predicted_labels = [np.argmax(i) for i in y_predicted]

index = 4
lab = y_predicted_labels[index]
animal = 'dog'
if lab == 0:
    animal = 'cat'
plt.xlabel(animal)

plt.imshow(test_img[index])
pylab.show()
