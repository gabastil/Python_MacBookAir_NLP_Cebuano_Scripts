#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Name:     DocumentPlus.py
# Version:  1.0.1
# Author:   Glenn Abastillas
# Date:     September 14, 2015
#
# Purpose: Allows the user to:
#           1.) Read in a document (.txt)
#           2.) Find a word in the loaded document (.txt)
#           3.) Save results of word search along with leading and trailing text whose length is controlled by the user.
#           4.) Count descriptive features of the word find (i.e., count, BOS, EOS, etc.).
#
# To see the script run, go to the bottom of this page.
#
# This class is directly inherited by the following classes:
#   - SpreadsheetSearch.py
#	- FindDebrid.py
#
# Updates:
# 1. [2016/02/29] - changed wording of notes in line 17 from '... class is used in the following ...' to '... class is directly inherited by the following ...'.
# 2. [2016/02/29] - changed variable name 'text' to 'searchTerm' to match related variable name in parent class.
# 3. [2016/02/29] - changed import statement from 'import Document' to 'from Document import Document' to allow for this class to inherit 'Document' instead of 'Document.Document'. Version changed from 1.0.0 to 1.0.1.
# 
# - - - - - - - - - - - - -
""" builds on Document class to provide text manipulation and text search capabilities

DocumentPlus extends the Document class providing new functionality such as
searching documents for particular key words or tokens allowing for control
on how much leading and trailing context to include. In addition to this, the
DocumentPlus class contains methods for removing stop words and punctuation. 
The corpus of stop words and punctuation is flexible, which means that the 
words or punctuation may be added upon or deleted.

"""

__author__      = "Glenn Abastillas"
__copyright__   = "Copyright (c) September 14, 2015"
__credits__     = "Glenn Abastillas"

__license__     = "Free"
__version__     = "1.0.1"
__maintainer__  = "Glenn Abastillas"
__email__       = "a5rjqzz@mmm.com"
__status__      = "Deployed"

from Document import Document
import re

