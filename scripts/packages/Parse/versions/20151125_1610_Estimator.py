#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "Glenn Abastillas"
from Counter import Counter
from collections import defaultdict
from nltk import ngrams as ng

class Estimator(Counter):
	"""
	Calculate basic descriptive statistics on a textual data set.
	"""

	def count(self, data, count = "t", lc = True, uc = False, includeNumbers = True):
		"""
			Count() getCounts occurrences of each unit (e.g., sentence, token, etc.) with respect to scope as indicated by 'count' variable.

			data:	data to be counted.
			count:	determine what to count. Possible values are: "s" (sentences), "p" (phrases), "t" (tokens), or "a" (alphabet, i.e., characters)
					default is "t" (tokens).

			returns a dictionary of getCounts
		"""

		if count == "s":
			pass
		elif count == "p":
			pass
		elif count == "t":
			return self.getWordList(lc = lc, uc = uc, includeNumbers = includeNumbers).count(data)
		elif count == "a":
			pass
		else:
			raise ValueError("Please enter the following values: \"s\" for sentences, \
							\"p\" for phrases, \"t\" for tokens, \"a\" for characters")

	def frequency(self, data, count = "t", countDone = False, exact = False, lc = True, uc = False, includeNumbers = True):
		"""
			Frequency() finds the occurrence frequency of each unit (e.g., sentence, token, etc.) with respect to scope as indicated by 'count' variable.

			data:		data to be counted.
			count:		determine what to count. Possible values are: "s" (sentences), "p" (phrases), "t" (tokens), or "a" (alphabet, i.e., characters)
						default is "t" (tokens).
			countDone:	indicates whether or not the data was already passed through Count().
						default is False

			returns a dictionary of frequencies
		"""
		if exact == False:
			data = data.lower()

		if countDone == False:
			data = self.count(data = data, count = count, lc = lc, uc = uc, includeNumbers = includeNumbers)

		return data

	def getNgramsCount(self, 	count 				= 't',
								nRange 				= 2, 		returnType 			= "dict", 
								countDone 			= False, 	exact 				= False, 
								lc 					= True, 	uc 					= False, 
								includeNumbers 		= True, 	includePunctuation 	= False):

		ngramsList 	= []
		count 		= count.lower()

		for sentence in self.sentences():
			tokensList = self.tokens(text = sentence, lc = lc, includePunctuation = includePunctuation)

			if count == 't':
				ngramsList.extend(ngrams(tokensList, nRange))
			
			elif count == 'a':
				for token in tokensList:
					for i in range(len(token)):
						if i == 0:
							ngramsList.append(('#', token[i]))
						elif i == len(token) - 1:
							ngramsList.append((token[i], '#'))
						else:
							ngramsList.append((token[i], token[i+1]))

				print ngramsList

		if len(ngramsList) > 0:
			ngramsCountList = defaultdict(lambda : defaultdict(int))

			for term in ngramsList:
				ngramsCountList[term[0]][term[1]] += 1

			return ngramsCountList

	def getNgramsFrequencies(self, ngramsList = None, nRange = 2, returnType = "dict", countDone = False, exact = False, lc = True, uc = False, includeNumbers = True):
		if ngramsList == None:
			ngramsList = self.getNgramsCount(nRange = 2, returnType = returnType, countDone = countDone, exact = exact, lc = lc, uc = uc, includeNumbers = includeNumbers)

		def getTotal(ngrams):
			if type(ngrams) == type(int()):
				return ngrams
			else:
				total = 0
				for key in ngrams.keys():
					total += getTotal(ngrams[key])
				return total

		total = float(getTotal(ngramsList))

		ngramsFrequenciesList = defaultdict(lambda:defaultdict())

		for key1 in ngramsList.keys():
			for key2 in ngramsList[key1].keys():
				ngramsFrequenciesList[key1][key2] = ngramsList[key1][key2]/total

		print ngramsFrequenciesList

	def getCounts(self, count = "t", returnType = "dict", countDone = False, exact = False, lc = True, uc = False, includeNumbers = True):
		"""
			returnType:		determine data structure return type
								1. "dictionary" returns a dictionary	(also, "dict", "d", "0")
								2. "list" 		returns a list			(also, "ls", "l", "1")
			count:			determines the scope of the count. 
								1. "a" is for "alphabet"
								2. "t" is for "tokens"
								3. "p" is for "phrases"
								4. "s" is for "sentences"
			countDone:		count complete
			exact:			case-sensitive count or case-insensitive count
			lc:				process and return lower case
			uc:				process and return upper case
			includeNumbers:	include numerical characters in the method
		"""
		getCountsList = defaultdict(int)

		if exact == True:
			for phrase in self.sentences(includePunctuation = True, lc = lc, uc = uc):
				for word in phrase.split():
					getCountsList[word] += 1

		elif exact == False:
			for word in self.getWordList(lc = lc, uc = uc, includeNumbers = includeNumbers):
				getCountsList[word] += 1

		returnType = str(returnType).lower()

		if (returnType == "0") or (returnType == "d") or (returnType == "dict") or (returnType == "dictionary"):
			return getCountsList
		elif (returnType == "1") or (returnType == "l") or (returnType == "ls") or (returnType == "list"):
			return [(key, getCountsList[key]) for key in getCountsList.keys()]
		else:
			return getCountsList
	
	def getFrequencies(self, count = "t", returnType = "dict", countDone = False, exact = False, lc = True, uc = False, includeNumbers = True):

		getCountsList = self.getCounts(returnType = returnType, countDone = countDone, exact = exact, lc = lc, uc = uc, includeNumbers = includeNumbers)
		totalCount = self.getTotalCount()
		
		#print type(getCountsList)

		if type(getCountsList) == type(defaultdict):
			getFrequenciesList = defaultdict(float)

			for key in getCountsList.keys():
				getFrequenciesList[key] = getCountsList[key]/totalCount

			return getFrequenciesList

		elif type(getCountsList) == type(list()):
			getFrequenciesList = list()

			for key, value in getCountsList:
				getFrequenciesList.append((key, value/totalCount))

			return getFrequenciesList

	def getTotalCount(self):
		"""
			getTotalCount() returns a floating point number of the total number of tokens in this textual data set.
		"""
		return sum([value * 1.0 for value in self.getCounts().values()])

if __name__ == "__main__":
	import os, sys, codecs

	dataSource = "/Users/ducrix/Documents/Research/Python/data/ceb2.txt"
	#data = "this is a test text sample. It should contain a good good good amount of words because it has to be use for a test. I am going to try to use as full of words as possible possible possible."
	data = open(dataSource, 'r').read()
	#data = codecs.open(dataSource, 'r', 'utf8').read()

	e = Estimator(text = data)
	freq = e.getFrequencies(returnType = 1)
	#print "count()\t\t\t\t", e.count("")
	#print "getCounts()\t\t\t", e.getCounts(returnType = 1)
	#print "frequency()\t\t\t", e.frequency("to")
	#print "getFrequencies()\t", len(freq)
	#print "getTotalCount()\t\t", e.getTotalCount()
	print "getNgramsCount()\t\t\t", e.getNgramsCount('a')
	print ng("this is a test", 3)
	#print "getNgramsFrequencies()\t", e.getNgramsFrequencies()
	#for w in e.getWordList():
	#	print e.frequency(w), '\t', w

