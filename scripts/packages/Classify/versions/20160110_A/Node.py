import numpy
import Leaf
import ExampleSet
import ObjectSet

class Node(ObjectSet.ObjectSet):

	def __init__(self, examples = None, attributes = None, branchCount = 3):
		super(Node, self).__init__()
		self.data = self.grow(examples, attributes, branchCount)

	def entropy(self, probabilities):
		""" calculate entropy for list of probabilities """
		logResults = [numpy.log2(p)*p for p in probabilities if p > 0.]
		if len(logResults) == 0.: return 0.
		return abs(sum(logResults))

	def entropyA(self, examples):
		""" calculate entropy before split for examples """
		return self.entropy(examples.getDistribution())

	def entropyB(self, examples, attribute, branchCount):
		""" calculate entropy for each branch after split. attribute = (index, attribute) """
		i = attribute[0]
		a = attribute[1]
		n = len(examples)*1.
		d = dict()

		""" get attribute values depending on numeric or nominal attribute """
		if a.isNumeric():
			values = self.getNumericBranches(examples, i, branchCount)
		else:
			values = a.getValues()

		""" set up dictionary for values and labels """
		for v in values:
			d[v] = dict()
			for l in examples.getLabels():
				d[v][l] = 0.

		""" populate dictionary according to values and lables of examples """
		for example in examples:
			v = example[i]
			l = example.getLabel()

			if a.isNumeric():
				for b in sorted(d.keys(), reverse = True):
					if b <= v:
						d[b][l] += 1.
						break
			else:
				d[v][l] += 1.

		""" calculate entropy for all branches """
		c = [d[branch].values() for branch in d]
		c = [self.entropy([v/sum(branch) for v in branch])*(sum(branch)/n) for branch in c if sum(branch) > 0.]
		c = sum(c)
		return c

	def informationGain(self, examples, attribute, branchCount):
		entropyA = self.entropyA(examples)
		entropyB = self.entropyB(examples, attribute, branchCount)
		return entropyA - entropyB

	def intrinsicInformation(self, examples, attribute, branchCount):
		""" attribute = (index, attribute) """
		i = attribute[0]
		a = attribute[1]
		n = len(examples)*1.
		d = dict()

		""" get attribute values depending on numeric or nominal attribute """
		if a.isNumeric():
			values = self.getNumericBranches(examples, i, branchCount)
		else:
			values = a.getValues()

		""" set up dictionary for values and labels """
		for v in values:
			d[v] = 0.

		""" populate dictionary according to values and lables of examples """
		for example in examples:
			v = example[i]

			if a.isNumeric():
				for b in sorted(d.keys(), reverse = True):
					if b <= v:
						d[b] += 1.
						break

			else:
				d[v] += 1.

		""" calculate entropy for all branches """
		branches = [d[branch]/n for branch in d]

		return self.entropy(branches)

	def gainRatio(self, examples, attribute, branchCount):
		informationGain 	 = self.informationGain(examples, attribute, branchCount)
		intrinsicInformation = self.intrinsicInformation(examples, attribute, branchCount)
		return informationGain/intrinsicInformation

	def getNumericBranches(self, examples, attribute, branchCount):
		exampleRange = examples.getRange(attribute)
		branchSlice  = (exampleRange[0] - exampleRange[1])/branchCount
		branchValues = [exampleRange[1] + (branchSlice*(j+1))for j in xrange(branchCount)]
		return branchValues

	def bestAttribute(self, examples, attributes, branchCount):
		attributes = enumerate(attributes.data.values()[:-1])
		scores = list()

		for a in attributes:
			scores.append(self.gainRatio(examples, a, branchCount))

		return scores.index(max(scores))

	def split(self, examples, attributes, best, branchCount):
		attribute = attributes.get(best)

		""" get attribute values depending on numeric or nominal attribute """
		if attribute.isNumeric():
			values = self.getNumericBranches(examples, best, branchCount)
		else:
			values = attribute.getValues()

		splitList = [ExampleSet.ExampleSet() for v in values]

		for example in examples:
			v = example[best]

			if attribute.isNumeric():
				for i, b in enumerate(values):
					if b >= v:
						v = i
						break

			splitList[v].add(example)

		return splitList

	def homogenous(self, examples, threshold = 0.8, limit = 3):
		labels = examples.getAllLabels()
		print "labels", labels

		if len(set(labels)) == 1.: return True

		unique = examples.countUniqueExamples()
		print "unique", unique, examples.getAllLabels(), [e.getValues() for e in examples]

		if unique == 1: return True

		if len(examples) < limit:
			counts = [threshold <= p for p in examples.getDistribution()]
			print "counts", counts, examples.getAllLabels()

			if max(counts): return True

		print "None"
		return False

	def grow(self, examples, attributes, branchCount):
		tree = list()
		append = tree.append

		print examples.getAllLabels()

		isNode = False
		best   = None
		node   = None
		branchValues = None

		if self.homogenous(examples):
			append((isNode, best, Leaf.Leaf(examples), branchValues))
		else:
			best  = self.bestAttribute(examples, attributes, branchCount)
			split = self.split(examples, attributes, best, branchCount)

			if attributes.get(best).isNumeric():
				branchValues = self.getNumericBranches(examples, best, branchCount)

			for e in split:
				print "Attribute: {0}".format(best)
				if len(e) > 0:
					isNode = True
					node   = Node(e, attributes, branchCount)
				
				append((isNode, best, node, branchValues))

		return tree

if __name__=="__main__":
	import DataSet

	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_weather.gla"
	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_genders.gla"
	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_cars.gla"
	#f = "/Users/ducrix/Documents/Research/Python/data/ml/test_words.gla"

	ds = DataSet.DataSet(f)
	#print ds.getExamples().countUniqueExamples()
	nd = Node(ds.examples, ds.attributes)
	#print nd.data[0][2].data[1][2].data[0][2].getLabel()

	def mapNode(node, i = 0):
		#print node[0][2], type(node[0][2]), type(nd)
		for n in node:
			if n[0]:
				if type(n[2]) == type(nd):
					print "{0}`{1}> Attribute {2}".format('\t'*i, '-', n[1])
					mapNode(n[2], i+1)
			else:
				if n[2] is not None:
					n = n[2].getLabel()
				print "{0}`{1}> Leaf {2}".format('\t'*i, '-', n)

	mapNode(nd.data)
