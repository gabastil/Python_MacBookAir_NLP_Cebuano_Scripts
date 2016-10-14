#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = "Glenn Abastillas"
from Parse.Parse import Parse

class Extractor(Parse):

	def __init__(self, text = None):
		super(Extractor, self).__init__(text = text)

	def getContext(self, word = None, scope = 10, exact = False):
		"""
			getContext allows the user to grab leading and trailing context for a certain word specified.
			If the word is the first or last word, then beginning-of-sentence (i.e., !!!) or end-of-sentence (i.e., ###) are returned.

			word:	this is the term to search for in the text.
			scope:	this is the amount of leading or trailing tokens to include.
			exact: 	this makes the search case sensitive.
		"""

		if word == None:
			return None
		elif exact == False:
			word = word.lower()

		textList = self.tokens(includePunctuation = False, lc = True)
		concList = []

		if len(textList) < scope:
			scope = len(textList)/2

		for i in range(len(textList)):
			token = textList[i]

			concLeft = ""
			concRght = ""

			if token == word:
				if (i + 1) == (len(textList)):
					#print textList[-scope:i]
					concLeft = " ".join(textList[i - scope - 1:i])

				elif i == 0:
					#print textList[i:scope]
					concRght = " ".join(textList[i:i + scope])

				elif (i < scope) and (i > 0):
					concLeft = " ".join(textList[0:i])
					concRght = " ".join(textList[i + 1:i + scope])

				else:
					concLeft = " ".join(textList[i - scope - 1:i])
					concRght = " ".join(textList[i + 1:i + scope])

			if (len(concLeft) == 0) and (len(concRght) == 0):
				pass

			elif (len(concLeft) > 0) and (len(concRght) > 0):
				concList.append([concLeft, token, concRght])

			elif (len(concLeft) > 0) and (len(concRght) == 0):
				concList.append([concLeft, token, "###"])

			elif (len(concLeft) == 0) and (len(concRght) > 0):
				concList.append(["!!!", token, concRght])

		return concList

	def getPairs(self, word1 = None, word2 = None, includeCount = False, includeSearchTerm = True):
		"""
			getPairs allows the user to grab bigrams (i.e., pairs) containing one or both words specified.
			If the word is the first or last word, then beginning-of-sentence (i.e., !!!) or end-of-sentence (i.e., ###) are returned.

			word1:				word is the leading term, terms after this word are searched for.
			word2:				word is the trailing term, terms before this word are searched for.
			includeCount:		if True, the count of the bigram is included.
								this is False by default.
			includeSearchTerm:	if False, then only the list of leading or trailing terms are returned.
								this is True by default to show the context.
		"""

		if word1 == None and word2 == None:
			return None
		elif word2 == None:
			searchType = 0	# 0 = leading word exists
			searchTerm = [word1.lower()]
		elif word1 == None:
			searchType = 1	# 1 = trailing word exists
			searchTerm = [word2.lower()]
		else:
			searchType = 2	# 2 = both leading and trailing words exist
			searchTerm = [word1.lower(), word2.lower()]
			includeSearchTerm = True

		#print "search type: ", searchType
		textList = self.tokens(includePunctuation = False, lc = True)
		pairList = []

		for i in range(len(textList)):
			token = textList[i]

			if token in searchTerm:
				if (searchType == 0) and (i + 1 != len(textList)):
					token1 = token
					token2 = textList[i+1]
				elif (searchType == 0) and (i + 1 == len(textList)):
					token1 = token
					token2 = "###"

				if (searchType == 1) and (i > 0):
					token1 = textList[i-1]
					token2 = token
				elif (searchType == 1) and (i == 0):
					token1 = "!!!"
					token2 = token

				if (searchType == 2) and (i + 1 != len(textList)):

					if (textList[i] == token) and (textList[i+1] == token):
						token1 = token
						token2 = textList[i+1]

				if includeSearchTerm == True:
					pairList.append([token1, token2])
				elif (includeSearchTerm == False) and (searchType == 0):
					pairList.append(token2)
				elif (includeSearchTerm == False) and (searchType == 1):
					pairList.append(token1)

		if len(pairList) > 0:
			pairListCounts = []
			for i in range(len(pairList)):
				#print i
				pairListCounts.append([pairList.count(pairList[i])])

			for i in range(len(pairList)):
				pairList[i] += str(pairListCounts[i])

		if includeCount == True:
			if len(pairList) > 0:
				pairListCounts = []
				for i in range(len(pairList)):
					#print i
					pairListCounts.append(pairList.count(pairList[i]))

				for i in range(len(pairList)):
					#print pairList[i], pairListCounts[i]
					pairList[i] += [str(pairListCounts[i])]

				pairList = sorted(pairList, key = lambda x: int(x[-1]), reverse = True)
		else:
			pairList = sorted(pairList, key = lambda x: x[-1], reverse = True)

		alreadyInList = []

		for pair in pairList:
			if pair not in alreadyInList:
				alreadyInList.append(pair)

		pairList = alreadyInList

		return pairList


		return pairList


if __name__ == "__main__":
	
	fin = open("ceb1.txt", "r")
	t = fin.read()
	fin.close()

	#t = "this person is the model of a very modern general. something here is what it does and every other mineral. da di da di da."

	e = Extractor(t)
	print e.getPairs("sa", includeCount = True)
	print e.getContext("sa")
