import numpy
import Leaf
import ExampleSet

class Node(object):

	def __init__(self, examples = None, attributes = None):
		self.node = self.grow(examples, attributes)

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
			exampleRange = examples.getRange(i)
			branchSlice  = (exampleRange[0] - exampleRange[1])/branchCount
			values = [exampleRange[0] - (branchSlice*(j+1))for j in xrange(branchCount)]
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
				#check = [b <= v for b in sorted(d.keys(), reverse = True)]
				#if max(check):
				#	d[b][l] += 1.
			else:
				d[v][l] += 1.

		print d
		branchesC = [d[branch].values() for branch in d]
		branchesP = [self.entropy([v/sum(branch) for v in branch])*(sum(branch)/n) for branch in branchesC if sum(branch) > 0.]
		
		return sum(branchesP)

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

		if a.isNumeric():
			exampleRange = examples.getRange(i)
			branchSlice  = (exampleRange[0] - exampleRange[1])/branchCount
			values = [exampleRange[0] - (branchSlice*(j+1))for j in xrange(branchCount)]
		else:
			values = a.getValues()

		for v in values:
			d[v] = 0.

		for example in examples:
			v = example[i]

			if a.isNumeric():
				check = [b <= v for b in sorted(d.keys(), reverse = True)]
				if max(check):
					d[b] += 1.

			else:
				d[v] += 1.

		branches = [d[branch]/n for branch in d]

		return self.entropy(branches)

	def gainRatio(self, examples, attribute, branchCount):
		informationGain 	 = self.informationGain(examples, attribute, branchCount)
		intrinsicInformation = self.intrinsicInformation(examples, attribute, branchCount)
		return informationGain/intrinsicInformation

	def bestAttribute(self, examples, attributes, branchCount):
		attributes = enumerate(attributes.data.values()[:-1])
		scores = list()

		for a in attributes:
			scores.append(self.gainRatio(examples, a, branchCount))

		return scores.index(max(scores))

	def split(self, examples, attributes, best, branchCount):
		attribute = attributes.get(best)
		splitList = [ExampleSet.ExampleSet() for v in attribute.getValues()]

		for example in examples:
			v = example[best]
			splitList[v].add(example)

		return splitList

	def homogenous(self, examples, threshold = 0.8, limit = 3):
		labels = examples.getAllLabels()
		print "labels", labels

		if len(set(labels)) == 1.: return True

		unique = examples.countUniqueExamples()
		print "unique", unique, examples.getAllLabels()

		if unique == 1: return True

		if len(examples) < limit:
			counts = [threshold <= p for p in examples.getDistribution()]
			print "counts", counts, examples.getAllLabels()

			if max(counts): return True

		#print "None"
		return False

	def grow(self, examples, attributes, branchCount = 3):
		tree = list()
		append = tree.append

		print examples.getAllLabels()

		if self.homogenous(examples):
			append(Leaf.Leaf(examples))
		else:
			best  = self.bestAttribute(examples, attributes, branchCount)
			split = self.split(examples, attributes, best, branchCount)

			for e in split:
				print "Attribute: {0}".format(best)
				append(self.grow(e, attributes, branchCount))

		return tree

if __name__=="__main__":
	import DataSet

	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_weather.gla"
	#f = "/Users/ducrix/Documents/Research/Python/data/ml/test_genders.gla"
	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_cars.gla"
	#f = "/Users/ducrix/Documents/Research/Python/data/ml/test_words.gla"

	ds = DataSet.DataSet(f)
	print ds.getExamples().countUniqueExamples()
	nd = Node(ds.examples, ds.attributes)
	#print nd.entropyA(ds.examples)
	#print nd.entropyB(ds.examples, (1, ds.attributes.get(1)))
	#print nd.informationGain(ds.examples, (0, ds.attributes.get(0)))
	#print nd.intrinsicInformation(ds.examples, (0, ds.attributes.get(0)))
	#print nd.gainRatio(ds.examples, (0, ds.attributes.get(0)))
	#print nd.grow(ds.examples, ds.attributes)

