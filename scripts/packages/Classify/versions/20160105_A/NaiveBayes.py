import numpy

class NaiveBayes(object):

	def __init__(self):
		self.data 	  = None
		self.classP   = None
		self.builtFor = None

	def build(self, ds, smoothValue = 0.1):
		""" create dictionary for probabilities for these attributes """
		dictionary = dict()
		classLabel = ds.getLabels()
		isNumeric  = ds.isNumeric
		labels 	   = [0. for c in ds.getLabels()]

		for c in classLabel:
			dictionary[c] = dict()

			for i,a in enumerate(ds.getAttributes()):
				dictionary[c][i] = dict()

				for v in a.getValues():
					if isNumeric(i): dictionary[c][i]    = list()
					else:			 dictionary[c][i][v] = smoothValue

		self.data   = dictionary
		self.classP = labels

	def probabilityDensity(self, x,m,s):

		part1Numerator   = 1
		part1Denominator = s * (numpy.sqrt(2*numpy.pi))
		part1 			 = part1Numerator/part1Denominator

		part2Numerator   = -(x-m)**2
		part2Denominator = 2 * (s**2)
		part2 			 = numpy.e**(part2Numerator/part2Denominator)

		if part1 == 0.0 or part2 == 0.0: return 0.0

		return -numpy.log2(part1*part2)

	def train(self, ds, examples = None):
		# (1) check if build matches dataset
		if self.builtFor != ds.getName():
			self.build(ds)
		
		# (2) pre-compile stuff
		if examples is None: x = ds.getExamples()
		else:				 x = examples
		n  	  = len(x)
		d 	  = self.data
		isNum = ds.isNumeric

		# (3) get counts for classes and attributes
		for e in x:
			c = e.getLabel()
			self.classP[c] += 1.	

			for i,v in enumerate(e.getValues()):
				if isNum(i):
					d[c][i].append(v)
				else:
					d[c][i][v] += 1.

		# (4) get probabilities for classes and attributes
		for c in d:
			for i in d[c]:
				if isNum(i):
					maximum, minimum = max(d[c][i]), min(d[c][i])
					attributeRange   = maximum - minimum
					attributeValues  = [(v-minimum)/attributeRange for v in d[c][i]]
					attributeMean	 = numpy.mean(attributeValues)
					attributeStdDev  = numpy.std(attributeValues)

					d[c][i] = [attributeMean, attributeStdDev, maximum, minimum]
				else:
					total = sum(d[c][i].values())
					for v in d[c][i]:
						d[c][i][v]   = -numpy.log2(d[c][i][v]/total)

		cp = [p/n for p in self.classP]

		for i,c in enumerate(cp):
			if c == 0.0: cp[i] = 0.0
			else:		 cp[i] = -numpy.log2(c)

		self.classP = cp

	def test(self, listOfExamples):
		results = list()
		append  = results.append

		for x in listOfExamples:
			append(self.classify(x))

		return results

	def classify(self, x):
		
		d = self.data
		l = self.classP

		label  = list()
		append = label.append

		#loop through classes (i)
		for i in xrange(len(l)):
			logScore = l[i]

			#loop through example attributes (j) and values (v)
			for j,v in enumerate(x):

				#numeric variable
				if type(d[i][j]) == type(list()):

					if   v > d[i][j][2]:	v = 1.0
					elif v < d[i][j][3]:	v = 0.0
					else:					v = v - d[i][j][3]
					#print i,j,v, d[i][j]

					p = self.probabilityDensity(v,d[i][j][0], d[i][j][1])

					#update the class score value
					logScore += p

				#nominal variable
				else:
					p = d[i][j][v]

				#update the class score value
				logScore += p

			#update class scores
			append(logScore)

		return label.index(min(label))

if __name__=="__main__":
	import DataSet

	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_weather.gla"
	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_genders.gla"
	#f = "/Users/ducrix/Documents/Research/Python/data/ml/test_cars.gla"

	ds = DataSet.DataSet(f)
	nb = NaiveBayes()
	ds.getExamples()

	#print ds.getExamples()
	nb.build(ds)
	nb.train(ds)

	fn = ds.convert("5.0 110")
	
	print nb.classify(fn)

	nb.train(ds, ds.getTestTrainSet()[1])
	print nb.test(ds.getTestTrainSet()[0])

