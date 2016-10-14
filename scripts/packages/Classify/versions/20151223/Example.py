class Example(object):

	def __init__(self, data, attributeSet):
		self.values	= None
		self.label 	= None
		self.initialize(data, attributeSet)

	def getValue(self, v = None):
		if v == None: 	return self.values
		else:			return self.values[v]

	def getLabel(self):
		return self.label

	def initialize(self, data, attributeSet):
		example = [attributeSet.get(i).getValues(x) for i,x in enumerate(data.split()) if len(x) > 0]

		self.values = example[:-1]
		self.label  = example[-1]			

if __name__=="__main__":
	from AttributeSet import AttributeSet
	from Attribute import Attribute


	a1 = ["weather", "n", "sunny rainy windy"]
	a2 = ["people", "n", "none some many"]
	a3 = ["time", "n", "morning afternoon evening"]

	d1 = Attribute(a1)
	d2 = Attribute(a2)
	d3 = Attribute(a3)

	aa = AttributeSet()

	aa.add(d1)
	aa.add(d2)
	aa.add(d3)

	e1 = "sunny some evening"
	e2 = "rainy many morning"
	e3 = "windy none morning"

	x1 = Example(e1, aa)

	print x1.getLabel()
	print x1.getValues()
