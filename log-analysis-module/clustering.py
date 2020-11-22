from sklearn.cluster import KMeans
import numpy as np


class ClusteringMgr:
    kmeans = {}
    
    def __init__(self, X):
        self.createClusteringModel(X)
    
    def createClusteringModel(self,X):
        print("create clustering model...")
        dataset = np.array(X)
        self.kmeans = KMeans(n_clusters=2, random_state=0).fit(dataset)
        print("Done: clustering model created")   

    # 새로운 data의 소속 군집 반환
    def predictNewData(self, data, append_to_dataset=False):
        result = self.kmeans.predict(data)
        return result
       
