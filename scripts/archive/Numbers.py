#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Author: Glenn Abastillas

from Parse.Parse import Parse

class Numbers(Parse):

	def __init__(self, text = None):
		super(Numbers, self).__init__(text = text)

	def freqTable(self, getDict = False, sort = False, asList = False):
		freqTable = []

		tokenDict = dict()
		tokenList = self.tokens(include = False, lc = True)
		tokenSet  = set(tokenList)

		numberOfTokens = 0.

		for t in tokenList:
			if t not in tokenDict:
				tokenDict[t] = 1

			else:
				tokenDict[t] = tokenDict[t] + 1

			numberOfTokens += 1

		if getDict == True:
			#if sort == True:
				#tokenDict = sorted(tokenDict, key = lambda x:x[1], reverse = True)

			return tokenDict


		for td in tokenDict:
			
			frequency = round(tokenDict[td]/numberOfTokens,4)

			if asList == True:
				freqTable.append([td, frequency])
			else:
				freqTable.append((td, frequency))

		if sort == True:
			freqTable = sorted(freqTable, key = lambda x:x[1], reverse = True)
			#print tokenDict[td],n
		
		#print tokenSet
		#print freqTable
		#print sorted(freqTable, key = lambda x: x[1], reverse = True)
		#print tokenDict

		return freqTable


	def getNumberOfTokens(self):
		return len(self.tokens())

	def getNumberOfSentences(self):
		return len(self.sentences())

	def getNumberOfPhrases(self):
		return len(self.phrases())


if __name__ == "__main__":
	import os

	os.chdir("/Users/ducrix/Documents/Research/Python/data")

	fin = open("ceb11.txt", 'r')
	t = fin.read()
	fin.close()

	#t = "This is a sample text. You can use or lose it but you will never improve it. Do you know what I mean by all of this or not? No? What not? All in All"
	n = Numbers(text = t)
	#print n.freqTable(sort = True, asList = True)
	print n.getNumberOfTokens(), n.tokens()[:50]
	print n.getNumberOfPhrases(), n.phrases()[:15]
	print n.getNumberOfSentences(), n.sentences()[:10]