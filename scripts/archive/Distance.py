#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Parse.Parse import Parse

class Distance(Parse):

	def __init__(self, text = None):
		super(Distance, self).__init__(text)
		pass

	def indices(self, tokens = True, text = None):
		if text is None:
			text = self.text
		
		if tokens == True:
			text = self.tokens(self.text)

		return range(len(text))

	def distances(self, tokenIndex = 0, tokens = True, text = None):
		if text is None:
			text = self.text

		indices = self.indices(tokens = tokens, text = text)

		print indices

	def lookBack(self, *tokens):
		if len(tokens) < 1:
			return None

		distances = []
		
		T1 = tokens[0]
		T2 = tokens[1:]
		text = self.tokens(self.text, lc = True)

		print text
		print T1, T2

		d1, d2 = None, None

		for i in self.indices(text = text):
			for t in T2:
				if text[i] == t:
					#print "Huzzah, match! ", text[i]
					d2 = i
					#print d2

				if text[i] == T1:
					#print "Idzah, mnitce! ", text[i]
					d1 = i
			
				if d1 is not None and d2 is not None:
					print "append"
					distances.append((t, d1, d2, d2 - d1))
					d2 = None

		return distances



if __name__ == "__main__":
	t = "Hey, this is a sample text. I think that it'll help out if you can include $2.50 in the 'envelope' fors' 'all' of us to use. Is that another way of making the belt?"
	p = Parse(t)
	d = Distance(t)

	print p.phrases()
	#print d.distances(3)
	print d.lookBack("that", "this", "you")