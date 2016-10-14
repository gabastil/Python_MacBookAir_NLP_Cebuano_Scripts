from Factory import Factory
import random

class DataSet(object):

	def __init__(self, filePath):
		self.name		= None
		self.attributes = None
		self.examples   = None
		
		self.initialize(filePath)

	def convert(self, stringData):
		return Factory().build(stringData, self.attributes)
		#return [self.attributes.get(i).getValue()(s) for i,s in enumerate(stringData.split()) if len(s) > 0]

	def getName(self):
		return self.name

	def getAttribute(self, i = None):
		return self.attributes.get(i)

	def getExample(self, i = None):
		return self.examples.get(i)

	def getExamples(self, i = None):
		return self.examples.getExamples(i)

	def getExamplesByAttribute(self, a, v, c = 1):
		return [e.getValue() + [e.getLabel()] for e in self.examples if (e.getValue(a) == v) and (e.getLabel() == c)]

	def getTestTrainSet(self, percent = .6):
		
		if percent > .9: percent = .9
		if percent < .1: percent = .1

		n = int(len(self.examples) * percent)

		trainSet = random.sample(self.examples, n)
		testSet  = [example for example in self.examples if example not in trainSet]

		return testSet, trainSet

	def initialize(self, filePath):
		fin = open(filePath, 'r')
		read = [line for line in fin.read().splitlines() if len(line) > 0]
		fin.close()

		self.name 		= read[0]
		self.attributes = Factory().build(read)
		self.examples	= Factory().build(read, self.attributes)

	def isNumeric(self, i = None):
		if self.getAttribute(i).getType() in [1, 'n', 'num', 'number', 'numeric']:
			return True
		return False

if __name__ == "__main__":
	from IBk import IBk

	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_weather.gla"

	ds = DataSet(f)
	bk = IBk()

	print ds.getAttribute(1).getName()
	print ds.getExample(1).getValue()
	print ds.getExamples(0)
	print ds.isNumeric(2)
	test, train = ds.getTestTrainSet()

	bk.train(ds, trainAll = False)
	un = ds.convert("6.3 120")
	print "EBA", ds.getExamplesByAttribute(0,1)
	
	#bk.classify(un)



