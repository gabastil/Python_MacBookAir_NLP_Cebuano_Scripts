#!/usr/bin/python
# -*- coding: UTF-8 -*-
# THIS CLASS IS MOSTLY FINISHED 
# THERE'S AN ERROR WITH THE __addToCount() 
# METHOD WHEN THE WORD IS SHORTER THAN THE N-GRAM (~4)
# Glenn Abastillas December 1, 00:55

from Parser import Parser
from collections import defaultdict

__author__ = "Glenn Abastillas"

class Counter(Parser):
	"""
	Counter counts the occurrences of single or word chains in a text.
	"""
	def __makeDictionary(self, ngram):
		"""

			!!TypeError OCCURS WITH NGRAMS/TUPLES == 4!!

			__makeDictionary() creates a dictionary with n-levels (indicated by ngram variable)
			Returns a blank dictionary.

			ngram:	number of terms in a group indicated in self.count()
		"""

		if ngram == 1: 
			return defaultdict(float)
		else: 
			return defaultdict(lambda : self.__makeDictionary(ngram - 1))

	def __addToCount(self, terms, dictionary):
		"""

			!!TypeError OCCURS WITH NGRAMS/TUPLES == 4!!

			__addToCount() counts the appearance of terms in groups with varying lengths according to dependant terms.
			Returns void.

			terms:		list of terms to be added in the dictionary whose size is indicated by the ngram variable in self.count()
			dictionary:	the dictionary to be used
		"""

		if len(terms) == 1: 
			dictionary[terms[0]] += 1
		else: 
			self.__addToCount(terms[1:], dictionary[terms[0]])

	def __getCount(self, dictionary):
		"""

			!!TypeError OCCURS WITH NGRAMS/TUPLES == 4!!

			__getCount() sums the total number of counts in a given dictionary provided the correct depth indicated by the ngram variable.
			Returns a scalar integer.

			dictionary:	the dictionary to be used
		"""

		try:
			return sum([self.__getCount(dictionary[key]) for key in dictionary.keys()])
		except(AttributeError):
			return sum(dictionary.values())

	def count(self, text = None, ngram = 1, level = 1, lc = True, punc = False, dictionary = None, tupleCount = False):
		"""
			count() counts the presence of text items (e.g., characters, tokens) indicated by the levels variable in groups
			whose sizes are indicated by the ngram variable.
			Returns a dictionary of counts of just the order of the items as well as the appearance of tuples in the text.

			text:		input string to counted.
			level:		level at which to parse the text input.
						0 = character
						1 = token
						2 = phrase
						3 = sentence

			ngram:		number of characters, tokens, phrases, or sentences covered by the ngram function.
			lc:			indicates use of lower case. Passed through to functions inherited from the Parse class.
			punc:		indicates inclusion of punctuation. Passed through to functions inherited from the Parse class.
			dictionary:	dictionary specified for updating.
			tupleCount:	indicate creation of a tuple dictionary, which counts the number of times the tuple appears in the text.
		"""

		if (text == None) or (ngram < 1): return None

		if dictionary is None: dictionary = self.__makeDictionary(ngram)
		if tupleCount == True: dictTuples = self.__makeDictionary(1)

		addToCount = self.__addToCount
		join 	   = str.join

		if level == 0:
			"""
				Count the presence of CHARACTERS
			"""
			listOfTokens = self.tokens(text = text, punc = punc, lc = lc)				#	Get list of tokens for counting characters that start and end tokens
			
			for token in listOfTokens:
				for item in self.ngrams(token, ngram):
					addToCount(item, dictionary)

					if tupleCount == True:
						addToCount([join(' ', list(item))], dictTuples)
			
		elif level == 1:
			"""
				Count the presence of TOKENS
			"""
			listOfSentences = self.sentences(text = text, punc = punc, lc = lc)			#	Get list of sentences for counting tokens that start and end sentences

			for sentence in listOfSentences:
				for item in self.ngrams(sentence.split(), ngram):
					addToCount(item, dictionary)

					if tupleCount == True:
						addToCount([join(' ', list(item))], dictTuples)

		elif level == 2:
			"""
				Count the presence of PHRASES
			"""
			listOfPhrases = self.phrases(text = text, punc = punc, lc = lc)				#	Get list of phrases for counting

			for item in self.ngrams(listOfPhrases, ngram):
				addToCount(item, dictionary)

				if tupleCount == True:
					addToCount([join(' ', list(item))], dictTuples)
			
		elif level >= 3:
			"""
				Count the presence of SENTENCES
			"""
			listOfSentences = self.sentences(text = text, punc = punc, lc = lc)			#	Get list of sentences for counting

			for item in self.ngrams(listOfSentences, ngram):
				addToCount(item, dictionary)

				if tupleCount == True:
					addToCount([join(' ', list(item))], dictTuples)

		if tupleCount == True: return dictionary, dictTuples
		else: return dictionary

	def ngrams(self, textList = None, ngram = 2):
		"""
			ngrams() groups list items into n-sized lists as indicated by the ngram variable.
			Returns a list of groups of items with ngram size.

			textList:	list of items to be grouped.
			ngram:		size of items for new groups.
		"""

		if textList == None: 
			return None

		if type(textList) == type(str()): 
			textList = [character for character in textList]

		ngramsResults 	= list()
		textLength 		= len(textList)
		textRange  		= xrange(textLength)

		append 			= ngramsResults.append

		for i in textRange:
			if i == 0:
				if ngram == 1:
					append(['$'])
					append(textList[i:ngram])
				else:
					append(['$'] + [item for item in textList[i:i+ngram-1]])

			elif i == textLength - ngram + 1:
				append([item for item in textList[i:i+ngram-1]] + ['#'])
				break

			elif textLength < ngram:
				append([item for item in textList] + ['#'])
				break

			else:
				append([item for item in textList[i:i+ngram]])

		return ngramsResults

	def total(self, countResults = None):
		"""
			total() returns the total number of counts from count(). Ngram variable should not exceed 3.
			Returns a scalar integer.

			countResults:	dictionary of term counts from self.count()
		"""
		if countResults == None: return 0
		return self.__getCount(countResults)

	def update(self, dictionary, text = None, ngram = 1, level = 1, lc = True, punc = False):
		"""
			update() revises the dictionary specified by appending new text.
			Returns dictionary without changes of text is None. Otherwise, returns updated dictionary.

			dictionary:	dictionary specified for updating.
			text:		input string to counted.
			level:		level at which to parse the text input.
						0 = character
						1 = token
						2 = phrase
						3 = sentence

			ngram:		number of characters, tokens, phrases, or sentences covered by the ngram function.
			lc:			indicates use of lower case. Passed through to functions inherited from the Parse class.
			punc:		indicates inclusion of punctuation. Passed through to functions inherited from the Parse class.
		"""

		if text == None: return dictionary
		else: return self.count(text = text, ngram = ngram, level = level, lc = lc, punc = punc, dictionary = dictionary)

if __name__ == "__main__":
	t = "kana ang ..akong \"giingon\" nimo; ayaw ug buhat niana 2.4 pa. kahibalo ba ka unsa akong giingon nimo? but do you know what's happening. There are, you know, many different things to see here."
	#t = "abcdefghijkkkkk"
	#data = "this is a test text sample. It should contain a good good good amount of words because it has to be use for a test. I am going to try to use as full of words as possible possible possible."
	
	dataSource = "/Users/ducrix/Documents/Research/Python/data/ceb2.txt"
	
	t = open(dataSource, 'r').read()

	p = Counter()

	a = p.count(t,2,0)
	b = p.count(t,2,1)

	#print "Characters:", a
	#print "Characters:", b

	c = p.total(b)

	print c
	#print "Tokens: ", p.count(t,1,True,1,False)
	#print "Sentences: ", p.count(t,1,True,2,False)
	#print "Phrases: ", p.count(t,1,True,3,False)
	#print "testestt for the testing".find('t')
	#print p.cleanText(t)
