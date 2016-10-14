#!/usr/bin/env Python
# -*- coding: utf-8 -*-
#
#	Name:		Crytographer.py
#	Author:		Glenn Abastillas
#	Version:	1.0.0
#	Date:		May 9, 2016
#
"""	allows encryption or decryption of a text file utilizing on Key objects

The Cryptographer class makes use of Matrix and Key classes to encode, decode,
encrypt, and decrypt input text. The Key class is used to hold encryption keys
stored in a Keys.txt file. The Matrix class is used to hold the output of 
various methods such as the encode, decode, encrypt, and decrypt methods. The
order in which these Key classes are utilized are indicated in an Algorithm.txt
file, which indicates which Key to use, their order of use, and any buffering
required to encrypt or decrypt the original text.

Matrix objects are the mainly used to hold and transform encrypted or
decrypted information.
"""

from Matrix import Matrix
from Key import Key

class Cryptographer(object):

	def __init__(self, **kwargs):
		self.keys = self.initializeKey(kwargs['pathToKeys'])
		self.algorithm = self.initializeAlgorithm(kwargs['pathToAlgorithm'])

	def __open(self, fileToOpen):
		"""	open specified file
			@param	fileToOpen: path to file to open
			@return	opened text file
		"""
		with open(fileToOpen, 'r') as inputFile:
			output = inputFile.read().split('\n')

		return output

	def addBuffer(self, matrix, length=2, fill=0.0):
		""" add buffer numbers to the matrix
			@param	matrix: matrix to buffer
			@param	length: length of buffer
			@param	fill: buffer
			@return Matrix object with buffer
		"""
		bufferVector = [float(fill)] * length
		bufferedMatrix = Matrix()
		append = bufferedMatrix.append

		for i in xrange(len(matrix)):
			if i%2==0:
				append(bufferVector + matrix[i])
			else:
				append(matrix[i] + bufferVector)

		#print bufferedMatrix.matrix
		return bufferedMatrix

	def addKey(self, *keys):
		""" add a key to keys list
			@param	keys: list of Key objects
		"""
		# loop through input keys and add to keys list
		for key in keys:
			self.keys.append(key)

	def encrypt(self, matrix):
		""" encrypt a matrix and return an encrypted matrix
			@param	matrix: matrix to encrypt
			@return	Matrix object encrypted
		"""

		# loop through the steps in the algorithm
		for step in self.algorithm:

			# if this step is a tuple, it is a buffer command
			if type(step)==type(tuple()):
				matrix = self.addBuffer(matrix, step[0], step[1])
			else:
				matrix = self.keys[step].multiply(matrix)

		return matrix

	def encryptText(self, text, rows=2):
		""" encrypt text input
			@param	text: text to encrypt
			@return	Matrix object
		"""
		encodedText = self.encode(text, rows)
		encryptedText = self.encrypt(encodedText)
		return encryptedText

	def encode(self, text, rows=2):
		"""	turn text into a codified matrix
			@param	text: input String
			@return	Matrix object
		"""

		intSize = len(text)/rows
		floatSize = len(text)/(rows*1.)

		# if the results from integer division are smaller
		# you need an extra item in the row
		if intSize<floatSize:
			length = intSize+1
		else:
			length = intSize

		encodedMatrix = Matrix()
		append = encodedMatrix.append

		# loop through the intended rows of the matrix
		for i in xrange(rows):

			vector = [0]*length
			
			# loop through the empty vector and set each value as needed
			for j in xrange(len(vector)):

				try:
					# try to encode each character
					vector[j] = ord(text[j])
				except IndexError:
					# if there are no more characters to encode, break loop
					break

			append(vector)
			text=text[j+1:]
		
		return encodedMatrix

	def decrypt(self, matrix, integers=False):
		""" decrypt a matrix and return an decrypted matrix
			@param	matrix: matrix to encrypt
			@return	Matrix object decrypted
		"""

		# loop through the steps in the algorithm in reverse
		for i in xrange(len(self.algorithm)):
			step = self.algorithm[-(i+1)]

			if type(step)==type(tuple()):
				matrix = self.removeBuffer(matrix, step[0])

			else:
				decryptionKey = self.keys[step].getInverse()

				matrix = decryptionKey.multiply(matrix)

		# if the user wants to return integers, values will be rounded and made integers
		if integers==True:
			for i in xrange(len(matrix)):
				newRow = [int(round(value)) for value in matrix[i]]
				matrix[i] = newRow

		return matrix

	def decryptText(self, matrix, integers=False):
		""" decrypt matrix input
			@param	matrix: matrix to decrypt
			@return	String text
		"""
		decryptedText = self.decrypt(matrix, integers)
		decodedText = self.decode(decryptedText)
		return decodedText

	def decode(self, matrix):
		"""	turn a codified matrix into text
			@param	matrix: codified matrix
			@return	String text
		"""
		text = ""

		# loop through the rows in the matrix
		for row in matrix:

			# loop through the values in the row
			for value in row:
				
				# get the character value for each value and append it to text string
				text += unichr(int(value))

		#print text
		return text

	def initializeKey(self, pathToKeys, delimiter='\t'):
		"""	get the keys and create matrices from them
			@param	pathToKeys: path to keys
			@return	List of Matrices
		"""
		keyStringsList = [line for line in self.__open(pathToKeys) if len(line) > 0]

		keys = list()
		append = keys.append

		# loop through each line (i.e. matrix) in the keyStringsList
		for line in keyStringsList:

			# add Key objects
			key = Key(line, delimiter)

			print "Key validation:", key.getDeterminant()
			append(key)

		#print keyStringsList, matrix.matrix, keys
		return keys

	def initializeAlgorithm(self, pathToAlgorithm):
		"""	get the set of rules used for en-/decryption
			@param	pathToAlgorithm: path to algorithm used for en-/decryption
			@return	list of rules
		"""
		algorithmStringsList = [line.split(';') for line in self.__open(pathToAlgorithm) if len(line) > 0]

		algorithmProcedures = list()
		append = algorithmProcedures.append

		# loop through the procedures in the algorithm list
		for procedure in algorithmStringsList:

			# loop through the steps of the procedure
			for steps in procedure:

				# add the keys to use - these are represented as integers
				try:
					append(int(steps))

				# add the buffers to use - these are represented as an arithmetic expression
				except(TypeError, ValueError):
					bufferParameters = steps.split('+')
					append((int(bufferParameters[0]), int(bufferParameters[1])))
		
		#print "List", algorithmStringsList, algorithmProcedures
		return algorithmProcedures

	def openMatrixFile(self, matrixToOpen, offset=0, delimiter=';'):
		""" open specified matrix
			@param	matrixToOpen: path to matrix file to open
			@return Matrix object
		"""
		with open(matrixToOpen, 'r') as inputMatrix:
			output = inputMatrix.read().split(delimiter)

		openedMatrix = Matrix()
		append = openedMatrix.append
		
		# loop through the rows and values to float
		for row in output:
			if len(row) > 0:

				# convert string to float + offset value
				row = [float(value)+offset for value in row.split(',')]
				append(row)

		return openedMatrix

	def removeBuffer(self, matrix, length=2):
		"""	remove buffer numbers from the matrix
			@param	matrix: matrix with buffer to remove
			@param	length: length of buffer
			@return	Matrix object without buffer
		"""
		#print matrix.matrix
		unbufferedMatrix = Matrix()
		append = unbufferedMatrix.append

		for i in xrange(len(matrix)):

			#print "\tMATRIX\t", matrix[i], i, i%2, i%2==0
			#print "\t\t-->\t\t", matrix.matrix
			#print "\t\t-->\t\t", matrix.matrix[i][length:]
			#print "\t\t-->\t\t", matrix.matrix[i][:-length]
			if i%2==0:
				append(matrix[i][length:])
			else:
				append(matrix[i][:-length])

		#print "UNBUFFERED MATRIX:\t", unbufferedMatrix.matrix
		return unbufferedMatrix

	def removeKey(self, index):
		""" remove key object from keys list at specified index
			@param	index: integer of key location
		"""
		del self.keys[index]

	def test(self, matrix):
		"""	test the input and output of a set of keys and algorithms
			@param	matrix: matrix to test against
			@return	boolean True if input and output are the same
		"""

		#print "\nPRE-ENCRYPTION\t", matrix.matrix
		encrypted = self.encrypt(matrix)
		#print "ENCRYPTED", encrypted, encrypted.matrix
		decrypted = self.decrypt(encrypted)
		#print "DECRYPTED", decrypted, decrypted.matrix

		#matrix.set(1,0,3)
		#print encrypted, decrypted, "\nEncrypted equals Decrypted: ", encrypted==decrypted, \
		#"\nDecrypted equals Matrix: ", decrypted==matrix, "\nDecrypted IS matrix: ", decrypted is matrix

