import ObjectSet

class Example(ObjectSet.ObjectSet):

	def __init__(self, data, attributeSet):
		super(Example, self).__init__()

		self.label 	= None
		self.initialize(data, attributeSet)

	def __len__(self):
		return len(self.data) + 1

	def getValues(self, v = None):
		""" return example's values """
		if v == None: 	return self.data
		else:			return self.data[v]

	def getLabel(self):
		""" return example's label """
		return self.label

	def initialize(self, data, attributeSet):
		example = [attributeSet.get(i).getValues(x) for i,x in enumerate(data.split()) if len(x) > 0]

		self.data = example[:-1]
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