class DocumentPlus(Document):

	def __init__(self, filePath = None, savePath = None, stop_puncs="./data/stoppuncs.txt", stop_words="./data/stopwords.txt", norm_words="./data/normwords.txt"):
		""" constructor for this class with two parameters
			@param	filePath: input file
			@param	savePath: output location
		"""

		self.super = super(DocumentPlus, self)	# Assign self.super the parent class Document
		self.super.__init__(filePath, savePath)	# Initialize the parent class Document
		
		self.stop_puncs   = self.open(stop_puncs).split()
		self.stop_words   = self.open(stop_words).split()
		self.norm_words   = dict()

		# initialize the norm_words variable
		for line in self.open(norm_words, splitLines=True, splitTabs=True):

			contractions 	= line[0].split(';')
			normalized_word = line[-1]

			for contraction in contractions:
				self.norm_words[contraction] = normalized_word

	def addStopPunctuation(self, newStopPunctuation):
		""" Add a new stop punctuation to this class's list
			@param	newStopPunctuation: new stop punctuation to add to this object
		"""
		newStopPunctuation = newStopPunctuation.lower()

		# If stop punctuation is not in the list already, add it
		if newStopPunctuation not in self.stop_puncs:
			self.stop_puncs.append(newStopPunctuation)

	def addStopWord(self, newStopWord):
		""" Add a new stop word to this class's list
			@param	newStopWord: new stop word to add to this object
		"""
		newStopWord = newStopWord.lower()

		# If stop word is not in the list already, add it
		if newStopWord not in self.stop_words:
			self.stop_words.append(newStopWord)

	def contains(self, term):
		"""	Return true if term in self.textFile
			@param	term: term to check in this document
			@return	True or False
		"""
		if term in self.textFile:
			return True
		
		return False

	def deleteStopWord(self, stopWordToRemove):
		""" Remove a stop word from this class's list
			@param	stopWordToRemove: stop word to remove from this object
		"""
		self.stop_words.remove(stopWordToRemove.lower())

	def find(self, text, term):
		"""	find the specified term in the text and return a list of indices
			@param	text: text String to search term in
			@param	term: String term to search for
			@return	List of tuples with start and end indices for search term
		"""
		listOfResults = list()

		currentIndex  = 0
		termLength	  = len(term)
		append		  = listOfResults.append

		while currentIndex >= 0:
			currentIndex = text.find(term, currentIndex+1)
			append((currentIndex, currentIndex+termLength))

		# Return listOfResults[:-1] because the last tuple contains -1 (negative one)
		return listOfResults[:-1]

	def findLines(self, text, term, scope=75):
		"""	Find the specified term in the text and return its surrounding context
			@param	text: text String to search term in
			@param	term: String term to search for
			@param	scope:	number of leading and trailing characters to include
			@return	List of Strings with matching term
		"""
		listOfResults = list()

		currentIndex  = 0
		termLength	  = len(term)
		append		  = listOfResults.append
		replace		  = str.replace

		text = text.lower()
		term = term.lower()

		while currentIndex >= 0:
			currentIndex = text.find(term, currentIndex+1)

			indexA = currentIndex - scope
			indexB = currentIndex + termLength + scope

			findings1 = replace(text[indexA:indexB], '\n', '_')
			findings2 = replace(findings1, '\t', ' ')
			append(findings2)

		return listOfResults[:-1]

	def findOwnLines(self, term, scope=75):
		"""	Find the specified term in the text and return its surrounding context
			@param	term: String term to search for
			@param	scope:	number of leading and trailing characters to include
			@return	List of tuples with start and end indices for search term
		"""
		return self.findLines(text=' '.join(self.textFile), term=term, scope=scope)

	def findTerms(self, text, terms, scope=50, includeAll=True):
		"""	find the specified terms in the text and return its surround context
			@param	text: text String to search term in
			@param	terms: list of term Strings [keyword, context term 1, ...]
			@param	scope:	number of leading and trailing characters to include
			@return	List of tuples with start and end indices for search term
		"""
		listOfResults  = list()
		listOfMatchesMain = list()
		listOfMatchesSecondary = list()

		append  = listOfResults.append
		replace	= str.replace

		keywordIndices = self.find(text, terms[0])

		# loop through the indices and check for dependencies if terms list has more than 1 term
		for indices in keywordIndices:

			leading  = text[indices[0]-scope:indices[0]]
			trailing = text[indices[0]:indices[0]+scope]

			leading  = replace(replace(leading, '\n', '_'), '\t', ' ') 
			trailing = replace(replace(trailing, '\n', '_'), '\t', ' ') 

			# if terms list has more than 1 term (i.e., contextual terms), see if present within scope
			if len(terms) > 1:

				# loop through the contextual terms and check for presence within scope
				for term in terms[1:]:

					# if term in either leading or trailing
					if (replace(term, '*', '') in leading.lower()) or (replace(term, '*', '') in trailing.lower()):

						# if '*' in term, do not add this context
						if '*' in term:
							pass

						# if '*' not indicated, add this context
						else:
							excerpt = leading + trailing

							if excerpt not in listOfResults:
								if includeAll==True:
									append(excerpt+'\t'+text[indices[0]:indices[1]]+'\t'+term)
								else:
									append(excerpt)

			# if terms list has 1 term, just append the excerpt
			else:

				excerpt = leading + trailing

				if excerpt not in listOfResults:
					if includeAll==True:
						append(excerpt+'\t'+text[indices[0]:indices[1]]+'\t')
					else:
						append(excerpt)

		return listOfResults

	def findTokens(self, text, term, scope=7, sort=False):
		"""	find the specified term in the text and return its surrounding token context
			@param	text: text String to search term in
			@param	term: String term to search for
			@param	scope: number of leading and trailing tokens to include
			@return	List of Strings of tokens with matching term
		"""
		listOfResults = list()

		append	= listOfResults.append
		tokens	= self.removeStopWords(self.removePunctuation(text.lower()), False)
		term	= term.lower()

		# Loop through all the tokens
		for token in tokens:

			# If this token matches the search term, add to list
			if term in token:
				indexOfToken = tokens.index(token)

				indexA = indexOfToken - scope
				indexB = indexOfToken + scope

				if sort:
					append(' '.join([token, tokens[indexOfToken+1], tokens[indexOfToken-1], \
											tokens[indexOfToken+2], tokens[indexOfToken-2], \
											tokens[indexOfToken+3], tokens[indexOfToken-3], \
											tokens[indexOfToken+4], tokens[indexOfToken-4]]))
				else:
					append(' '.join(tokens[indexA:indexB]))

		return listOfResults

	def getStopPunctuation(self):
		"""	Get all stop punctuation used in this class
			@return	List of stop punctuation
		"""
		return self.stop_puncs

	def getStopWords(self):
		"""	Get all stop words used in this class
			@return	List of stop words
		"""
		return self.stop_words

	def getTokens(self, text):
		"""	Get tokens from a document
			@param	text: text String
			@return	list of tokens
		"""
		textWithoutPunctuation = self.removePunctuation(text)
		textWithoutStopWords   = self.removeStopWords(textWithoutPunctuation)
		return textWithoutStopWords

	def getWords(self, text):
		"""	Get words from a document without punctuation
			@param	text: text String
			@return list of words
		"""
		textWithoutPunctuation = self.removePunctuation(text)
		return [word for word in textWithoutPunctuation.split() if len(word) >= 1]

	def removeContractions(self, text=None):
		""" Remove all contractions from input text
			@return text string with normalized words
		"""

		if type(text) != type(str):
			text = " ".join(text)

		for key in self.norm_words:
			text = text.replace(key, self.norm_words[key])

		text = text.split(" ")

		return text

	def removePunctuation(self, text=None):
		""" Remove all punctuation from an input text
			@text	text: text String with punctuation to remove
			@return	String of text without punctuation
		"""
		# Loop through all the punctuation in self.stop_puncs
		for punctuation in self.stop_puncs:

			# Replace punctuation with leading and trailing spaces
			text = text.replace(" " + punctuation, " ")
			text = text.replace(punctuation + " ", " ")

			# Replace punctuation within the first and last 5 characters of the text
			text = text[:5].replace(punctuation, "") + text[5:]
			text = text[:-5] + text[-5:].replace(punctuation, "")

			# Otherwise, remove the punctuation if not in list specified
			if punctuation not in [".", ",", "-", "--"]:
				text = text.replace(punctuation, "")

		return text

	def removeStopWords(self, text=None, sort=True, lc=False):
		"""	Remove all stop words from an input list of tokens
			@param	text: List of Strings with stop words to remove
			@param	sort: sort the output
			@param	lc: return lower case word list
			@return	List of tokens without stop words
		"""

		if type(text) == type(str()):
			text = text.split()

		textWithStopWords    = text
		textWithoutStopWords = list()

		if sort:
			textWithStopWords = sorted(textWithStopWords)

		append = textWithoutStopWords.append
		lower  = str.lower

		# Loop through all the words in the text
		for word in textWithStopWords:

			# If the word is not a stop word, add it to textWithoutStopWords
			if lower(word) not in self.stop_words:
				if lc==True:
					append(lower(word))
				else:
					append(word)

		return textWithoutStopWords

	def removeOwnContractions(self):
		""" Remove the contractions from this object's self.textFile variable
		"""
		self.textFile = self.removeContractions(text=self.textFile)

	def removeOwnPunctuation(self):
		""" Remove all punctuation from this object's self.textFile variable
		"""
		self.textFile = self.removePunctuation(self.open(self.filePath)).split()

	def removeOwnStopWords(self, sort=True, lc=False):
		"""	Remove all stop words from this object's self.textFile variable
			@param	sort: sort the output
			@param	lc: return lower case word list
		"""
		self.textFile = self.removeStopWords(text=self.textFile, sort=sort, lc=lc)

	def setOwnTokens(self):
		""" Set this object's self.textFile variable as tokens
		"""
		self.removeOwnPunctuation()
		self.removeOwnStopWords()

