import ObjectSet

class ExampleSet(ObjectSet.ObjectSet):

	def __init__(self, examples = None):
		super(ExampleSet, self).__init__()

		if examples is not None: self.data = examples

	def add(self, example):
		self.data.append(example)

	def get(self, i):
		if i is None: return self.data
		return self.data[i]

	def getExamples(self, label = None):
		return [example for example in self.data if example.getLabel() == label]

	def getAllLabels(self):
		return [e.getLabel() for e in self.data]

	def getLabels(self):
		return set(self.getAllLabels())

	def getCounts(self):
		labels = self.getAllLabels()
		return [labels.count(l) for l in self.getLabels()]

	def getDistribution(self):
		c = self.getCounts()
		n = sum(c)*1.
		return [x/n for x in c]

	def unique(self):
		examples = [str(e.getValues()) for e in self.data]
		examples = set(examples)
		return len(examples)

	def getRange(self, attribute):
		values = [example.getValues(attribute) for example in self.data]
		return max(values), min(values)

if __name__=="__main__":
	import Attribute
	import AttributeSet

	a1 = ["att", "n", "this is a test"]
	a2 = ["avd", "n", "this was a test"]
	a3 = ["avs", "c", "this will be a test"]
	a4 = ["kmn", "c", "this could be a test"]

	d1 = Attribute.Attribute(a1)
	d2 = Attribute.Attribute(a2)
	d3 = Attribute.Attribute(a3)
	d4 = Attribute.Attribute(a4)

	aa = AttributeSet.AttributeSet()

	aa.add(d1)
	aa.add(d2)
	aa.add(d3)
	aa.add(d4)

	print aa.get(0).getValues()
