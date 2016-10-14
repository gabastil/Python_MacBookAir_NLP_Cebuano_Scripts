class Attribute(object):

	def __init__(self, data):
		self.name 		= None
		self.dataType 	= None
		self.values		= None
		self.labels		= None
		self.index 		= 0
		self.initialize(data)

	def __getitem__(self, key):
		return self.values[key]

	def __len__(self):
		return len(self.values)+1

	def __iter__(self):
		return self

	def next(self):
		try:
			self.index += 1
			return self.values[self.index-1]
		except(IndexError):
			self.index = 0
			raise StopIteration

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
			return self.values
		
		if self.dataType in [1, 'n', 'num', 'number', 'numeric']: 
			return float(name)
		
		i = self.labels.index(name)
		return self.values[i]

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
		self.values		= values

	def toString(self):
		""" return attribute as string """
		return "@{0}".format('\t'.join([self.name] + [self.dataType] + self.labels))
