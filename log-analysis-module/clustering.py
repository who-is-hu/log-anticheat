from sklearn.cluster import KMeans
import numpy as np
from sklearn.decomposition import PCA
import pandas as pd
from sklearn import preprocessing


class ClusteringMgr:
    kmeans = {}
    pca = {}
    source_dataset = []
    abnormal_label = -1

    def __init__(self, X):
        self.pca = PCA(n_components=2)
        self.createClusteringModel(X)

    def createClusteringModel(self, X):
        print("create clustering model...")
        self.source_dataset = X
        scaledDataset = preprocessing.StandardScaler().fit_transform(X)
        print('scaled X')
        for d in scaledDataset:
            print(d)
        principalComponents = self.pca.fit_transform(scaledDataset)
        dataset = np.array(principalComponents)
        print('pca X')
        for d in dataset:
            print(d)
        self.kmeans = KMeans(n_clusters=2, random_state=0).fit(dataset)

        # test for clustering accuracy
        n1 = 0
        n2 = 0
        for i in self.kmeans.labels_:
            if i == 0:
                n1 += 1
            else:
                n2 += 1
        print("n1", n1)
        print("n2", n2)
        if min(n1, n2) == n1:
            self.abnormal_label = 0
        else:
            self.abnormal_label = 1
        print('abnormal label', self.abnormal_label)
        ##############################
        print("Done: clustering model created")

    # 새로운 data의 소속 군집 반환
    def predictNewData(self, data, append_to_dataset=False):
        print('on predict')
        try:
            # dataset = [data]  # np.array(data)
            result = self.kmeans.predict([data]).tolist()
        except Exception as e:
            print(e)
        return result[0]

    def getPCfrom1dArray(self, X):
        print('source')
        print(X)
        print('before', len(self.source_dataset))
        self.source_dataset.append(X)
        print('after', len(self.source_dataset))
        scaledDataset = preprocessing.StandardScaler().fit_transform(self.source_dataset)
        print('scaled 1d arr')
        scaledArr = scaledDataset[len(scaledDataset)-1]
        print(scaledArr)
        printcipalComponents = self.pca.fit_transform(scaledDataset)
        print(printcipalComponents[len(printcipalComponents)-1])
        return printcipalComponents[len(printcipalComponents)-1]

    def getAbnormalLabel(self):
        return self.abnormal_label
