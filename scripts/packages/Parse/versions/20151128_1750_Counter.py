#!/usr/bin/python
# -*- coding: UTF-8 -*-
# THIS CLASS IS UNFINISHED

from Parser import Parser
from collections import defaultdict
from nltk import ngrams

__author__ = "Glenn Abastillas"

class Counter(Parser):
	"""
	Parse extracts sentences, phrases, or tokens from a text.

	1. Sentences are extracted based on the following punctuation: '.', '?', '!'. A space after each of these is required for the parses to correctly extract sentences.
	2. Phrases are extracted based on the output of the Parse.sentences() counter. A space after each of the phrasal punctuation is required for the parses to correctly extract phrases. If no subphrases are found, the sentence is returned as a phrase.
	3. Tokens are extracted based on spaces, i.e., " ".
	"""
	def __makeDictionary(self, ngram):
		if ngram == 1: return defaultdict(int)
		else: return defaultdict(lambda : self.__makeDictionary(ngram - 1))

	def count(self, text = None, ngram = 1, lc = True, level = 1, punc = False):
		"""
			Returns a dictionary of counts.

			level:	level at which to parse the text input.
					0 = character
					1 = token
					2 = phrase
					3 = sentence

			ngram:	number of characters, tokens, phrases, or sentences covered by the ngram function.

		"""
		if (text == None) or (ngram < 1): return None

		count = self.__makeDictionary(ngram)

		def addToCount(terms, dictionary):
			if len(terms) == 1: dictionary[terms[0]] += 1
			else: addToCount(terms[1:], dictionary[terms[0]])

		#print "This is the count dictionary {0}.".format(count)

		"""
		if ngram == 1:
			counts = defaultdict(int)
		elif ngram > 1:
			counts = defaultdict(lambda : defaultdict(int))
		else:
			return None
		"""

		if level == 0:
			"""
				Count the presence of CHARACTERS
			"""

			listOfTokens = self.tokens(text = text, punc = punc, lc = lc)
			#print listOfTokens
			
			for token in listOfTokens:
				#print token
				for item in self.ngrams(token, ngram):
					#print ">>>",item
					addToCount(item, count)
			
		elif level == 1:
			"""
				Count the presence of TOKENS
			"""

			#print self.ngrams(text, 3)
			listOfSentences = self.sentences(text = text, punc = punc, lc = lc)

			for sentence in listOfSentences:
				for item in self.ngrams(sentence.split(), ngram):
					#print ">>>", item
					addToCount(item, count)

		elif level == 2:
			"""
				Count the presence of PHRASES
			"""
			
			listOfPhrases = self.phrases(text = text, punc = punc, lc = lc)

			for item in self.ngrams(listOfPhrases, ngram):
				#print ">>>", item
				addToCount(item, count)
			
		elif level >= 3:
			"""
				Count the presence of SENTENCES
			"""

			listOfSentences = self.sentences(text = text, punc = punc, lc = lc)

			for item in self.ngrams(listOfSentences, ngram):
				#print ">>>", item
				addToCount(item, count)

		print "FINISHED DICTIONARY {0}".format(count)

	def total(self, countResults = None):
		if countResults == None: return 0

	def ngrams(self, textList = None, ngram = 2):
		if textList == None: return None
		if type(textList) == type(str()): textList = [character for character in textList]#textList = self.tokens(textList)

		ngramsResults 	= list()

		textLength 		= len(textList)
		textRange  		= range(textLength)

		#print "textList\t", textList
		#print "textLength\t", textLength
		#print "textRange\t", textRange

		for i in textRange:
			if i == 0:
				if ngram == 1:
					ngramsResults.append(['$'])
					ngramsResults.append(textList[i:ngram])
				else:
					ngramsResults.append(['$'] + [item for item in textList[i:i+ngram-1]])

			#elif textLength < ngram - 2:
			#	ngramsResults.append([item for item in textList[i:]] + ['#'])

			elif i == textLength - ngram + 1:
				ngramsResults.append([item for item in textList[i:i+ngram-1]] + ['#'])
				break
			elif textLength < ngram:
				ngramsResults.append([item for item in textList] + ['#'])
				break
			else:
				ngramsResults.append([item for item in textList[i:i+ngram]])

		return ngramsResults


if __name__ == "__main__":
	t = "kana ang ..akong \"giingon\" nimo; ayaw ug buhat niana 2.4 pa. kahibalo ba ka unsa akong giingon nimo? but do you know what's happening. There are, you know, many different things to see here."
	#data = "this is a test text sample. It should contain a good good good amount of words because it has to be use for a test. I am going to try to use as full of words as possible possible possible."
	
	#dataSource = "/Users/ducrix/Documents/Research/Python/data/ceb2.txt"
	
	#t = open(dataSource, 'r').read()

	p = Counter()

	print "Characters:", p.count(t,2,True,0,False)
	print "Characters:", p.count(t,2,True,2,False)
	#print "Tokens: ", p.count(t,1,True,1,False)
	#print "Sentences: ", p.count(t,1,True,2,False)
	#print "Phrases: ", p.count(t,1,True,3,False)
	#print "testestt for the testing".find('t')
	#print p.cleanText(t)