if __name__ =="__main__":
	""" run as a script if this file is run as a stand-alone program
	"""

	d = DocumentPlus("data/test.txt","data/")

	text = d.open("data/test.txt")
	#d.find("This and th:at and ,ever$ything- spice @$%!@is wha#######t makes the world feel about right. in-s$pa@ce.")
	t = d.find("This is a test for this thing, right, test?", "test")
	t = d.findLines(d.open(d.filePath), "american")
	print t

	t = d.findTokens(d.open(d.filePath), "american")
	print t

	a = d.removePunctuation("This and th:at and ,ever$ything- spice @$%!@is wha#######t makes the world feel about right. in-s$pa@ce.")
	b = d.removeStopWords(a.split())
	c = d.getTokens("this is a huge string- of t^&ext.... -23.432.. that... has a bunch of words in it that I am interested in advanced..!")
	c = d.getTokens("g/dl")

	print "\n.removePunctuation()\t", a
	print ".removeStopWords()\t", b
	print ".getTokens()\t", c

	print d.find(text, "clinic")
	print len(d.findTerms(text, ["the", "bed", "time", "patient"]))
	print d.findTerms(text, ["the", "bed", "time", "patient"])
	print len(d.findTerms(text, ["the"]))
	print d.findTerms(text, ["the"])