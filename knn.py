import numpy as np 
import csv

def build_list(filename):
	X = []
	with open(filename) as data:
		reader = csv.reader(data, delimiter=',')
		reader.__next__() #skip the first line
		for row in reader:
			X.append( [row[0]] + [float(x) for x in row[1:]] )
	return X

def sorted_add(neighbors, elem, k):
	neighbors[elem[0]] = elem[1]
	if len(neighbors) > k:
		items = sorted(neighbors.items(), key=lambda t: t[1][0])
		return dict(items[:k])
	else:
		return neighbors

def dist(arr1, arr2, n=5, start=1):
	deltas = []
	for i in range(start,start+n):
		deltas.append((arr1[i]-arr2[i])**2)
	return sum(deltas)

def vote(neighbors, prob=False):
	total = 0
	for n in neighbors.values():
		total += n[1]
	survival_prob = float(total) / len(neighbors) 

	if prob:
		return survival_prob
	return 1 if survival_prob > 0.5 else 0

def nearest_neighbors(X, x, k=5):
	top = {}
	for row in X:
		distance = dist(row,x)
		neighbor = ( row[0], [distance, row[6]] )
		top = sorted_add(top, neighbor, k)
	return top

def predict(Xtrain, Xtest, output, prob=False):
	fd = open(output, 'w', newline='')
	writer = csv.writer(fd, delimiter=',')
	writer.writerow(['PassengerId','Survived'])
	for x in Xtest:
		neighbors = nearest_neighbors(Xtrain, x, 5)
		survived = vote(neighbors, prob)
		writer.writerow([x[0], survived])
	fd.close()

def score(Xtrain, Xtest):
	correct = 0
	for x in Xtest:
		neighbors = nearest_neighbors(Xtrain, x, 7)
		survived = vote(neighbors)
		if survived == x[-1]:
			correct += 1
	return float(correct) / float(len(Xtest))

def main():
	Xtrain = build_list("train-prep.csv")
	Xtest = build_list("test-prep.csv")
	predict(Xtrain, Xtest, "prob-knn.csv", True)

if __name__ == "__main__":
	main()