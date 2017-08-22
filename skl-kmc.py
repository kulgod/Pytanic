import numpy as np 
import pandas as pd 
from sklearn import cluster

def fit(X,y):
	model = cluster.KMeans(n_clusters=40, max_iter=10000, tol=0.000001, n_jobs=-2)
	model.fit(X,y)
	return model

def train_and_score(X, y, k, model):
	labels = model.predict(X)
	cluster_labels = np.column_stack((labels,y))
	votes = [ [0,0] for _ in range(k) ]
	for vote in cluster_labels:
		cluster = int(vote[0])
		label = int(vote[1])
		votes[cluster][label] += 1

	cluster_proba = [ x[1] / float(sum(x)) for x in votes ]
	correct = 0
	n = 0
	for x in cluster_labels:
		cluster = int(x[0])
		yhat = 1 if cluster_proba[cluster] > 0.5 else 0
		if yhat == int(x[1]):
			correct += 1
		n += 1
	return correct / float(n), cluster_proba

def predict_kmeans(cluster, cluster_proba):
	return 1 if cluster_proba[int(cluster)] > 0.5 else 0

def main():
	train_df = pd.read_csv("train-prep.csv")
	test_df = pd.read_csv("test-prep.csv")
	X = train_df.as_matrix(['Class', 'Female','Child','Sibsp','Parch'])
	Xtest = test_df.as_matrix(['Class', 'Female','Child','Sibsp','Parch'])
	y = train_df.as_matrix(['Survived']).flatten()
	model = fit(X,y)
	score, cluster_proba = train_and_score(X,y,40,model)

	y_labels = model.predict(Xtest)
	yhat = [ predict_kmeans(x,cluster_proba) for x in y_labels ]

	y_publish = np.column_stack((test_df.as_matrix(['ID']), yhat))
	publish_df = pd.DataFrame(y_publish)
	publish_df.to_csv("output/prediction-kmc.csv", header=["PassengerId","Survived"], index=False)

if __name__ == "__main__":
	main()

