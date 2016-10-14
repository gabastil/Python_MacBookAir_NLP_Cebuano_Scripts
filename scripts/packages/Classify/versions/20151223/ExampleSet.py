class ExampleSet(object):

	def __init__(self, examples = None):

		self.examples = list()
		self.index    = 0

		if examples is not None: self.examples = examples

	def __getitem__(self, key):
		return self.examples[key]

	def __len__(self):
		return len(self.examples)

	def __iter__(self):
		return self

	def next(self):
		try:
			self.index += 1
			return self.examples[self.index-1]
		except(IndexError):
			self.index = 0
			raise StopIteration

	def add(self, example):
		self.examples.append(example)

	def get(self, i):
		if i is None: return self.examples
		return self.examples[i]

	def getExamples(self, label = None):
		return [example for example in self.examples if example.getLabel() == label]

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
