from AttributeSet 	import AttributeSet
from ExampleSet 	import ExampleSet
from Attribute 		import Attribute
from Example 		import Example

class Factory(object):

	def build(self, data = None, attributeSet = None):

		if attributeSet is None:
			# build an attribute set.

			aa = AttributeSet()

			for line in data:
				if line[0] == '@':
					aa.add(Attribute(line[1:].split('\t')))

			return aa

		else:
			# build an example set.

			ee = ExampleSet()

			for line in data:
				if type(line) == type(str()):
					if line[0] == '#':
						ee.add(Example(line[1:], attributeSet))
				elif type(line) == type(ExampleSet()):
					ee.add(line)

			return ee

if __name__ == "__main__":
	fin = open("/Users/ducrix/Documents/Research/Python/data/ml/test_weather.gla", 'r')
	read = [line for line in fin.read().splitlines() if len(line) > 0]
	fin.close()

	f = Factory()

	attributeSet = f.build(read)
	exampleSet 	 = f.build(read, attributeSet)

	print attributeSet.get()
	print exampleSet.getExamples(1)

