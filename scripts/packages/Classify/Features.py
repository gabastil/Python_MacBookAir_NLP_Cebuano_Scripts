from nltk.probability 	import ConditionalFreqDist 	as cfd
from nltk.probability 	import ConditionalProbDist 	as cpd
from nltk.probability 	import LidstoneProbDist	 	as lpd
from nltk.tokenize		import word_tokenize		as tokenizeW
from nltk.tokenize		import line_tokenize		as tokenizeL
from nltk.tokenize		import sent_tokenize		as tokenizeS
from Parse.Parser 		import Parser
import os, math

class Features(object):

	spaces = ['\a', '\b', '\f', '\n', '\r', '\t', '\v', ' ']

	def load(self, pathName):
		return (open("{0}/{1}".format(pathName, f), 'r').read() for f in os.listdir(pathName))

	def mean(self, probabilityList):
		return sum(probabilityList)/(1.*len(probabilityList))

	def entropy(self, probabilityList):
		return sum([-p*math.log(p, 2) for p in probabilityList])

	def extractFeatures(self, **options):
		features  = list()
		append	  = features.append

		documents = self.load(options.get('path'))

		#mean
		if options.get('meanWordLength') == True:
			parseT = Parser().tokens
			output = [parseT(doc) for doc in documents]
			output = [self.mean([len(word) for word in words]) for words in output]
			append(output)

		if options.get('meanWordPerLineCount') == True:
			parseL = tokenizeL
			parseW = tokenizeW
			output = [parseL(doc) for doc in documents]
			output = [[len(parseW(line)) for line in doc] for doc in output]
			output = [self.mean(doc) for doc in output]
			append(output)

		if options.get('meanCharPerLineCount') == True:
			parseL = tokenizeL
			output = [parseL(doc) for doc in documents]
			output = [[len(line) for line in doc] for doc in output]
			output = [self.mean(doc) for doc in output]
			append(output)

		#numberOf
		if options.get('numberOfLines') == True:
			parseL = tokenizeL
			output = [parseL(doc) for doc in documents]
			output = [len(doc) for doc in output]
			append(output)

		if options.get('numberOfWords') == True:
			parseW = tokenizeW
			output = [parseW(doc) for doc in documents]

		if options.get('numberOfChars') == True:
			pass

		if options.get('numberOfSpaces') == True:
			pass

		#presenceOf

		#varietyOf
		if options.get('wordVariety') == True:
			parse  = Parser().tokens
			output = [parse(doc) for doc in documents]
			output = [(1.*len(words))/len(set(words)) for words in output]
			append(output)

		return features
"""
	def getFeatures(self, f):
		files = [Parser().cleanText(open("{0}/{1}".format(f, item), 'r').read().lower()) for item in os.listdir(f)]

		getWords = [self.getWords(f) for f in files]
		getWordsp = [cpd(c, lpd, 10) for c in getWords]

		print "1.", getWords
		print [[(c[k].prob(k),k) for k in c.keys()] for c in getWordsp]
		#print dir(getWordsp[0])
		print getWordsp[0].keys()
		print getWordsp[0]['$'].max()
		#print dir(getWordsp[0].get('$', 'n'))
		print getWordsp[0].get('$', 'n').samples()
		#print [self.getVocab(f) for f in files]
		#print [nltk.ConditionalFreqDist(f) for f in files]

	def getChars(self, text):
		return set(text)

	def getWords(self, text):
		tokens = Parser().tokens(text)
		cfdDict = cfd()

		for token in tokens:
			for i, letter in enumerate(token):
				if i == 0:
					cfdDict['$'].inc(letter)

				if (i+1) == (len(token)):
					#print "test"
					cfdDict[letter].inc('#')
					break
				else:
					cfdDict[letter].inc(token[i+1])

		return cfdDict

	def getVocab(self, text):
		return set(self.getWords(text))

"""
if __name__=="__main__":
	fd = "/Users/ducrix/Documents/Research/Python/data/extra"

	ft = Features()

	print ft.extractFeatures(path = fd, meanCharPerLineCount = True)
