import math

class NaiveBayes(object):

	def __init__(self):
		self.data 	  = None
		self.classP   = None
		self.builtFor = None

	def build(self, ds, smoothValue = 0.5):
		""" create dictionary for probabilities for these attributes """
		dictionary = dict()
		attributes = enumerate(ds.getAttributes())
		isNumeric  = ds.isNumeric

		for i,a in attributes:
			dictionary[i] = dict()

			for v in a.getValues():

				if isNumeric(i):
					dictionary[i]    = list()
				else:
					dictionary[i][v] = smoothValue

		#labels = dict()

		#for c in ds.getLabels():
		#	labels.append(c)

		self.data   = dictionary
		#self.classP = labels

	def train(self, ds):
		"""ds = DataSet()"""

		if self.builtFor != ds.getName():
			self.build(ds)
		
		isNumeric  = ds.isNumeric

		d = self.data
		examples = ds.getExample()
		totalLen = len(examples)

		for e in examples:
			print e.getLabel()
			self.classP[e.getLabel()] += 1.

	def test(self):
		pass

	def classify(self):
		pass

if __name__=="__main__":
	import DataSet

	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_weather.gla"
	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_genders.gla"

	ds = DataSet.DataSet(f)
	nb = NaiveBayes()
	ds.getExamples()

	print ds.getExamples()
	nb.build(ds)

	nb.train(ds)