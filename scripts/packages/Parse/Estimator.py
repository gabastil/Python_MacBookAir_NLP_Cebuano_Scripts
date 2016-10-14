#!/usr/bin/python
# -*- coding: UTF-8 -*-
# THIS CLASS IS MOSTLY FINISHED 
# THERE'S AN ERROR WITH THE __addToCount() 
# METHOD WHEN THE WORD IS SHORTER THAN THE N-GRAM (~4)
# Glenn Abastillas November 30, 18:02

from Counter import Counter
from math import log
from copy import deepcopy

__author__ = "Glenn Abastillas"

class Estimator(Counter):
	"""
	Estimator gets probabilities of words or word chains counted in a text.
	"""

	def __getFrequency(self, dictionary, total, asLog = False, logBase = 2):
		"""
			__getFrequency() calculates the frequency/probability of keys with respect to the total count.
			Does not return anything. This method updates the dictionary passed through it as a parameter.

			dictionary:	the dictionary to be used.
			total:		total number of counts in the dictionary provided.
			asLog:		indicates assignment of negative logarithmic results.
						if True or floating point numbers if False. If False, there is a risk of underflow.
		"""

		try:
			for keys in dictionary.keys():
				self.__getFrequency(dictionary[keys], total, asLog)
		except(AttributeError):
			for keys in dictionary.keys():
				frequency = dictionary[keys]/total
				if asLog == True:
					dictionary[keys] = log(frequency, logBase)
				elif asLog == False:
					dictionary[keys] = frequency

	def probabilities(self, text = None, ngram = 1, level = 1, lc = True, punc = False, asLog = True, dictionary = None):
		"""
			probabilities() builds a dictionary of counts of items in a text specified by level (e.g., 0 = char, 1 = token) and 
			calculates the frequency/probability of each of those items represented in floating or logarithmic numbers.
			Returns a dictionary containing the items and their corresponding frequencies/probabilities.

			text:	input string to counted.
			level:	level at which to parse the text input.
					0 = character
					1 = token
					2 = phrase
					3 = sentence

			ngram:	number of characters, tokens, phrases, or sentences covered by the ngram function.
			lc:		indicates use of lower case. Passed through to functions inherited from the Parse class.
			punc:	indicates inclusion of punctuation. Passed through to functions inherited from the Parse class.
			asLog:	passed through to the self.__getFrequency() function to indicate assignment of negative logarithmic results.
					if True or floating point numbers if False. If False, there is a risk of underflow.
		"""
		if dictionary == None:
			count = self.count(text, ngram, level, lc, punc)
		else:
			count = deepcopy(dictionary)

		total = self.total(count)

		self.__getFrequency(count, total, asLog)

		return count

	def entropy(self, data):
		pass

	def informationGain(self, data):
		pass

if __name__ == "__main__":
	#t = "kana ang ..akong \"giingon\" nimo; ayaw ug buhat niana 2.4 pa. kahibalo ba ka unsa akong giingon nimo? but do you know what's happening. There are, you know, many different things to see here."
	#t = "abcdefghijkkkkk"
	#data = "this is a test text sample. It should contain a good good good amount of words because it has to be use for a test. I am going to try to use as full of words as possible possible possible."
	
	dataSource = "/Users/ducrix/Documents/Research/Python/data/ceb2.txt"
	t = open(dataSource, 'r').read()

	p = Estimator()

	a = p.count(t,2,1, tupleCount = True)[0]
	z = p.count(t,2,1, tupleCount = True)[1]
	b = p.count(t,1,0)
	d = p.probabilities(t,2,0)
	e = p.probabilities(dictionary = z)

	#print d
	#print e
	print a
	print z
	print 2**e['t w']
	#print len(e), e.keys()

	dataSource = "/Users/ducrix/Documents/Research/Python/data/ceb4.txt"
	t = open(dataSource, 'r').read()

	a = p.update(a,t,2,0)
	print "a", a
	f = a
	b = p.count(t,1,0)
	#d = p.probabilities(t,2,0)
	e = p.probabilities(t,1,0, dictionary = f)

	#print d
	#print e
	print "e", e

	#print "Characters:", a
	#print "Characters:", b

	c = p.total(a)

	print c
