"""
parse		contains code to parse and extracts specified terms from a text.
			to load: from Parse.[module] import [class]
			
			[modules]:
						__init__.py		notify python that this is a package. 				(see scripts)
						Extractor.py	extract context/concordances, pairs, or word lists. (see scripts)
						Parse.py		parse text into sentences, phrases, or tokens. 		(see scripts)
						
=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*

__init__ 	notifies python that container folder is a package

Extractor	extract context/concordances, pairs, or word files.

			[class(es)]	(1) Extractor

			[method(s)]	getContext(word = None, scope = 10, exact = False)
							- gets leading text and trailing text surrounding search term "word".
							- returns: concList = [leading text, search term, trailing text]
								> word:		search term
								> scope:	number of tokens to include in leading and trailing content.
								> exact:	match search term exactly, i.e., case-sensitive search.

						getPairs(word1 = None, word2 = None, includeCount = False, includeSearchTerm = True)
							- gets word pairs adjacent to search terms, i.e., word1, word2, or both
							- returns: pairList = [[word1, word2], [...], ...]
								> word1:				leading anchor, i.e., first position search word
								> word2: 				trailing anchor, i.e., second position search word
								> includeCount:			append count of pairs with each pair, e.g., [[word1, word2, 3], [...], ...]
								> includeSearchTerm:	include the anchor term, e.g., 	if True  and word1 = "sa", [["sa", word2], [...], ...]; 
																						if False and word1 = "sa", [[word2], [...], ...]

						getWordList(lc = True, uc = False)
							- gets a non-duplicate list of all words in the text
							- returns: wordList = [word1, word2, word3, word4, ...]
"""