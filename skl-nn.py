import csv
from sklearn import neural_network

# Set of indices of columns used globally as
# features from prepared data
features = [1,2,3,4,5]

def get_data(filename):
	X = []
	y = []
	with open(filename) as data:
		reader = csv.reader(data, delimiter=',')
		for row in reader:
			if reader.line_num == 1: 
				continue
			xrow = [float(row[x]) for x in features]
			X.append(xrow)
			y.append( float(row[6]) )
	return X,y

def get_test(filename):
	ids = []
	X = []
	with open(filename) as data:
		reader = csv.reader(data, delimiter=',')
		for row in reader:
			if reader.line_num == 1: 
				continue
			ids.append( float(row[0]) )
			X.append([ float(row[x]) for x in features ])
	return ids, X

def train(X,y):
	model = neural_network.MLPClassifier(hidden_layer_sizes=(10,5), 
											activation='relu', solver='adam', 
											learning_rate='adaptive', learning_rate_init=0.0001, 
											max_iter=100000, tol=0.000001)
	model.fit(X,y)
	return model

def publish(ids, yhat, output):
	with open(output,'w',newline='') as fd:
		writer = csv.writer(fd,delimiter=',')
		writer.writerow(['PassengerId', 'Survived'])
		for x in range(len(ids)):
			writer.writerow([ int(ids[x]), int(yhat[x]) ])

def main():
	X, y = get_data('train-prep.csv')
	ids, Xtest = get_test('test-prep.csv')
	model = train(X,y)
	yhat = model.predict(Xtest)
	print(model.score(X,y))
	publish(ids, yhat, './output/prediction-skl.csv')

if __name__ == "__main__":
	main()
