#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# Glenn Abastillas
# December 16, 2015
# Distance.py
#
# Updates: 06/24/2016	Added __iter__ and next methods

from Factory import Factory
from ExampleSet import ExampleSet
import random

class DataSet(object):

	def __init__(self, filePath=None):
		self.name		= None
		self.attributes = None
		self.examples   = ExampleSet()

		self.iteration_index = 0
		
		if filePath is not None:
			self.initialize(filePath)

	def __iter__(self):
		""" allow for iteration over the examples """
		return self

	def next(self):
		""" get next item in iteration
			@return	Example object
		"""
		try:
			self.iteration_index += 1
			return self.examples[self.iteration_index-1]
		except(IndexError):
			self.iteration_index = 0
			raise StopIteration

	def addAttribute(self, attribute):
		""" add attribute to attributes """
		self.attributes.add(attribute)

	def addExample(self, example):
		""" add example object to examples """
		self.examples.add(example)

	def convert(self, stringData):
		""" return Example class object from string input """
		return [self.attributes.get(i).getValues(a) for i,a in enumerate(stringData.replace('#', '').split())]

	def getName(self):
		"""	return dataset name """
		return self.name

	def getAttribute(self, i = None):
		"""	return ith attribute """
		return self.attributes.get(i)

	def getAttributes(self):
		"""	return all attributes """
		return self.attributes

	def getValueAttributes(self):
		""" """
		return [self.attributes[i] for i in range(len(self.attributes))[:-1]]

	def getLabelAttributes(self):
		""" """
		return self.attributes[-1]

	def getExample(self, i = None):
		""" return ith example """
		return self.examples.get(i)

	def getExamples(self):
		return self.examples

	def getExamplesByClass(self, i = None):
		""" return examples with label i """
		return ExampleSet(self.examples.getExamples(i))

	def getExamplesByAttribute(self, a, v, c = 1):
		""" return examples with specified (a) attribute, (v) value, (c) label """
		return [e.getValues() + [e.getLabel()] for e in self.examples if (e.getValue(a) == v) and (e.getLabel() == c)]

	def getLabels(self):
		""" return class labels """
		return self.attributes[-1].getValues()

	def getTrainTestSet(self, percent = .6):
		""" return tuple of testing and training subsets of data with ratio 'percent' """
		if percent > .9: percent = .9
		if percent < .1: percent = .1

		n = int(len(self.examples) * percent)

		trainSet = Factory().build(random.sample(self.examples, n), self.attributes)
		testSet  = Factory().build([example for example in self.examples if example not in trainSet], self.attributes)

		return trainSet, testSet

	def setSeed(self, n = 10):
		""" set seed number for randomizer """
		random.seed(n)

	def initialize(self, filePath):
		""" load data and initialize this class's data: (1) name, (2) attributes, (3) examples """
		fin = open(filePath, 'r')
		read = [line for line in fin.read().splitlines() if len(line) > 0]
		fin.close()

		self.name 		= read[0]
		self.attributes = Factory().build(read)
		self.examples	= Factory().build(read, self.attributes)

	def isNumeric(self, i = None):
		""" return boolean determining if ith attribute is numeric """
		if self.getAttribute(i).getType() in [1, 'n', 'num', 'number', 'numeric']:
			return True
		return False

if __name__ == "__main__":
	from IBk import IBk

	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_weather.gla"

	ds = DataSet(f)

	e1 = Factory().example([1,2,1])
	ds.addExample(e1)
	print ds.examples[-1].getValues()
	print ds.examples[-1].getLabel()
	print ds.getExamples().getAttribute(0)
	
	print "--\n"
	
	for example in ds.getExamples():
		print example.data
	"""
	bk = IBk()

	print ds.getAttributes().toString()
	print ds.getAttribute(1).toString()
	print ds.getExample(0).getValues()
	print ds.getExample(0).getLabel()
	print ds.isNumeric(2)
	fact = Factory().example([3,2,4,1])
	test, train = ds.getTrainTestSet()


	bk.train(ds, trainAll = False)
	un = ds.convert("6.3 120")
	print "EBA", ds.getExamplesByAttribute(0,1)
	
	#bk.classify(un)
	"""


