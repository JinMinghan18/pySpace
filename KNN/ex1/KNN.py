import numpy as np
from os import listdir
from sklearn.neighbors import KNeighborsClassifier as KNN

# 将32*32矩阵转为1*1024向量
def convertImgtoVector(filename):
    #创建向量
    Vector = np.zeros((1, 1024))
    #打开文件
    fr = open(filename)
    #按行读取
    for i in range(32):
        #读一行数据
        line = fr.readline()
        #每一行的前32个元素添加到Vector中
        for j in range(32):
            Vector[0, 32*i+j] = int(line[j])
        #返回向量
    return Vector


def handwrittingClassify():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')
    m = len(trainingFileList)
    #初始化训练矩阵，训练集
    trainingMat = np.zeros((m, 1024))
    #从文件名中解析出训练集类别
    for i in range(m):
        #读取文件名
        fileName = trainingFileList[i]
        #读取分类数字
        classifyNumber = int(fileName.split('_')[0])
        #读取到的类别添加到hwLabel中
        hwLabels.append(classifyNumber)
        #将每一个文件的1*1024数据存储到traningMat矩阵中
        trainingMat[i, :] = convertImgtoVector('trainingDigits/%s' % (fileName))
    #构建KNN分类器
    neigh = KNN(n_neighbors =3, algorithm= 'auto')
    #拟合模型，trainingMat为训练矩阵，hwlabels为对应的标签
    neigh.fit(trainingMat, hwLabels)
    #返回testDigits目录下的文件列表
    testFileList = listdir('testDigits')
    #错误识别计数
    errCount = 0.0
    #测试集计数
    mTest = len(testFileList)
    #获取测试集类别并分类
    for i in range(mTest):
        #获取文件名
        fileName = testFileList[i]
        #获取分类的数字
        classifyNumber = int(fileName.split('_')[0])
        #获得测试集向量，用于测试
        VectorTest = convertImgtoVector('testDigits/%s' % (fileName))
        #获取测试结果
        classifiedResult = neigh.predict(VectorTest)
        print("Test result is %d\tReal Result is %d" % (classifiedResult, classifyNumber))
        if(classifiedResult != classifyNumber):
            errCount += 1.0
    print("Totally %d digits\nerror ration is %f%%" % (errCount, errCount/mTest * 100))

if __name__=='__main__':
    handwrittingClassify()
