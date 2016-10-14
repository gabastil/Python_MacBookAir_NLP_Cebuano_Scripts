import numpy

class NaiveBayes(object):

	def __init__(self):
		self.data 	  = None
		self.classP   = None
		self.builtFor = None

	def build(self, ds, smoothValue = 0.1):
		""" create dictionary for probabilities for these attributes """
		dictionary = dict()
		#attributes = enumerate(ds.getAttributes())
		classLabel = ds.getLabels()
		isNumeric  = ds.isNumeric

		#print [(i,a) for i,a in attributes]

		for c in classLabel:
			dictionary[c] = dict()

			for i,a in enumerate(ds.getAttributes()):
				dictionary[c][i] = dict()

				for v in a.getValues():

					if isNumeric(i):
						dictionary[c][i]    = list()
					else:
						dictionary[c][i][v] = smoothValue

		labels = list()

		for c in ds.getLabels():
			labels.append(0.)

		self.data   = dictionary
		self.classP = labels
		#self.classP = labels
		#print "Data", self.data

	def probabilityDensity(self, x,m,s):

		return -numpy.log2((1/(s * (numpy.sqrt(2*numpy.pi))))*(numpy.e**(-((x-m)**2)/(2*(s**2)))))

	def train(self, ds):
		"""ds = DataSet()"""

		# (1) check if build matches dataset
		if self.builtFor != ds.getName():
			self.build(ds)
		
		# (2) pre-compile stuff
		x  	  = ds.getExample()
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
					#print attributeMean, attributeStdDev
					#print "A MEAN", attributeMean, attributeValues
					d[c][i] = [attributeMean, attributeStdDev, maximum, minimum]
				else:
					total = sum(d[c][i].values())
					for v in d[c][i]:
						d[c][i][v]   = -numpy.log2(d[c][i][v]/total)

		# (5) get (log) probabilities for class probabilities
		#print self.classP
		#print d

		cp = [p/n for p in self.classP]
		#print cp

		for i,c in enumerate(cp):
			if c == 0.0: cp[i] = 0.0
			else:		 cp[i] = -numpy.log2(c)

		self.classP = cp
		#print cp
		#print d
		#print "classP", self.classP
		#print "data", self.data

	def test(self):
		pass

	def classify(self, x):
		
		d = self.data
		l = self.classP

		label = list()

		#print "Befor: \t{0}".format(l)
		for i,c in enumerate(l):
			label.append(l[i])
			#print label

			for j,v in enumerate(x):

				#- if numeric variable -
				if type(d[i][j]) == type(list()):
					if v < d[i][j][3]:
						v = 0.0
					elif v > d[i][j][2]:
						v = 1.0
					else:
						v = v - d[i][j][3]

					p = self.probabilityDensity(v,d[i][j][0], d[i][j][1])
					#print "classify()", p
					label[i] = label[i] + p

				else:
					p = d[i][j][v]

				label[i] = label[i] + p

		#print "After: \t{0}".format(label)
		return label.index(min(label))

if __name__=="__main__":
	import DataSet

	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_weather.gla"
	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_genders.gla"
	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_cars.gla"

	ds = DataSet.DataSet(f)
	nb = NaiveBayes()
	ds.getExamples()

	#print ds.getExamples()
	nb.build(ds)
	nb.train(ds)

	fn = ds.convert("#.5 4 2")
	
	print nb.classify(fn)

