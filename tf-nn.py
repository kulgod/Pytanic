import tensorflow as tf
import numpy as np
import queue
import csv

# Used as a callback by DNNClassifier to get input data
# Returns a feature and target array, as Tensor objects
# ---------------------------------------------------------
def train_input_fn():
	X = []
	y = []
	with open("train-prep.csv") as data:
		reader = csv.reader(data, delimiter=',')
		for row in reader:
			if reader.line_num == 1: #skip the header
				continue
			y.append([ float(row[5]) ])
			X.append([ float(row[x]) for x in range(1,5) ])
	return tf.constant(X), tf.constant(y)

# Used as a callback by DNNClassifier to get input data
# Returns a feature array as the input for prediction
# ---------------------------------------------------------
def test_input_fn():
	X = []
	with open("test-prep.csv") as data:
		reader = csv.reader(data, delimiter=',')
		for row in reader:
			if reader.line_num == 1: #skip the header
				continue
			X.append([ float(row[x]) for x in range(1,5) ])
	return np.array(X, dtype=np.float32)

# Writes the predicted outputs to a new file in the format
# expected by the Titanic competition 
# Assumes same order of IDs as input file, starting at 892
# ---------------------------------------------------------
def publish(prediction):
	with open('prediction-tf.csv','w',newline='') as data:
		writer = csv.writer(data, delimiter=',')
		writer.writerow(['PassengerId','Survived'])
		i = 892
		for p in prediction:
			writer.writerow([i,p])
			i += 1

# Creates a 4-layered Neural Network using 4 features 
# from the Titanic dataset. Stores checkpoint files in 
# "tmp" folder, which may need to be deleted between runs
# if the Classifier parameters are changed
# ---------------------------------------------------------
def main():
	feature_columns = [tf.contrib.layers.real_valued_column("", dimension=4)]
	model = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
										hidden_units=[10,5],
										n_classes=2,
										model_dir="./tmp/")

	model.fit(input_fn=train_input_fn, steps=10000)
	predictions = list(model.predict_classes(input_fn=test_input_fn))
	publish(predictions)

if __name__ == "__main__":
	main()