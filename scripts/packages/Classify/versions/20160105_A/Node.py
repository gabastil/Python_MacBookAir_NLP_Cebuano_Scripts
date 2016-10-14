import numpy
import Leaf

class Node(object):

	def __init__(self, attributes = None, examples = None):
		pass

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
		print branchesC
		branchesP = [self.entropy([v/sum(branch) for v in branch])*(sum(branch)/n) for branch in branchesC if sum(branch) > 0.]
		print branchesP
		return sum(branchesP)
		#probabilities = [[v/sum(branch) for v in branch] for branch in branches if sum(branch) > 0.0]
		#entropies 	  = [self.entropy(branch)*branch for branch in probabilities if branch > 0.0]

		#return sum(entropies)

	def informationGain(self, examples, attribute):
		entropyA = self.entropyA(examples)
		entropyB = self.entropyB(examples, attribute)
		return entropyA - entropyB

	#def intrinsicInformation(self, examples, attribute):

	#def gainRatio(self, example, attributes):

if __name__=="__main__":
	import DataSet

	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_weather.gla"
	#f = "/Users/ducrix/Documents/Research/Python/data/ml/test_genders.gla"
	#f = "/Users/ducrix/Documents/Research/Python/data/ml/test_cars.gla"
	#f = "/Users/ducrix/Documents/Research/Python/data/ml/test_words.gla"

	ds = DataSet.DataSet(f)
	nd = Node(ds.getAttributes(), ds.getExamples())
	#print nd.entropyA(ds.examples)
	#print nd.entropyB(ds.examples, (1, ds.attributes.get(1)))
	print nd.informationGain(ds.examples, (0, ds.attributes.get(0)))

