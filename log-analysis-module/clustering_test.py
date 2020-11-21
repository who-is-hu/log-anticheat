import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import KMeans
import numpy as np

def sendToMailModule(data):
    return 0
    
X = np.array([
                [1,2,1,2,1,2], 
                [1,4,1,4,1,4],
                [1,0,1,0,1,0],
                [10,2,10,2,10,2],
                [10,4,10,4,10,4],
                [10,0,10,0,10,0],
                [10,1,10,1,10,1]
            ])
# 클러스터링 계산 fit()
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)

#center 점 확인가능
print(kmeans.cluster_centers_)

# X에 있는 요소들 어떤 레이블로 분류되었는지 나옴
lables = kmeans.labels_
print(lables)

# 가정 1=normal 0=abnormal
#만든 model로 인자로준 value 어떤 lable인지 판단.
source = {'id' : "uid01", 'value' : [4,2,1,2,1,2]}
result = kmeans.predict([source['value']])
print("normal = 0 , abnormal = 1 result=>%d" % (result))
if result == 1:
    print('abnormal user detected')
    sendToMailModule(source)

# 판단결과를 기존 데이터셋에 추가
X = np.append(X, np.array([source['value']]), axis=0)
lables = np.append(lables, np.array(result))

plt.scatter(X[:, 0], X[:, 1], c=lables)
plt.xlabel('1st attr')
plt.ylabel('2st attr')
plt.show()