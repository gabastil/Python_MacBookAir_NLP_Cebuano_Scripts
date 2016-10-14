#!/usr/bin/env Python
# -*- coding: utf-8 -*-
#
#	Name:		Key.py
#	Author:		Glenn Abastillas
#	Version:	1.0.0
#	Date:		May 14, 2016
#
"""	holds information for an encryption or decryption key

The Key object inherits all methods from the Matrix class except for the
getType() method, which returns the Key object's matrix dimensions. The key
is used as part of the Cryptographer class to encrypt or decrypt a string.
Key objects are created by reading in a text file and feeding each line into
a new Key object, which are then initialized as matrix objects.
"""

from Matrix import Matrix

class Key(Matrix):

	def __init__(self, line, delimiter='\t'):
		""" initialize this key object with a String line input
			@param	line: String line input (example format: #,#	#,#)
		"""
		super(Key, self).__init__()

		# split the line into vectors
		vectors = [row.split(',') for row in line.split(delimiter) if len(row) > 0]

		# loop through the vectors and change string values to float before adding to matrix
		for vector in vectors:

			row = list()
			appendToRow = row.append

			for value in vector:
				try:
					appendToRow(float(value))
				except ValueError:
					appendToRow(float(ord(value)))

			self.append(row)

		self.type = "{}x{}".format(len(self.matrix), len(self.matrix[0]))
		self.validate()

	def getType(self):
		""" get key's dimensions
			@return	String in #x# format
		"""
		return self.type

	def validate(self):
		""" validate key by checking determinant
			@return	True if valid, False if invalid
		"""
		if self.getDeterminant()==0:
			raise ValueError("Key is invalid or corrupt.")
		return True

if __name__=="__main__":
	keys = "./data/Keys3-x.txt"

	with open(keys, 'r') as keysFile:
		keysIn = keysFile.read().split('\n')

	for key in keysIn:
		K = Key(key)
		print "Key", K.matrix

	print K.getType()
	print K.matrix
	print K.getAdjugate().matrix
	print K.getDeterminant()
	print (K.getInverse()*K).matrix
	#print dir(K)