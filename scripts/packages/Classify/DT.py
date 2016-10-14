import numpy 
import ObjectSet
import Node

class DT(ObjectSet.ObjectSet):

	def __init__(self, examples = None, attributes = None, branches = 3):
		super(DT, self).__init__()
		if examples != None and attributes != None:

			if branches < 2: branches = 2
			self.data = self.train(examples, attributes, branches)

	def train(self, examples, attributes, branches):
		return Node.Node(examples, attributes, branches)

	def test(self, examples, includeExampleLabel = True):
		output = list()
		for example in examples:
			if includeExampleLabel:
				output.append((self.classify(example), example.getLabel()))
			else:
				output.append(self.classify(example))

		return output
	def getBranch(self, value, branches):
		for branch in branches:
			if branch >= value:
				return branches.index(branch)

		if value > branches[-1]: return branches.index(branches[-1])

	def classify(self, example, node = None):
		if node is None: node = self.data

		isNode = node[0][0]
		bestAt = node[0][1]
		nodeAt = node[0][2]
		branch = node[0][3]
		isNum  = node[0][3] != None
		
		if isNode:
			value = example[bestAt]

			if isNum:
				value = self.getBranch(value, branch)

			return self.classify(example, nodeAt)

		else:
			if nodeAt is not None: return nodeAt.getLabel()
			return None


if __name__=="__main__":
	import DataSet

	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_weather.gla"
	#f = "/Users/ducrix/Documents/Research/Python/data/ml/test_genders.gla"
	#f = "/Users/ducrix/Documents/Research/Python/data/ml/test_cars.gla"
	#f = "/Users/ducrix/Documents/Research/Python/data/ml/test_words.gla"

	ds = DataSet.DataSet(f)

	train, test = ds.getTrainTestSet(.1)

	dt = DT(train, ds.getAttributes(), 2)
	#print dt.data[:]
	#print dt.classify(test[0])
	t = dt.test(test)
	p = [tt[0]==tt[1] for tt in t]
	print p, t
	print (1.*p.count(True))/len(p)
	#print len(train), [t.getValues() for t in train]
	#print len(test), [t.getValues() for t in test]
