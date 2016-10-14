class AttributeSet(object):

	def __init__(self):
		self.attributes = dict()
		self.index 		= 0

	def __getitem__(self, key):
		#print "AttributeSet Class keys", self.attributes.keys()
		return self.attributes[self.attributes.keys()[key]]

	def __len__(self):
		return len(self.attributes)

	def __iter__(self):
		return self

	def next(self):
		try:
			self.index += 1
			return self.attributes[self.index-1]
		except(IndexError, KeyError):
			self.index = 0
			raise StopIteration

	def add(self, attribute):
		self.attributes[len(self.attributes)] = attribute

	def get(self, i = None):
		if i is None: return self.attributes
		if type(i) == type(str()):
			i = [a.getName() for a in self.attributes.values()].index(i)
		return self.attributes[i]

	def index(self, name):
		a = [a.getName() for a in self.attributes.values()].index(i)
		if name in a:
			return a.index(i)
		return None

	def toString(self):
		return '\n'.join([self.attributes[a].toString() for a in self.attributes])

if __name__=="__main__":
	import Attribute

	a1 = ["att", "n", "this is a test"]
	a2 = ["avd", "n", "this was a test"]
	a3 = ["avs", "c", "this will be a test"]
	a4 = ["kmn", "c", "this could be a test"]

	d1 = Attribute.Attribute(a1)
	d2 = Attribute.Attribute(a2)
	d3 = Attribute.Attribute(a3)
	d4 = Attribute.Attribute(a4)

	aa = AttributeSet()

	aa.add(d1)
	aa.add(d2)
	aa.add(d3)
	aa.add(d4)

	print aa.get(0).getValues()

	for a in aa:
		print a
