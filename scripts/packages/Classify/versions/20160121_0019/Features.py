from nltk.probability 	import ConditionalFreqDist as cfd
from nltk.probability 	import ConditionalProbDist as cpd
from nltk.probability 	import LidstoneProbDist	 as lpd
from Parse.Parser 		import Parser
import os

class Features(object):


	

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

	print ft.getFeatures(fd)