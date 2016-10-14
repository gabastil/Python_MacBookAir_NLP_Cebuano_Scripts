#!usr/bin/env Python
#-*-coding: utf-8 -*-
#
# Name:		ExampleSet.py
# Author:	Glenn Abastillas
# Version:	1.0.0
# Date:		July 2, 2016 (date when comments were added)

import ObjectSet

class ExampleSet(ObjectSet.ObjectSet):

	def __init__(self, examples = None):
		super(ExampleSet, self).__init__()

		if examples is not None: self.data = examples

	def __all_labels(self):
		""" return all labels for example Example object """
		return [e.getLabel() for e in self.data]

	def add(self, example):
		"""	add example object to self.data
			@param	example: Example object to add to set
		"""
		self.data.append(example)

	def get(self, i):
		"""	retrieve specified Example object
			@return Example object
		"""
		if i is None: return self.data
		return self.data[i]

	def getAttribute(self, index):
		""" get a list of attributes at the specified index from all examples
			@param	index: attribute index to return
			@return	List of values from each example at specified index
		"""
		return [example.getValue(index) for example in self.data]

	def getExamples(self, label = None, values = False):
		"""	get all Example objects as list
			@param	label: retrieve just class labels
			@param	values: retrieve just values
			@return List of Example objects
		"""
		# Return the raw self.data variable if nothing is indicated
		if label is None and values == False: return self.data

		# If class label is specified, return Examples matching that class label
		if label is not None:
			examples = [example for example in self.data if example.getLabel() == label]
		
		# If values is set to True, get a list of example values and lables
		if values:
			return [example.getValues()+[example.getLabel()] for example in self.data]

		return examples
		
	# COMMENTED OUT ON 7/13/2016
	#"""	DEPRECATE THIS """
	#def getAllLabels(self):
	#	""" 
	#		*****
	#		REMOVE THIS CLASS ONCE INSTANCES ARE ERASED IN ALL CLASSES USING THIS CLASS 
	#		THIS METHOD IS DEPRECATED. IT IS REPLACED BY __all_labels()
	#		*****
	#	"""
	#	return [e.getLabel() for e in self.data]

	def getLabels(self, asSet=False):
		""" return a list or set of labels
			@param	asSet: True if set of labels desired, False if list desired
			@return	Set if asSet is True; List if asSet is False
		"""
		if asSet:
			return set(self.getAllLabels())
		return self.__all_labels()

	def getCounts(self):
		""" return list of counts of Example objects belonging to each label """
		labels = self.getAllLabels()
		return [labels.count(l) for l in self.getLabels()]

	def getDistribution(self):
		""" return distribution of class labels """
		counts = self.getCounts()
		total  = sum(counts)*1.
		return [count/total for count in counts]

	def unique(self):
		"""	return a set of unique examples """
		examples = [str(e.getValues()) for e in self.data]
		examples = set(examples)
		return len(examples)

	def getRange(self, attribute):
		""" return a tuple with the maximum and minimum values for a specified attribute
			@param	attribute: index of attribute to get values for
			@return	Tuple with values 
		"""
		values = [example.getValue(attribute) for example in self.data]
		return max(values), min(values)

	def toString(self):
		""" return self.data as string 
			@return string of data
		"""
		string = ""

		for example in self.data:
			string += "{}\n".format(example.getValues() + [example.getLabel()])

		return string

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

