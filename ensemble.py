import csv

def build_list(filename):
	X = []
	with open(filename) as data:
		reader = csv.reader(data, delimiter=',')
		reader.__next__() #skip the first line
		for row in reader:
			X.append( [row[0]] + [float(x) for x in row[1:]] )
	return X

def vote(p1, p2, p3):
	summ = p1 + p2 + p3
	return 1 if (summ/3.0) > 0.5 else 0

def predict(p1, p2, p3, startID, output):
	fd = open(output, 'w', newline='')
	writer = csv.writer(fd, delimiter=',')
	writer.writerow(['PassengerId','Survived'])
	for x in range(len(p1)):
		survived = vote(p1[x][1], p2[x][1], p3[x][1])
		writer.writerow([startID + x, survived])

def main():
	tf = build_list("./output/prediction-tf.csv")
	skl = build_list("./output/prediction-skl.csv")
	knn = build_list("./output/prediction-knn.csv")
	predict(tf, skl, knn, 892, "prediction-ens.csv")

if __name__ == "__main__":
	main()