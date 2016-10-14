class Attribute(object):

	def __init__(self, data):
		self.name 		= None
		self.dataType 	= None
		self.values		= None
		self.labels		= None
		self.initialize(data)

	def getName(self):
		return self.name

	def setName(self, name):
		self.name = name

	def getType(self):
		return self.dataType

	def getValues(self, name = None):
		if name is None: return self.values
		if self.dataType in [1, 'n', 'num', 'number', 'numeric']: return float(name)
		i = self.labels.index(name)
		return self.values[i]

	def getLabels(self, i = None):
		if i is None: return self.labels
		return self.labels[i]

	def initialize(self, data):
		self.name 		= data[0]
		self.dataType 	= data[-2]

		dataValues = ((a,b) for a, b in enumerate(data[-1].split()))

		values = list()
		labels = list()

		for a, b in dataValues:
			values.append(a)
			labels.append(b)

		self.labels 	= labels
		self.values		= values


