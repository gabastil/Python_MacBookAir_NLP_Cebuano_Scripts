#!usr/bin/env Python
#-*-coding: utf-8 -*-
#
# Name:		Example.py
# Author:	Glenn Abastillas
# Version:	1.0.0
# Date:		July 11, 2016 (date when comments were added)

import ObjectSet

class Example(ObjectSet.ObjectSet):

	def __init__(self, data=None, attributeSet=None):
		super(Example, self).__init__()

		self.label 	= None
		if data is not None:
			self.__initialize(data, attributeSet)

	def __len__(self):
		return len(self.data) + 1

	def __initialize(self, data, attributeSet):
		""" initialize this object 
			@param	data: input data to turn into an Example
			@param	attributeSet: AttributeSet object that describes features
		"""
		example = [attributeSet.get(i).getValues(x) for i,x in enumerate(data.split()) if len(x) > 0]

		self.data = example[:-1]
		self.label  = example[-1]

	def getValue(self, index):
		""" return example's value at specified index 
			@param	index: example value's index
			@return	integer or float value
		"""
		try:
			return self.data[index]
		except(IndexError, KeyError):
			raise IndexError("Index is out of range.")

	def getData(self, label=True):
		""" return example's data and label 
			@param	label: include label in list return
			@return	list of values
		"""
		if label == True:
			return self.data + [self.label]
		return self.data

	""" 
		****
		REMOVE 'v' PARAMETER ONCE 
		ALL INSTANCES OF THIS METHOD 
		HAVE BEEN REPLACED BY 'getValue' 
		****

		REMOVED on 07/13/2016 -- remove this comment in about 1 month
	"""
	#def getValues(self, v = None):
	def getValues(self):
		""" return example's values """
		return self.data

	def getLabel(self):
		""" return example's label """
		return self.label

	def setData(self, data):
		""" set the self.data variable to user specified data """
		self.data = data

	def toString(self):
		""" return Example object as a string """
		return "{} {}".format(self.data, self.label)		

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

	#print aa.toString()
	print aa.get(0).toString()
	print aa.get(0).getValues("sunny")

	e1 = "sunny some evening"
	e2 = "rainy many morning"
	e3 = "windy none morning"

	x1 = Example(e1, aa)

	print x1.getLabel()
	print x1.getValues()