if __name__=="__main__":

	C = Cryptographer(pathToKeys="./data/Keys3.txt", pathToAlgorithm="./data/Algorithm.txt")
	#print C.keys[0].matrix
	#print C.keys[1].matrix
	M = C.addBuffer(C.keys[0])
	N = C.keys[0].multiply(M)
	O = C.keys[0].getInverse().multiply(N)
	P = C.removeBuffer(O)
	P.transpose()
	#print "PROCEDURAL RESULTS:\n", M.matrix,'\n', N.matrix, '\n', O.matrix, '\n', P.matrix

	Z = Matrix([[1,0],[0,1]])
	#E = C.encrypt(Z)
	#F = C.decrypt(E, 1)

	#print "\nORIGINAL: ", Z.matrix, "ENCRYPTED: ", E.matrix, "DECRYPTED: ", F.matrix
	#C.test(Z)
	#EM = C.encode("what would happen if we were to write a longer message? How big would this file's size be exactly1234!?wha098234#$&*(@#$)(*&")
	#EM2 = C.encrypt(EM)
	#EM3 = C.decrypt(EM2)
	#C.decode(EM)

	print "\n{}{}{}\n".format('-'*20, "Encrypted (Test.txt)", '-'*20)
	test_txt = open("./data/test.txt", 'r')
	test_txt_read = test_txt.read()
	test_txt.close()

	CM = C.encryptText(test_txt_read,3)
	print "ENCRYPTED TEXT:\t", CM.toString(0)
	CM.save()

	print C.algorithm
	matrixFile = C.openMatrixFile("./data/matrix.mx")
	print "Opened matrixFile:\t", matrixFile.matrix
	print "before wrong keys C.decrypt()", C.decrypt(matrixFile).matrix
	#C.keys = C.initializeKey("./data/Keys3.txt")
	#print "after wrong keys C.decrypt()", C.decrypt(matrixFile).matrix
	print "\n{}{}{}\n".format('-'*20, "Decrypted (Text.txt)", '-'*20)
	print C.decryptText(matrixFile, 1)

	M = Matrix([[0,1],[0,0]])