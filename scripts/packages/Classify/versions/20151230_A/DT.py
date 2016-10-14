import numpy 

class DT(object):

	def __init__(self):
		self.tree = None
		pass

	def OLDgetBestAttribute(self, listOfExamples, listOfClassLabels):
		listOfExamplesLength    = len(listOfExamples)
		classLabelProbabilities = list()

		for classLabel in listOfClassLabels:
			thisCount = 0.

			for example in listOfExamples:

				if example.getLabel() == classLabel:
					thisCount += 1

			classLabelProbabilities.append(thisCount/listOfExamplesLength)

		entropyBefore = self.entropy(classLabelProbabilities)
		#print classLabelProbabilities, entropyBefore

		attributeIndices = xrange(len(listOfExamples[0].getValues()))

		for i in attributeIndices:
			pass



	def getBestAttribute(self, ds, examples, attributes, classLabels):
		#attributes  = ds.getValueAttributes()
		#classLabels = ds.getLabelAttributes().getValues()
		sizeOfExamples = 1. * len(examples)

		# (1) Get entropy before split.
		classProbs  = list()
		
		for c in classLabels:
			classProbs.append(len(ds.getExamplesByClass(c))/sizeOfExamples)

		entropyA 	= self.entropy(classProbs)

		# (2) Get entropy after split.
		bestAttributeEntropy = list()

		for j,a in enumerate(attributes):
			splitProbs = list()

			for v in a:
				valueProbs = list()

				for i,p in enumerate(classProbs):
					valueProbs.append(len(ds.getExamplesByAttribute(j,v,i)))

				sumValueProbs  = sum(valueProbs)
				frqValueProbs  = [v/t for v in valueProbs]
				thisValueProbs = (sumValueProbs/t)*self.entropy(frqValueProbs)
				splitProbs.append(thisValueProbs)

			bestAttributeEntropy.append(entropyA - sum(splitProbs))
		bestAttribute = bestAttributeEntropy.index(max(bestAttributeEntropy))

		return bestAttribute

	def grow(self, ds):
		attributes  = ds.getValueAttributes()
		classLabels = ds.getLabelAttributes().getValues()

		# (1) Get entropy before split.
		classProbs  = list()
		t           = float(len(ds.getExamples()))

		for c in classLabels:
			classProbs.append(len(ds.getExamplesByClass(c))/t)

		entropyA 	= self.entropy(classProbs)
		print "Entropy before: %0.2f" % entropyA

		# (2) Get entropy after split.
		bestAttributeEntropy = list()

		for j,a in enumerate(attributes):
			splitProbs = list()

			for v in a:
				valueProbs = list()

				for i,p in enumerate(classProbs):
					valueProbs.append(len(ds.getExamplesByAttribute(j,v,i)))

				sumValueProbs  = sum(valueProbs)
				frqValueProbs  = [v/t for v in valueProbs]
				thisValueProbs = (sumValueProbs/t)*self.entropy(frqValueProbs)

				splitProbs.append(thisValueProbs)

			bestAttributeEntropy.append(entropyA - sum(splitProbs))

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
	dt.getBestAttribute(ds, ds.getExamples(), ds.getAttributes(), ds.getLabelAttributes().getValues())