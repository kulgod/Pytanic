import csv

def extract_features(row, sex_index, age_index):
	row[sex_index] = '1' if (row[sex_index] == 'female') else '0'
	age = row[age_index]
	row[age_index] = '1' if (age and float(age) < 16) else '0'
	return row
 
def prepTrainer(filename):
	with open(filename + '.csv') as data:
		newfile = open(filename + '-prep.csv', 'w', newline='')
		writer = csv.writer(newfile, delimiter=',')
		reader = csv.reader(data, delimiter=',')
		elems = [0,2,4,5,6,7,1]
		for row in reader:
			if reader.line_num == 1:
				writer.writerow(['Id','Class','Female','Child','Sibsp','Parch','Survived'])
				continue
			row = extract_features(row,4,5)
			writer.writerow([row[x] for x in elems])
		newfile.close()

def prepTester(filename):
	with open(filename + '.csv') as data:
		newfile = open(filename + '-prep.csv', 'w', newline='')
		writer = csv.writer(newfile, delimiter=',')
		reader = csv.reader(data, delimiter=',')
		elems = [0,1,3,4,5,6]
		for row in reader:
			if reader.line_num == 1:
				writer.writerow(['ID','Class','Female','Child','Sibsp','Parch'])
				continue
			row = extract_features(row,3,4)
			writer.writerow([row[x] for x in elems])
		newfile.close()

def getStats(filename):
	with open(filename + '.csv') as data:
		reader = csv.reader(data, delimiter=',')
		counts = []
		rowlen = 0
		n = 0
		for row in reader:
			if reader.line_num == 1:
				rowlen = len(row)
				counts = [0 for _ in range(rowlen)]
				continue
			for x in range(rowlen):
				if row[x]:
					counts[x] += 1
			n += 1
		print([x/n for x in counts])

def main():
	prepTester('test')

if __name__ == "__main__":
	main()