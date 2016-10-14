import numpy 

class DT(object):

	def __init__(self):
		self.tree = None
		pass

	def splitOnAttribute(self, attributeToSplit, examples):
		pass
		
	def getBestAttribute(self, ds, examples, attributes, labels):
		sizeOfExamples 	   = 1. * len(examples)

		# (1) Get entropy before split.
		classProbabilities = list()
		getExamplesByClass = ds.getExamplesByClass
		
		for c in labels:
			classProbabilities.append(len(getExamplesByClass(c))/sizeOfExamples)

		entropyBeforeSplit = self.entropy(classProbabilities)

		# (2) Get entropy after split.
		bestAttributeEntropy   = list()
		getExamplesByAttribute = ds.getExamplesByAttribute

		for j,a in enumerate(attributes):
			attributeSplitProbabilities = list()

			for v in a:
				attributeValueProbabilities = list()

				for i,p in enumerate(classProbabilities):
					attributeValueProbabilities.append(len(getExamplesByAttribute(j,v,i)))

				attributeValueProbabilitiesSum  = sum(attributeValueProbabilities)
				attributeValueProbabilitiesFreq = [value/sizeOfExamples for value in attributeValueProbabilities]
				attributeValueProbabilitiesThis = (attributeValueProbabilitiesSum/sizeOfExamples)*self.entropy(attributeValueProbabilitiesFreq)
				attributeSplitProbabilities.append(attributeValueProbabilitiesThis)

			bestAttributeEntropy.append(entropyBeforeSplit - sum(attributeSplitProbabilities))

		bestAttribute = bestAttributeEntropy.index(max(bestAttributeEntropy))

		return bestAttribute

	def grow(self, ds):
		attributes  = ds.getValueAttributes()
		labels = ds.getLabelAttributes().getValues()

		# (1) Get entropy before split.
		classProbabilities  = list()
		t           = float(len(ds.getExamples()))

		for c in labels:
			classProbabilities.append(len(ds.getExamplesByClass(c))/t)

		entropyBeforeSplit 	= self.entropy(classProbabilities)
		print "Entropy before: %0.2f" % entropyBeforeSplit

		# (2) Get entropy after split.
		bestAttributeEntropy = list()

		for j,a in enumerate(attributes):
			attributeSplitProbabilities = list()

			for v in a:
				attributeValueProbabilities = list()

				for i,p in enumerate(classProbabilities):
					attributeValueProbabilities.append(len(ds.getExamplesByAttribute(j,v,i)))

				attributeValueProbabilitiesSum  = sum(attributeValueProbabilities)
				attributeValueProbabilitiesFreq  = [v/t for v in attributeValueProbabilities]
				attributeValueProbabilitiesThis = (attributeValueProbabilitiesSum/t)*self.entropy(attributeValueProbabilitiesFreq)

				attributeSplitProbabilities.append(attributeValueProbabilitiesThis)

			bestAttributeEntropy.append(entropyBeforeSplit - sum(attributeSplitProbabilities))

		bestAttribute = bestAttributeEntropy.index(max(bestAttributeEntropy))
		print bestAttribute

	def test(self):
		pass

	def classify(self):
		pass

	def entropy(self, listOfValues):
		if 0.0 in listOfValues: return 0.0
		return -sum([v*numpy.log2(v) for v in listOfValues])

if __name__=="__main__":
	import DataSet

	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_weather.gla"
	#f = "/Users/ducrix/Documents/Research/Python/data/ml/test_genders.gla"
	#f = "/Users/ducrix/Documents/Research/Python/data/ml/test_cars.gla"

	ds = DataSet.DataSet(f)
	dt = DT()

	#dt.grow(ds)
	print dt.getBestAttribute(ds, ds.getExamples(), ds.getValueAttributes(), ds.getLabelAttributes().getValues())