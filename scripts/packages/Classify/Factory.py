#!usr/bin/env Python
#-*-coding: utf-8 -*-
#
# Name:		Factory.py
# Author:	Glenn Abastillas
# Version:	1.0.0
# Date:		July 13, 2016 (date when comments were added)

from AttributeSet 	import AttributeSet
from ExampleSet 	import ExampleSet
from Attribute 		import Attribute
from Example 		import Example

class Factory(object):

	def example(self, data = None):
		if type(data)==type(list()):
			e = Example()
			e.data = data[:-1]
			e.label = data[-1]
			return e
		else:
			return Example(data)

	def build(self, data = None, attributeSet = None):
		""" return an AttributeSet or ExampleSet object
			@param	data: input data; raw (textual) attributes or examples
			@param	attributeSet: AttributeSet object required to create ExampleSet objects
			@return	AttributeSet or ExampleSet objects
		"""
		# Build an AttributeSet object from raw (text) attributes.
		if attributeSet is None:
			attributeSet = AttributeSet()

			for line in data:

				# If the line is prefixed with '@', create an Attribute object and add it to the AttributeSet
				if line[0] == '@':
					attributeSet.add(Attribute(line[1:].split('\t')))

			return attributeSet

		# Build an ExampleSet object from raw (text) examples and an AttributeSet.
		else:
			exampleSet = ExampleSet()

			# Loop through the data split by newline
			for line in data:

				# If the line is a string, check it is an example (prefixed by '#')
				if type(line) == type(str()):

					# If the line is an example, create an Example object and add it to the ExampleSet
					if line[0] == '#':
						exampleSet.add(Example(line[1:], attributeSet))

				# Commented out for the time being 7/13/2016
				#else:
				#	exampleSet.add(line)

			return exampleSet

if __name__ == "__main__":
	fin = open("/Users/ducrix/Documents/Research/Python/data/ml/test_weather.gla", 'r')
	read = [line for line in fin.read().splitlines() if len(line) > 0]
	fin.close()

	f = Factory()

	attributeSet = f.build(read)
	exampleSet 	 = f.build(read, attributeSet)

	print attributeSet.get()
	print exampleSet.getExamples(1)

