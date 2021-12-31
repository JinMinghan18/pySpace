import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import cv2 as cv
import os, shutil
from pathlib import Path

p = Path(r'D:\ProgramData\test\test')
files = list(p.glob("**/*.jpg"))

# 读取图像 resize成244*244
images = [cv.resize(cv.imread(str(file)), (224, 224)) for file in files]
paths = [file for file in files]
print(paths[1])
print(type(paths[1]))
# 图像数组转换为float32类型，并归一
images = np.array(np.float32(images).reshape(len(images), -1) / 255)
# 加载训练模型
model = tf.keras.applications.MobileNetV2(include_top=False, weights='imagenet', input_shape=(224, 224, 3))
predictions = model.predict(images.reshape(-1, 224, 224, 3))
pred_images = predictions.reshape(images.shape[0], -1)
print(pred_images.shape)
print(pred_images)
# print(type(pred_images))
# kmeans 聚类
k = 3
kmodel = KMeans(init='k-means++', n_clusters=k, n_jobs=-1, random_state=1000)
kmodel.fit(pred_images)
kpredictions = kmodel.predict(pred_images)
print(kpredictions)

for i in ['1', '2', '3']:
    os.mkdir(r'D:\ProgramData\test\ani_'+str(i))
count = 0

for i in range(len(paths)):
    if kpredictions[i] == 0:
        if paths[i].__str__().split("\\")[4].split("_")[0] != "01":
            count += 1
        shutil.copy2(paths[i], r'D:\ProgramData\test\ani_1')
    elif kpredictions[i] == 1:
        if paths[i].__str__().split("\\")[4].split("_")[0] != "02":
            count += 1
        shutil.copy2(paths[i], r'D:\ProgramData\test\ani_2')
    else:
        if paths[i].__str__().split("\\")[4].split("_")[0] != "03":
            count += 1
        shutil.copy2(paths[i], r'D:\ProgramData\test\ani_3')
print("accuracy rate:")
print(1 - count/3000)