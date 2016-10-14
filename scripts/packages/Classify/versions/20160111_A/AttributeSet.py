import ObjectSet

class AttributeSet(ObjectSet.ObjectSet):

	def __init__(self):
		super(AttributeSet, self).__init__()
		self.data = dict()
		self.index = 0

	def __getitem__(self, key):
		return self.data[self.data.keys()[key]]

	def add(self, attribute):
		self.data[len(self.data)] = attribute

	def get(self, i = None):
		if i is None: return self.data
		if type(i) == type(str()):
			i = [a.getName() for a in self.data.values()].index(i)
		return self.data[i]

	def indices(self, includeAll = False):
		if includeAll: return self.data.keys()
		return self.data.keys()[:-1]

	def attributes(self, includeAll = False):
		if includeAll: return self.data.values()
		return self.data.values()[:-1]

	def index(self, name):
		a = [a.getName() for a in self.data.values()].index(i)
		if name in a:
			return a.index(i)
		return None

	def toString(self):
		return '\n'.join([self.data[a].toString() for a in self.data])

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
