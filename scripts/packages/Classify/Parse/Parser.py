#!/usr/bin/python
# -*- coding: UTF-8 -*-
# GOLD: THIS CLASS IS FINISHED
# Glenn Abastillas, November 28, 2015 @ 17:47
# UPDATED 2015/12/08: Optimized loops and functions in loops

__author__ = "Glenn Abastillas"

class Parser(object):
	"""
	Parse extracts sentences, phrases, or tokens from a text.

	1. Sentences are extracted based on the following punctuation: '.', '?', '!'. A space after each of these is required for the parses to correctly extract sentences.
	2. Phrases are extracted based on the output of the Parse.sentences() parser. A space after each of the phrasal punctuation is required for the parses to correctly extract phrases. If no subphrases are found, the sentence is returned as a phrase.
	3. Tokens are extracted based on spaces, i.e., " ".
	"""

	def __init__(self, text = None):
		self.numbers 			= {	'1',	'2',	'3',	'4',	'5',	'6',	'7',	'8',	'9',	'0'}		# These are numbers that are presented or ignored.
		self.punct_sentences 	= {	'.', 	'?', 	'!', 	'\n'}														# These punctuation are used to parse sentences.
		self.punct_phrases   	= {	'.', 	'?', 	'!', 	'"', 	'\'', 	',', 	';', 	':', 	'-', 	''}			# These punctuation are used to parse phrases.
		self.punct_general	 	= {	',', 	'.',  	'?', 	'!', 	'\'', 	'\"', 	'`', 	';', 	':', 	'—',		# These are general punctuation.
									'-', 	'--', 	'_', 	'+', 	'=', 	'@', 	'#', 	'$', 	'%', 	'^', 
									'&', 	'*', 	'(', 	')', 	'/', 	'\\', 	'<', 	'>', 	'[', 	']', 
									'{', 	'}', 	'|', 	'', 	'”', 	'“', 	'‘', 	'`', 	'…', 	'@'}

		self.dict 				= {'@': ['at'], 'cm': ['centimeter']}
		self.dict_contractions 	= {	"i'm": 		"i am", 	"im": 		"i am", 	"i'll": 	"i will",	"you'll": 	"you will",
									"you're": 	"you are", 	"youre": 	"you are", 	"you'll": 	"you will",	"he's": 	"he is", 	
									"she's": 	"she is"}

		self.text = text	#This text is the text to be parsed

	def sentences(self, text = None, punc = False, lc = False):
		# Parses text into sentences. If "include" is "True", punctuation in the list is included.

		if text is None:
			text = self.text

		listOfSentences = []
		lastIndex 		= 0

		append 		 = listOfSentences.append
		lower 		 = str.lower
		removeSpaces = self.removeSpaces

		for i in xrange(len(text)):
			if text[i] in self.punct_sentences:
				if (text[i] == '.') and (i + 1 != len(text)) and (text[i + 1] != " "):
					"""-------------------------------------------------------------------""
					# If the punctuation is a period '.' and the next character is:
					# not longer than the length of the text and
					# it is not a blank space:
					# then, the period is probably part of the word.
					# Therefore, pass.
					""-------------------------------------------------------------------"""
					pass

				elif (i + 1 != len(text)) and (text[i] == '.') and (text[i+2] in self.numbers): 
					"""-------------------------------------------------------------------""
					# If the counter 'i' is not longer than the text and
					# the current character is a period '.'
					# and the character two away is a number, then it is probably a date:
					# pass date constructed like: mon. dd, yyyy
					""-------------------------------------------------------------------"""
					pass

				elif (i > 2) and (text[i] == '.') and (text[i-2] == '.'):
					"""-------------------------------------------------------------------""
					# If the counter 'i' is greater than 2 and
					# the current character is a period '.' and
					# two characters behind is also a period:
					# This is probably part of a word, pass.
					""-------------------------------------------------------------------"""
					#print text[i]
					pass

				elif (i > 2) and (text[i] == '.') and (text[i-2] == ' '):
					"""-------------------------------------------------------------------""
					# If the counter 'i' is greater than 2 and
					# the current character is a period '.' and
					# two characters behind is a space:
					# This is probably part of a word, pass.
					""-------------------------------------------------------------------"""
					pass

				elif text[i] == "\n":
					"""-------------------------------------------------------------------""
					# If the current text is a new line '\n', then
					# this is a sentence boundary.
					""-------------------------------------------------------------------"""

					s = text[lastIndex:i]
					s = removeSpaces(s)

					if (set(s) == set(" ")) or (len(set(s)) < 1):
						"""-------------------------------------------------------------------"
						# If this set is empty, pass
						""-------------------------------------------------------------------"""
						pass

					else:
						"""-------------------------------------------------------------------"
						# If this set is not empty, it contains a sentence
						""-------------------------------------------------------------------"""
						append(s)
						
					lastIndex = i + 1
				else:
					if punc is True:
						s = text[lastIndex:i+1]
					else:
						s = text[lastIndex:i]

					if lc == True:
						s = lower(s)

					s = removeSpaces(s)

					append(s)
					lastIndex = i + 2

		return listOfSentences

	def phrases(self, text = None, punc = False, lc = False):
		# Parses text into phrases. First, it extracts sentences. Then it parses the sentences further into phrases.
		# Sentences without subphrases are appended as a whole to the list.

		def clip(term):
			if term[0] == ' ' and term[-1] == ' ': return term[1:-1]
			elif term[0] == ' ': return term[1:]
			elif term[-1] == ' ': return term[:-1]
			else: return term

		if text is None:
			text = self.text

		sentences = self.sentences(punc = punc, text = text, lc = lc)

		listOfPhrases = []

		append = listOfPhrases.append

		for s in sentences:
			lastIndex 	 	 = 0
			phrasesAdded 	 = 0
			setOfApostrophes = False
			
			for i in xrange(len(s)):

				if s[i] in self.punct_phrases:
					if i + 1 == len(s):
						break

					elif (i > 2) and (s[i] == '.') and (s[i-2] == '.'):	#skip over initials constructed like: X.X.
						pass

					elif (i > 2) and (s[i] == ',') and (s[i-1] and s[i+2] and s[i+3]) in self.numbers:	#skip over dates constructed like: XX, XXXX
						pass

					elif s[i] in {'\'', '"', '`'}  and s[i-1] == " " and setOfApostrophes == False:
						setOfApostrophes = not setOfApostrophes

					elif s[i+1] == " ":
						if s[i] in {'\'', '"', '`'} and setOfApostrophes == True:
							setOfApostrophes = not setOfApostrophes
							pass
						else:
							if s[i-1] == 's' and setOfApostrophes == False:
								pass
							else:
								p = s[lastIndex:i]

								append(clip(p))
								
								lastIndex = i+1
								phrasesAdded += 1

				if phrasesAdded == 0 and i + 1 == len(s):
					append(clip(s))
					break

				elif phrasesAdded > 0 and i + 1 == len(s):
					p = s[lastIndex:i+1]
					append(clip(p))
					break

		return listOfPhrases

	def tokens(self, text = None, punc = False, lc = False):
		# Parses text into individual tokens. If "include" is "True", then punctuation +/-1 distance away from last letter is included. Otherwise, it is removed.
		# "lc" makes the output all lower case. "uc" makes the outpute all upper case.

		if text is None:
			text = self.text

		listOfTokens = []

		append 		= listOfTokens.append
		cleanText 	= self.cleanText
		lower 		= str.lower

		for t in text.split():

			if lc == True:
				t = lower(t)

			if punc == False:

				try:
					if type(float(t[0])) == type(float):
						pass
				except(ValueError):
					t = cleanText(t)

			if len(t) > 0:
				append(t)

		return listOfTokens

	def removeSpaces(self, string):
		if len(string) < 1:
			return string
		elif string == " ":
			return string

		if string[0] == " ":
			string = string[1:]

		if string[-1] == " ":
			string = string[:-1]

		return string

	def cleanText(self, text):
		if len(text) < 1:
			return text
		elif text == " ":
			return text

		replace = str.replace

		for punc in self.punct_general:
			if punc in text:
				text = replace(text, punc, "")

		return text

if __name__ == "__main__":
	t = "kana ang ..akong \"giingon\" nimo; ayaw ug buhat niana 2.4 pa. kahibalo ba ka unsa akong giingon nimo? but do you know what's happening. There are, you know, many different things to see here."
	dataSource = "/Users/ducrix/Documents/Research/Python/data/ceb2.txt"
	#data = "this is a test text sample. It should contain a good good good amount of words because it has to be use for a test. I am going to try to use as full of words as possible possible possible."
	t = open(dataSource, 'r').read()

	p = Parser(t)
	print "Tokens: ", p.tokens(punc = False)
	print "Sentences: ", p.sentences()
	print "Phrases: ", p.phrases()
	print "testestt for the testing".find('t')
	#print p.cleanText(t)
