import ObjectSet

class Attribute(ObjectSet.ObjectSet):

	def __init__(self, data):
		super(Attribute, self).__init__()
		self.name 		= None
		self.dataType 	= None
		self.labels		= None
		self.initialize(data)

	def getName(self):
		""" return attribute's name """
		return self.name

	def setName(self, name):
		""" set attribute's name """
		self.name = name

	def getType(self):
		""" return attribute's type """
		return self.dataType

	def getValues(self, name = None):
		""" return Values indicated by name """

		if name is None: 
			return self.data
		
		if self.dataType in [1, 'n', 'num', 'number', 'numeric']: 
			return float(name)
		
		i = self.labels.index(name)
		return self.data[i]

	def getLabels(self, i = None):
		""" return attribute's label """
		if i is None: return self.labels
		return self.labels[i]

	def initialize(self, data):
		""" return tialize indicated by  """
		self.name 		= data[0]
		self.dataType 	= data[-2]

		dataValues = ((a,b) for a, b in enumerate(data[-1].split()))

		values = list()
		labels = list()

		for a, b in dataValues:
			values.append(a)
			labels.append(b)

		self.labels 	= labels
		self.data		= values

	def isNumeric(self):
		if self.dataType in [1, 'n', 'num', 'number', 'numeric']: return True
		return False

	def toString(self):
		""" return attribute as string """
		return "@{0}".format('\t'.join([self.name] + [self.dataType] + self.labels))
