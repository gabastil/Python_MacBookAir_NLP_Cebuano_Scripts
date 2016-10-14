import numpy
import Leaf
import ExampleSet

class Node(object):

	def __init__(self, examples = None, attributes = None):
		self.node = self.grow(examples, attributes)

	def entropy(self, probabilities):
		logResults = [numpy.log2(p)*p for p in probabilities if p > 0.]
		if len(logResults) == 0.: return 0.
		return abs(sum(logResults))

	def entropyA(self, examples):
		return self.entropy(examples.getFrequencies())

	def entropyB(self, examples, attribute):
		""" attribute = (index, attribute) """
		i = attribute[0]
		a = attribute[1]
		n = len(examples)*1.
		d = dict()

		for v in a.getValues():
			d[v] = dict()
			for l in examples.getLabels():
				d[v][l] = 0.

		for example in examples:
			v = example[i]
			l = example.getLabel()
			d[v][l] += 1.

		branchesC = [d[branch].values() for branch in d]
		branchesP = [self.entropy([v/sum(branch) for v in branch])*(sum(branch)/n) for branch in branchesC if sum(branch) > 0.]
		
		return sum(branchesP)

	def informationGain(self, examples, attribute):
		entropyA = self.entropyA(examples)
		entropyB = self.entropyB(examples, attribute)
		return entropyA - entropyB

	def intrinsicInformation(self, examples, attribute):
		""" attribute = (index, attribute) """
		i = attribute[0]
		a = attribute[1]
		n = len(examples)*1.
		d = dict()

		for v in a.getValues():
			d[v] = 0.

		for example in examples:
			v = example[i]
			d[v] += 1.

		branches = [d[branch]/n for branch in d]

		return self.entropy(branches)

	def gainRatio(self, examples, attribute):
		informationGain 	 = self.informationGain(examples, attribute)
		intrinsicInformation = self.intrinsicInformation(examples, attribute)
		return informationGain/intrinsicInformation

	def bestAttribute(self, examples, attributes):
		attributes = enumerate(attributes.attributes.values()[:-1])
		scores = list()

		for a in attributes:
			scores.append(self.gainRatio(examples, a))

		return scores.index(max(scores))

	def split(self, examples, attributes, best):
		attribute = attributes.get(best)
		splitList = [ExampleSet.ExampleSet() for v in attribute.getValues()]

		for example in examples:
			v = example[best]
			splitList[v].add(example)

		return splitList

	def homogenous(self, examples):
		labels = examples.getAllLabels()

		if len(set(labels)) > 1.: return False
		return True

	def grow(self, examples, attributes):
		#best = self.bestAttribute(examples, attributes)
		#split = self.split(examples, attributes, best)
		tree  = list()

		if self.homogenous(examples):
			tree.append(Leaf.Leaf(examples))
		else:
			best  = self.bestAttribute(examples, attributes)
			split = self.split(examples, attributes, best)

		#print "Best Attribute to split on: \'{0}\' named \"{1}\"".format(best, attributes.get(best).getName())
		#print examples.getAllLabels()
		#for examples in split:
		#	print examples.getAllLabels()
		#	if self.homogenous(examples):
		#		tree.append(examples.getLabels())
		#		#return examples.getLabels()
		#	else:
		#		print examples.getLabels()
		#		tree.append(self.grow(examples, attributes))
		#print tree
		return tree

if __name__=="__main__":
	import DataSet

	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_weather.gla"
	#f = "/Users/ducrix/Documents/Research/Python/data/ml/test_genders.gla"
	#f = "/Users/ducrix/Documents/Research/Python/data/ml/test_cars.gla"
	#f = "/Users/ducrix/Documents/Research/Python/data/ml/test_words.gla"

	ds = DataSet.DataSet(f)
	nd = Node(ds.examples, ds.attributes)
	#print nd.entropyA(ds.examples)
	#print nd.entropyB(ds.examples, (1, ds.attributes.get(1)))
	#print nd.informationGain(ds.examples, (0, ds.attributes.get(0)))
	#print nd.intrinsicInformation(ds.examples, (0, ds.attributes.get(0)))
	#print nd.gainRatio(ds.examples, (0, ds.attributes.get(0)))
	#print nd.grow(ds.examples, ds.attributes)

