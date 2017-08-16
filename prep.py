import csv

def prepTrainer(filename):
	with open(filename + '.csv') as data:
		newfile = open(filename + '-prep.csv', 'w', newline='')
		writer = csv.writer(newfile, delimiter=',')
		reader = csv.reader(data, delimiter=',')
		for row in reader:
			if reader.line_num == 1:
				writer.writerow(['Id','Class','IsMale','Sibsp','Parch','Survived'])
				continue
			row[4] = '1' if (row[4] == 'male') else '0'
			elems = [0,2,4,6,7,1]
			newrow = [row[x] for x in elems]
			writer.writerow(newrow)
		newfile.close()

def prepTester(filename):
	with open(filename + '.csv') as data:
		newfile = open(filename + '-prep.csv', 'w', newline='')
		writer = csv.writer(newfile, delimiter=',')
		reader = csv.reader(data, delimiter=',')
		for row in reader:
			if reader.line_num == 1:
				writer.writerow(['ID','Class','IsMale','Sibsp','Parch'])
				continue
			row[3] = '1' if (row[3] == 'male') else '0'
			elems = [0,1,3,5,6]
			newrow = [row[x] for x in elems]
			writer.writerow(newrow)
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
	prepTrainer('train')

if __name__ == "__main__":
	main()