import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import KMeans

iris = datasets.load_iris()
samples = iris.data

model = KMeans(n_clusters = 3)
model.fit(samples)
labels = model.predict(samples)

x = samples[:,0]
y = samples[:,1]
plt.scatter(x,y,c=labels, alpha=0.5)
plt.xlabel('sepal length;')
plt.ylabel('sepal width')
plt.show()
