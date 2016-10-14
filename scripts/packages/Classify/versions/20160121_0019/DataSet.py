from Factory import Factory
from ExampleSet import ExampleSet
import random

class DataSet(object):

	def __init__(self, filePath):
		self.name		= None
		self.attributes = None
		self.examples   = None
		
		self.initialize(filePath)

	def convert(self, stringData):
		""" return Example class object from string input """
		return [self.attributes.get(i).getValues(a) for i,a in enumerate(stringData.replace('#', '').split())]

	def getName(self):
		"""	return dataset name """
		return self.name

	def getAttribute(self, i = None):
		"""	return ith attribute """
		return self.attributes.get(i)

	def getAttributes(self):
		"""	return all attributes """
		return self.attributes

	def getValueAttributes(self):
		return [self.attributes[i] for i in range(len(self.attributes))[:-1]]

	def getLabelAttributes(self):
		return self.attributes[-1]

	def getExample(self, i = None):
		""" return ith example """
		return self.examples.get(i)

	def getExamples(self):
		return self.examples

	def getExamplesByClass(self, i = None):
		""" return examples with label i """
		return self.examples.getExamples(i)

	def getExamplesByAttribute(self, a, v, c = 1):
		""" return examples with specified (a) attribute, (v) value, (c) label """
		return [e.getValues() + [e.getLabel()] for e in self.examples if (e.getValues(a) == v) and (e.getLabel() == c)]

	def getLabels(self):
		""" return class labels """
		return self.attributes[-1].getValues()

	def getTrainTestSet(self, percent = .6):
		""" return tuple of testing and training subsets of data with ratio 'percent' """
		if percent > .9: percent = .9
		if percent < .1: percent = .1

		n = int(len(self.examples) * percent)

		trainSet = Factory().build(random.sample(self.examples, n), self.attributes)
		testSet  = Factory().build([example for example in self.examples if example not in trainSet], self.attributes)

		return trainSet, testSet

	def setSeed(self, n = 10):
		""" set seed number for randomizer """
		random.seed(n)

	def initialize(self, filePath):
		""" load data and initialize this class's data: (1) name, (2) attributes, (3) examples """
		fin = open(filePath, 'r')
		read = [line for line in fin.read().splitlines() if len(line) > 0]
		fin.close()

		self.name 		= read[0]
		self.attributes = Factory().build(read)
		self.examples	= Factory().build(read, self.attributes)

	def isNumeric(self, i = None):
		""" return boolean determining if ith attribute is numeric """
		if self.getAttribute(i).getType() in [1, 'n', 'num', 'number', 'numeric']:
			return True
		return False

if __name__ == "__main__":
	from IBk import IBk

	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_weather.gla"

	ds = DataSet(f)
	bk = IBk()

	print ds.getAttributes().toString()
	print ds.getAttribute(1).toString()
	print ds.getExample(1).getValues()
	print ds.getExamples(0)
	print ds.isNumeric(2)
	test, train = ds.getTestTrainSet()

	bk.train(ds, trainAll = False)
	un = ds.convert("6.3 120")
	print "EBA", ds.getExamplesByAttribute(0,1)
	
	#bk.classify(un)



