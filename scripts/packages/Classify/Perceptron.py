#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# Glenn Abastillas
# June 24, 2016
# Perceptron.py

import math
from Distance import Distance
from DataSet import DataSet
from Factory import Factory
import numpy as np

class Perceptron(object):

	def __init__(self, rate=.01, epochs=None, dataset=None):
		""" initialize Perceptron object
			@param	dataset: DataSet object
			@param	rate: learning rate (typically < 1.0)
			@param	epochs: maximum iterations if training is not converging
		"""

		self.weights = [0. for value in dataset.getExample(0).getValues()] + [0.]
		self.rate 	 = rate
		self.epochs  = epochs

		self.error = 0

		#print "Testing class variables:\t {}, {}, {}".format(self.weights, self.rate, self.epochs)
		#print "Training test:"

		if dataset is not None:
			self.train(dataset.getExamples(), rate, epochs)
		#self.test(dataset.getExamples())
		#self.__normalize(dataset)

	def __evaluate(self, estimated, actual):
		""" return True if estimated class equals actual class 
			@param	estimated: predicted class label
			@param	actual: actual example class label
			@return	True or False
		"""
		return estimated == actual

	def __dot(self, array1, array2):
		""" return dot product of two arrays
			@param	array1: first array as list of values
			@param	array2: second array as list of values
			@return	scalar float
		"""
		maxLength 	= max([len(array1), len(array2)])
		sumProducts = (array1[i]*array2[i] for i in xrange(maxLength))

		return sum(sumProducts)

	def __normalize(self, dataset):
		print dataset.getAttributes()
		print dataset.getExamples()

	def __sign(self, value, threshold=0.):
		""" return sign if value greater or less than threshold
			@param	value: integer or float number to evaluate
			@param	threshold: threshold value determining what integer to return
			@return integer
		"""
		if value >= threshold:
			return 1
		return 0

	def __update(self, rate, predicted, example):
		""" update the weights variable 
			@param	rate: learning rate
			@param	predicted: predicted class label
			@param	example: Example object
		"""

		label = example.getLabel()
		example =  example.getData()

		newWeights = [self.weights[i]+(rate*(label-predicted)*example[i]) for i in xrange(len(self.weights))]
		self.weights = newWeights

	def train(self, examples, rate=.01, epochs=None):
		"""	train Perceptron's weights on the ExampleSet supplied
			@param	examples: ExampleSet object containing Example objects
			@param	rate: learning rate
			@param	epochs: maximum number of epochs before ending training
		"""
		self.epochs = epochs

		# Train until maximum number of epochs is reached if epochs are specified.
		if self.epochs is not None:
			epoch = 0
			while epoch < self.epochs:

				for example in examples:
					dotProduct = self.__dot(example.getValues()+[1], self.weights)
					signResult = self.__sign(dotProduct * example.getLabel())
					equalSigns = self.__evaluate(signResult, example.getLabel())

					if not equalSigns:
						self.__update(rate, signResult, example)

					epoch += 1

		# Train until data converges.
		else:
			converged = False

			while converged == False:
				converged = True
				for example in examples:
					dotProduct = self.__dot(example.getValues()+[1], self.weights)
					signResult = self.__sign(dotProduct * example.getLabel())
					equalSigns = self.__evaluate(signResult, example.getLabel())

					if not equalSigns:
						self.__update(rate, signResult, example)
						converged = False

					#print "These are the weights: {}\tExample: {}".format(self.weights, example.getValues())

	def classify(self, example):
		""" return classification for one example 
			@param	example: list of values (i.e., NOT an Example object
			@return integer indicating class
		"""
		return self.__sign(self.__dot(example, self.weights))

	def test(self, examples):
		""" return a list of classifications for an ExampleSet
			@param	examples: ExampleSet object with Example objects
			@return	list of integers indicating classifications for each example
		"""
		print "Testing"
		results = list()
		append = results.append

		for example in examples:
			append((self.classify(example.getData()), example.getLabel()))#, example.getLabel(), example.getValues()

		print results
		return results

if __name__=="__main__":
	import matplotlib.pyplot as plt
	from mpl_toolkits.mplot3d import Axes3D
	import random
	import os

	print os.getcwd()
	ds = DataSet("..//..//data//ml//test_weather.gla")

	p = Perceptron(dataset=ds, epochs=10)

	print "Perceptron test:", p.classify([0,0,1,1])
	p.test(ds.getExamples())

	attribute1 = [n for n in xrange(10)]
	attribute2a = [random.sample(range(50)[:35],1)[0] for n in xrange(5)]
	attribute2b = [random.sample(range(50)[20:],1)[0] for n in xrange(5)]

	class0examples = [[attribute1[n], attribute2a[n], 0] for n in xrange(5)]
	class1examples = [[attribute1[n], attribute2b[n], 1] for n in xrange(5)]

	for exs in class1examples+class0examples:
		#print exs
		ds.addExample(Factory().example(exs))

	class0 = [x.getValues() for x in ds.getExamplesByClass(0)]
	class0x = [x[0] for x in class0]
	class0y = [x[1] for x in class0]
	class0z = [((x[0]-np.mean(class0x))*x[1]-np.mean(class0y))**2 for x in class0]

	class1 = [x.getValues() for x in ds.getExamplesByClass(1)]
	class1x = [x[0] for x in class1]
	class1y = [x[1] for x in class1]
	class1z = [((x[0]-np.mean(class1x))*x[1]-np.mean(class1y))**2 for x in class1]

	fig = plt.scatter(class1x, class1y)
	fig2 = plt.scatter(class0x, class0y, c='r')
	#plt.show()

	#print class0
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(class0x, class0y, class0z, c='r')
	ax.scatter(class1x, class1y, class1z, c='b')
	#plt.show()

	"""
	c0xm = np.mean(class0x)
	c1xm = np.mean(class1x)
	c0ym = np.mean(class0y)
	c1ym = np.mean(class1y)
	c0zm = np.mean(class0z)
	c1zm = np.mean(class1z)

	class0x = [n-c0xm for n in class0x]; class0y = [n-c0ym for n in class0y]; class0z = [n-c0zm for n in class0z]
	class1x = [n-c1xm for n in class1x]; class1y = [n-c1ym for n in class1y]; class1z = [n-c1zm for n in class1z]
	"""
	#ax.scatter(class0x, class0y, class0z, c='g')
	#ax.scatter(class1x, class1y, class1z, c='r')
	#plt.show()

