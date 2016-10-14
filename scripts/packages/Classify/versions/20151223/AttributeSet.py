class AttributeSet(object):

	def __init__(self):
		self.attributes = dict()

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
