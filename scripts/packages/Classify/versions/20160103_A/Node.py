import numpy
import Leaf

class Node(object):

	def __init__(self, examples = None):
		self.tree = self.grow(examples)
		self.data = None
		self.leaf = False

		#if examples is not None:
		#	self.tree = self.grow(examples)
			#self.data = [e.getLabel() for e in examples]

	def getBestAttribute(self, examples):
		""" get best attribute to split on based on gain ratio """
		attributes 			 = [i for i,e in enumerate(examples[0].getValues())]
		informationGain 	 = [self.getInformationGain(a, examples) for a in attributes]
		intrinsicInformation = [self.getIntrinsicInformation(a, examples) for a in attributes]
		listOfAttributeScores= [self.getGainRatio(informationGain[a], intrinsicInformation[a]) for a in attributes]
		return listOfAttributeScores.index(max(listOfAttributeScores))

	def getEntropy(self, listOfProbabilities):
		""" calculate entropy from list of probabilities """
		""" -sum(p * log2(p)) """
		return -sum([numpy.log2(p)*p for p in listOfProbabilities if p > 0.])

	def getEntropyAfter(self, attribute, examples):
		""" calculate entropy after split on attribute specified """
		""" entropy(labels) * probability of branch """
		classLabelDictionary = dict()

		for example in examples:

			value = example.getValues()[attribute]
			label = example.getLabel()

			if value in classLabelDictionary:
				if label in classLabelDictionary[value]:
					classLabelDictionary[value][label] += 1.
				else:
					classLabelDictionary[value][label]  = 1.
			else:
				classLabelDictionary[value] = {label: 1.}

		probabilities = list()

		for value in classLabelDictionary:
			listOfProbabilities = [l/sum(classLabelDictionary[value].values()) for l in classLabelDictionary[value].values()]
			probabilities.append((self.getEntropy(listOfProbabilities), sum(classLabelDictionary[value].values())/len(examples)))

		return [l*p for l,p in probabilities]

	def getEntropyBefore(self, examples):
		""" calculate entropy before split """
		""" entropy(class labels) """
		classLabelDictionary = dict()

		for example in examples:

			label = example.getLabel()

			if label in classLabelDictionary:
				classLabelDictionary[label] += 1.
			else:
				classLabelDictionary[label]  = 1.

		classLabelLength        = sum(classLabelDictionary.values())
		classLabelProbabilities = [c/classLabelLength for c in classLabelDictionary.values()]

		return self.getEntropy(classLabelProbabilities)

	def getIntrinsicInformation(self, attribute, examples):
		""" calculate intrinsic information of examples after split """
		""" entropy(# of examples in branch) """
		attributeDictionary = dict()

		for example in examples:
			value = example.getValues()[attribute]

			if value in attributeDictionary:
				attributeDictionary[value] += 1.
			else:
				attributeDictionary[value]  = 1.

		totalNumberOfExamples  = sum(attributeDictionary.values())
		attributeProbabilities = [c/totalNumberOfExamples for c in attributeDictionary.values()]
		
		return self.getEntropy(attributeProbabilities)

	def getInformationGain(self, attribute, examples):
		""" calculate information gain: entropy before - sum(entropy after) """
		return self.getEntropyBefore(examples) - sum(self.getEntropyAfter(attribute, examples))

	def getGainRatio(self, informationGain, intrinsicInformation):
		""" calculate gain ratio: information gain / intrinsic information """
		if intrinsicInformation == 0.: return 0.0
		return informationGain/intrinsicInformation

	def splitOnAttribute(self, attribute, examples):
		""" split examples on attribute specified """
		splitExamples = dict()

		for example in examples:
			
			value = example.getValues()[attribute]
			
			if value in splitExamples:
				splitExamples[value].append(example)
			else:
				splitExamples[value] = [example]

		return splitExamples.values()

	def isHomogenous(self, examples, rate = 1):
		""" return true or false based on homogeneity of examples """
		exampleData1 = [e.getLabel() for e in examples]
		exampleData2 = list(set(exampleData1))
		exampleData3 = exampleData1.count(exampleData2[0])
		exampleData4 = len(exampleData1)
		exampleData5 = exampleData3/exampleData4*1.
		print exampleData1, exampleData2, exampleData3, exampleData5
		if len(exampleData2) > 1: return False
		return True

	def grow(self, examples):
		bestAttribute = self.getBestAttribute(examples)
		splitExamples = self.splitOnAttribute(bestAttribute,examples)

		print "Best attribute is {0}.\t{1}".format(bestAttribute, [(e.getValues()[bestAttribute], e.getLabel()) for e in examples])

		leaf = list()
		for branch in splitExamples:
			if self.isHomogenous(branch):
				#print "Yes, class is: {0}".format(branch[0].getLabel())
				self.leaf = True
				leaf.append(Leaf.Leaf(branch))
				#print self.isHomogenous(branch), [b.getLabel() for b in branch]

				#Set data to leaf
			else:
				leaf.append(Node(branch))
				#print self.isHomogenous(branch), [b.getLabel() for b in branch]
				#print leaf
				#print "No", [b.getLabel() for b in branch]#, self.getBestAttribute(branch)
				#ba = self.getBestAttribute(branch)
				#se = self.splitOnAttribute(ba, branch)
				#print "Next best attribute", ba

				#for b in se:
				#	print [bb.getLabel() for bb in b]
					#print self.isHomogenous(b)
		return leaf

if __name__=="__main__":
	import DataSet

	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_weather.gla"
	#f = "/Users/ducrix/Documents/Research/Python/data/ml/test_genders.gla"
	#f = "/Users/ducrix/Documents/Research/Python/data/ml/test_cars.gla"
	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_words.gla"

	ds = DataSet.DataSet(f)
	nd = Node(ds.getExamples())

	#print nd.tree

	for l in nd.tree:
		
		if type(l) == type(nd):
			#print l.tree
			for ll in l.tree:
				print '\t', ll.getLabel()
		else:
			print l.getLabel()

		#if type(l) != type(list()):
		#	print l.getLabel()
		#else:
		#	for ll in l:
		#		print '\t', ll.getLabel()

	#b = nd.getEntropyBefore(ds.getExamples())
	#a = nd.getEntropyAfter(0, ds.getExamples())
	#c = nd.getInformationGain(1, ds.getExamples())
	#d = nd.getIntrinsicInformation(1, ds.getExamples())
	#print c/d
	#print nd.getBestAttribute(ds.getExamples())
	#a = nd.splitOnAttribute(0, ds.getExamples())

	#print nd.isHomogenous(a[2])
	#print nd.grow(ds.getExamples())
