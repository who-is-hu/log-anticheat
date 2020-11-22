from sklearn.cluster import KMeans
import numpy as np


class ClusteringMgr:
    kmeans = {}
    
    # 처음 모델을 만들기 위함
    def __init__(self, X):
        createClusteringModel(self,X)
    
    def preprocess(self, message):
        data = json.loads(message)
        kpd = data['kill'] / data['death']
        data.pop('kill')
        data.pop('death')
        data.update({'kpd': kpd})
        print(data)
        return data.values()

    def createClusteringModel(self,X):
        print("create clustering model...")
        dataset = np.array(X)
        self.kmeans = KMeans(n_clusters=2, random_state=0).fit(dataset)
        print("Done: clustering model created")

    # 새로운 data의 소속 군집 반환
    def predictNewData(data, append_to_dataset=False):
        p_data = self.preprocess(data)
        result = self.kmeans.predict(p_data)
        #if append_to_dataset == True:
        #    X = np.append(X, np.array([source['value']]), axis=0)
        #    lables = np.append(lables, np.array(result))
        return result
       
