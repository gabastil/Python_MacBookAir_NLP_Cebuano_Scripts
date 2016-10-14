#!/usr/bin/env Python
# -*- coding: utf-8 -*-
#
#	Name:		Matrix.py
#	Author:		Glenn Abastillas
#	Version:	1.0.0
#	Date:		May 9, 2016
#
"""	mathematical Matrix object supporting matrix operations

This object creates a mathematical Matrix and supports matrix operations such
as matrix Addition, Subtraction, Multiplication and Transposition. This class
also allows the user to derive the determinant and inverse of this matrix.

@date	2016/05/11 - Matrix is unable to provide co-matrices at this point
"""

import copy

class Matrix(object):

	def __init__(self, rows=None, columns=None):
		""" Initiate an empty Matrix object. The matrix is oriented to have
			rows as sub-lists. For example, ([row 1], [row 2],..., [row n]).
			Otherwise, object is initialized with row and column numbers.
		"""
		self.matrix = list()
		self.transposed = False
		self.empty = True
		self.row_size = 0
		self.col_size = 0

		self.index = 0

		append = self.matrix.append

		# if the user specifies a matrix size, initialize one
		if type(rows)==type(int()) and type(columns)==type(int()):
			
			# for each row, add a list of columns length
			for row in xrange(rows):
				append([0] * columns)

			self.empty = False

			self.row_size = rows
			self.col_size = columns

		# if the user specifies the rows to go into the matrix, add them
		elif type(rows)==type(list()) or type(rows)==type(self):

			# for each row, add it to the matrix
			for row in rows:
				append(row)

			self.empty = False

			self.row_size = len(row)
			self.col_size = len(self.matrix[0])

	def __add__(self, matrix):
		""" add two matrices together
			@param	matrix: matrix to add
			@return Matrix object
		"""
		return self.add(matrix)

	def __div__(self, matrix):
		"""	divide two matrices
			@param	matrix: matrix divisor
			@return	Matrix object
		"""
		return self.multiply(matrix.getInverse())

	def __eq__(self, matrix):
		""" check equality with another matrix
		"""
		return self.matrix==matrix.matrix

	def __getitem__(self, key):
		"""	provide support for indexing
			@param	key: index of data to retrieve
			@return	row at key
		"""
		return self.matrix[key]

	def __getslice__(self, i, j):
		""" get a slice of the matrix
			@param	i: starting index
			@param	j: ending index
			@return	select rows from the matrix
		"""
		return self.matrix[i:j]

	def __len__(self):
		"""	provide length of matrix in number of rows
			@return	integer length of matrix
		"""
		return len(self.matrix)

	def __mul__(self, matrix):
		"""	multiply two matrices
			@param	matrix: matrix multicand
			@return	Matrix object
		"""
		return self.multiply(matrix)

	def __rmul__(self, matrix):
		"""	multiply two matrices
			@param	matrix: matrix multicand
			@return	Matrix object
		"""
		return matrix.multiply(self.getMatrix())

	def __setitem__(self, i, item):
		"""	set row in matrix to another item
			@param	item: list to replace list in matrix
		"""
		self.matrix[i] = item

	def __setslice__(self, i, j, item):
		""" set several rows to new items
			@param	i: starting index
			@param	j: ending index
			@param	item: list to replace list in matrix
		"""
		self.matrix[i:j] = item

	def __sub__(self, matrix):
		""" subtract two matrices
			@param	matrix: matrix to subract
			@return Matrix object
		"""
		return self.subtract(matrix)

	def __iter__(self):
		"""	allow for iteration over this object
			@return self
		"""
		return self

	def next(self):
		""" returns the next object when object is iterated against
			@return	next item in self.matrix
		"""
		try:
			self.index += 1
			return self.matrix[self.index-1]
		except(IndexError, KeyError):
			self.index = 0
			raise StopIteration

	def add(self, matrix):
		""" add the input matrix to this matrix
			@param	matrix: input matrix to add to existing matrix
			@return	Matrix object
		"""
		if (len(matrix) != len(self.matrix)) and (len(matrix[0]) != len(self.matrix[0])):
			raise ValueError("Matrices of different sizes. m-by-n is not the same as n-by-k.")

		outputMatrix = Matrix()
		appendToOutput = outputMatrix.append

		# loop through rows
		for i in xrange(self.row_size):

			vector = list()
			appendToVector = vector.append

			# loop through columns
			for j in xrange(len(self.matrix[i])):

				appendToVector(self.matrix[i][j]+matrix[i][j])

			appendToOutput(vector)

		return outputMatrix

	def append(self, vector):
		""" append a new row/column to the matrix
			@param	row: new row to be added
		"""
		#print "VECTOR:\t", vector
		if not self.empty and (len(vector) != self.col_size):
			raise ValueError("Vector has the incorrect number of values. Vector needs {} values.".format(self.row_size))

		self.matrix.append(vector)
		self.empty = False

		self.row_size = len(self.matrix)
		self.col_size = len(self.matrix[0])
		#print "Matrix.append\t", vector, len(vector)

	def clear(self):
		""" make matrix a zero matrix
		"""
		# loop through the columns
		for i in xrange(self.row_size):

			# loop through the rows and set i,r to 0
			for r in xrange(len(self.matrix)):

				self.set(r, i, 0)

	def dotMultiply(self, vector1, vector2):
		""" dot multiply two vectors
			@param	vector1: list of values
			@param	vector2: list of values
			@return	double scalar
		"""

		if len(vector1) != len(vector2):
			raise ValueError("Vectors of different sizes.")

		scalar = 0.0

		for i in xrange(len(vector1)):
			scalar += (vector1[i]*vector2[i])
			##print "\t", scalar

		return scalar

	def getAdjugate(self):
		""" get adjugate for this matrix if 2x2
			@return	Matrix object of adjugate
		"""
		self.toRows()

		if self.row_size==2 and len(self.matrix)==2:
			adjugate = Matrix()
			append = adjugate.append

			append([self.matrix[1][1], -self.matrix[0][1]])
			append([-self.matrix[1][0], self.matrix[0][0]])

			return adjugate
		
		else:
			adjugate = self.getMinors()
			adjugate.transpose()
			return adjugate

	def getDeterminant(self, matrix=None):
		"""	get the determinant of this matrix
			@param	matrix: input Matrix object
			@return	integer determinant
		"""

		if matrix is None:
			matrix = self.getMatrix(True)

		# if matrix is 2x2, return determinant
		if matrix.getRowSize()==2:

			a = matrix.get(0,0)
			b = matrix.get(0,1)

			c = matrix.get(1,0)
			d = matrix.get(1,1)

			return (a*d)-(b*c)

		else:

			determinant = 0

			# loop through the top row of the matrix > 2x2 and get determinants from minor matrices
			for i in xrange(matrix.getColSize()):

				minorMatrix = Matrix(matrix)

				minorMatrix.removeRow(0)
				minorMatrix.removeCol(i)

				# if i%2 is not 0, then make the sign of the product of the determinant and value negative
				if i%2!=0:
					determinant += -self.getDeterminant(minorMatrix) * matrix.get(0, i)
				else:
					determinant += self.getDeterminant(minorMatrix) * matrix.get(0, i)

			return determinant

	def getMatrix(self, asList=False):
		""" get this object's matrix
			@return	list of matrix
		"""
		matrix = list()

		if asList==True:
			matrix = Matrix()

		append = matrix.append

		for row in self.matrix:
			append(row)

		return matrix

	def getMinors(self, matrix=None):
		""" get a matrix of minors for matrices larger than 2x2
			@param	matrix:	input matrix of size 3x3 or larger
			@return	Matrix object with determinants of sub-matrices
		"""
		
		if matrix is None:
			matrix = self.getMatrix(True)

		minors = Matrix()

		# loop through rows
		for i in xrange(matrix.getRowSize()):

			r = list()

			# loop through columns
			for j in xrange(matrix.getColSize()):

				minor_matrix = Matrix(matrix)
				minor_matrix.removeRow(i)
				minor_matrix.removeCol(j)
				
				determinant = self.getDeterminant(minor_matrix)

				# apply negative sign to determinant if i,j in negative zone
				# according to the checkerboard patter [+,-,+,...,+]
				if (i%2!=0 and j%2==0) or (i%2==0 and j%2!=0):
					determinant = -determinant

				r.append(determinant)

			minors.append(r)

		return minors

	def getInverse(self):
		"""	get inverse matrix for this matrix
			@return	Matrix object
		"""
		# create a temporary matrix and make transformations
		adjugate = self.getAdjugate()

		# get cofactor
		try:
			cofactor = 1./self.getDeterminant()
		except ZeroDivisionError:
			# raise error
			raise ZeroDivisionError("There is no cofactor for this matrix.")

		# scale matrix with cofactor
		adjugate.scale(cofactor)

		return adjugate

	def get(self, row, col):
		""" get the indicated row in the matrix
			@param	row: row index
			@param	col: column index
			@return	single value
		"""
		return self.matrix[row][col]

	def getCol(self, col):
		"""	get the indicated column in the matrix
		"""
		if self.transposed:
			return self.matrix[col]

		self.toColumns()

		column = self.matrix[col]

		self.toRows()

		return column

	def getColSize(self):
		"""	get the number of columns in matrix
			@return	integer indicating number of columns
		"""
		return self.col_size

	def getRow(self, row):
		""" get the indicated row in the matrix
			@param	row: row index
			@return	list row of values
		"""
		if not self.transposed:
			return self.matrix[row]

		self.toRows()

		row = self.matrix[row]

		self.toColumns()

		return row

	def getRowSize(self):
		"""	get the number of rows in matrix
			@return	integer indicating number of rows
		"""
		return self.row_size

	def isEmpty(self):
		""" see if matrix is empty
		"""
		return self.empty

	def multiply(self, matrix, sigfig=3):
		""" multiply this matrix by input matrix
			@param	matrix: matrix or scalar value
			@param	sigfig: number of significant figures to round to
			@return	Matrix object
		"""
		outputMatrix = Matrix()
		appendToOutput = outputMatrix.append

		#if len(self.matrix[0])!=len(matrix):
		#	raise ValueError("Matrix sizes are incompatible: m-by-n needs n-by-k matrix. This Matrix: {}x{}\tInput: {}x{}".format(self.row_size, len(self.getRow(0)), matrix.size, len(matrix.getRow(0))))

		#print "In Matrix Object; multiply method:\t", self.matrix

		# loop through the rows in the matrix
		for matrixRow in self.matrix:

			outputRow = list()
			appendToRow = outputRow.append

			# loop through the columns of the input matrix
			for column in xrange(len(matrix[0])):

				inputMatrixColumn = [inputMatrixRow[column] for inputMatrixRow in matrix]

				if sigfig is None:
					appendToRow(self.dotMultiply(inputMatrixColumn, matrixRow))
				else:
					appendToRow(round(self.dotMultiply(inputMatrixColumn, matrixRow), sigfig))

			appendToOutput(outputRow)

		return outputMatrix

	def removeRow(self, row):
		""" delete a row
			@param	row: row index
		"""
		if not self.transposed:
			del self.matrix[row]

		else:
			self.toRows()
			del self.matrix[row]
			self.toColumns()

	def removeCol(self, col):
		""" delete a column
			@param	col: column index
		"""
		if self.transposed:
			del self.matrix[col]

		else:
			#print "Before to columns:", self.matrix
			self.toColumns()
			#print "After to columns:", self.matrix
			del self.matrix[col]
			self.toRows()

	def reset(self):
		""" empty this matrix object and reset values
		"""
		self.matrix = list()
		self.transposed = False
		self.empty = True
		self.row_size = 0

	def toIntegers(self, significantFigures = 0):
		"""	convert values in matrix to integers
			@param	significantFigures: significant figures to round off to
		"""
		for i in xrange(self.row_size-1):

			print "ROUND", self.matrix[i], len(self.matrix[i])
			for j in xrange(len(self.matrix[i])):

				if significantFigures == 0:
					self.matrix[i][j] = int(round(self.matrix[i][j]))
				else:
					self.matrix[i][j] = round(self.matrix[i][j], significantFigures)

	def save(self, name="matrix.mx", location="./data", offset=0, delimiter=';'):
		"""	save matrix as a text file
			@param	location: path to storage location
		"""

		outputMatrixString = ""

		# loop through each row to make the vector a string to append to file
		for row in self.matrix:
			
			row = [fig-offset for fig in row]
			row = str(row).replace(' ', '')
			row = row[1:-1]

			#row = [hex(int(fig)) for fig in row]
			outputMatrixString += "{}{}".format(row, delimiter)

		matrixOut = open("{}/{}".format(location,name), 'w')
		matrixOut.write(outputMatrixString)

	def scale(self, scalar):
		"""	scale the values of this matrix
			@param	scalar: number to scale the values of this matrix
		"""
		scaledMatrix = list()
		appendToScaledMatrix = scaledMatrix.append

		for row in self.matrix:

			vector = list()
			appendToVector = vector.append

			for value in row:
				appendToVector(scalar*value)

			appendToScaledMatrix(vector)

		self.matrix = scaledMatrix

	def set(self, row, col, value):
		""" set a cell in the matrix to a value
			@param	row: row index
			@param	col: column index
		"""
		self.matrix[row][col] = value

	def setMatrix(self, matrix):
		"""	set this matrix to another matrix
			@param	matrix: matrix to set this object to
		"""

		self.matrix = matrix
		self.emtpy = False
		self.row_size = len(matrix)

	def subtract(self, matrix):
		""" subtract the input matrix to this matrix
			@param	matrix: input matrix to subtract from existing matrix
			@return	Matrix object
		"""
		if (len(matrix) != len(self.matrix)) and (len(matrix[0]) != len(self.matrix[0])):
			raise ValueError("Matrices of different sizes. m-by-n is not the same as n-by-k.")

		outputMatrix = Matrix()
		appendToOutput = outputMatrix.append

		# loop through rows
		for i in xrange(self.row_size):

			vector = list()
			appendToVector = vector.append

			# loop through columns
			for j in xrange(len(self.matrix[i])):

				appendToVector(self.matrix[i][j]-matrix[i][j])

			appendToOutput(vector)

		return outputMatrix

	def toRows(self):
		""" set matrix to rows (i.e., transposed==False)
		"""
		if self.transposed:
			self.transpose()

	def toColumns(self):
		""" set matrix to columns (i.e., transposed==True)
		"""
		if not self.transposed:
			self.transpose()

	def toString(self, format=1):
		"""	print matrix to screen as a string
		"""
		if format==1:
			rowsList = [str(row).replace(", ", "\t") for row in self.matrix]
			#print "\n".join(rowsList)
			return "\n".join(rowsList)
		else:
			rowsList = [str(row).replace(", ", ",")[1:-1] for row in self.matrix]
			#print "\t".join(rowsList)
			return "\t".join(rowsList)

	def transpose(self):
		""" make rows columns and vice versa
		"""
		newMatrix = list()
		appendToMatrix = newMatrix.append

		# loop through the columns
		for i in xrange(self.col_size):

			newVector = list()
			appendToVector = newVector.append

			# loop through rows and get ith element
			for r in self.matrix:
				#print r, i, self.row_size, self.col_size, r[i]
				appendToVector(r[i])

			appendToMatrix(newVector)

		self.matrix = newMatrix
		self.row_size = len(self.matrix)
		self.col_size = len(self.matrix[0])
		self.transposed = not self.transposed

if __name__=="__main__":
	"""
	m = Matrix()
	m.append([1,2,3,4])
	print m.matrix
	m.append([1,2,3,6])

	print "\n{}{}{}\n".format("-"*25,"2x2 Matrix Test: adding values with .set()","-"*25)
	n = Matrix(4,3)
	n.set(0,0,11); n.set(0,1,11); n.set(0,2,11)
	n.set(1,0,22); n.set(1,1,22); n.set(1,2,22)
	n.set(2,0,33); n.set(2,1,33); n.set(2,2,33)
	print n.matrix, n.getRowSize()
	n.transpose()
	print n.matrix, n.getRowSize()
	n.toRows()
	print n.matrix, n.getRowSize()
	n.toColumns()
	n.clear()
	print n.matrix, n.getRowSize()
	n.transpose()
	#n.delRow(1)
	print n.matrix, n.getRowSize()

	p = Matrix([[1,2], [5,6]])
	print p.matrix
	print p.get(1,1), p.getRow(0)
	k = p.getInverse()
	print "Determinant ", p.getDeterminant()
	print "INVERSE\t", k, "MATRIX\t", p.matrix, "ADJUNCT\t", p.getAdjugate()
	print "multiply\n", p.multiply(k).toString(), p.scale(6), p.toString()
	print "ROW AND COL", p.getRowSize(), p.getColSize()

	print p.toString()
	p.reset()
	print "AFTER RESET:", p.toString()

	print "\n{}{}{}\n".format("-"*25,"2x2 Matrix Test: Encrypting and Decrypting","-"*25)
	key1 = Matrix([[0,2],[4,6]])
	key2 = Matrix([[8,10],[4,2]])

	message = Matrix([[8,5,12],[12,15,0]])

	N = key1.multiply(message)
	N.matrix = [[0.0, 0.0, 24.0, 30.0, 0.0], [104.0, 110.0, 48.0, 0.0, 0.0]]
	M = key2.multiply(N)

	def decrypt(message, key1, key2):
		key1inverse = key1.getInverse()
		key2inverse = key2.getInverse()
		print key1inverse.matrix, key2inverse.matrix
		dN = key2inverse.multiply(message)
		dN.matrix = [dN.matrix[0][2:], dN.matrix[1][:-2]]
		dN = key1inverse.multiply(dN.matrix)
		print "DN", dN.matrix
		dN.toIntegers()
		print dN.matrix, round(dN.matrix[0][0])

	print "M", M.matrix
	decrypt(M, key1, key2)

	key3 = key1.add(key2)

	print "POST", key3.add(key2).getMatrix()
	print key3.subtract(key2).matrix
	key3.clear()
	print key3.getMatrix()
	print "NN", key1.matrix, key2.matrix
	O = key1 * key2
	Q = key1 - key2
	S = key1/key2
	O.toString()
	Q.toString()
	S.toString()

	print "Y"
	Y = Matrix(S)
	Y.toString()
	#Y[0:2] = [[1,2],[3,4]]
	Y.toIntegers()
	print "DONE\n", Y.matrix, Y

	print "\n{}{}{}\n".format("-"*25,"2x2 Matrix Test","-"*25)
	
	two_by_two = Matrix([[0,2],[3,5]])

	print "Original Matrix:\t", two_by_two.getMatrix()
	print "Determinant:\t\t", two_by_two.getDeterminant()
	print "Adjugate:\t\t\t", two_by_two.getAdjugate().getMatrix()
	print "Inverse:\t\t\t", two_by_two.getInverse().getMatrix()
	print "M-1*M:\t\t\t\t", two_by_two.getInverse().multiply(two_by_two.getMatrix()).matrix
	"""
	print "\n{}{}{}\n".format("-"*25,"3x3 Matrix Test","-"*25)
	
	three_by_three = Matrix([[1,9,-4],[3,5,9],[5,2,2]])

	print "Original Matrix:\t", three_by_three.getMatrix()
	print "Matrix of Minors:\t", three_by_three.getMinors().getMatrix()
	print "Determinant:\t\t", three_by_three.getDeterminant()
	#print "Comatrix:\t\t\t", three_by_three.getComatrix().getMatrix()
	print "Adjugate:\t\t\t", three_by_three.getAdjugate().getMatrix()
	print "Inverse:\t\t\t", three_by_three.getInverse().getMatrix()
	print "M-1*M:\t\t\t\t", three_by_three.getInverse().multiply(three_by_three.getMatrix()).matrix

	#four_by_four = Matrix([[0,2,1,4],[1,3,4,2],[0,0,1,0],[2,0,1,4]])
	four_by_four = Matrix([[1,0,0,1],[0,2,1,2],[2,1,0,1],[2,0,1,4]])

	print "\n{}{}{}\n".format("-"*25,"Mutiple Regression: Linear Regression Test","-"*25)

	X = Matrix([[1,-2, 1], [1,-1, 2], [1, 0, 3], [1, 2, 4], [1, 4, 5]])
	Y = Matrix([[0],[1], [2], [4], [5]])
	Xt = Matrix(X.getMatrix())
	Xt.transpose()

	print "X.toString(): ", X.toString(), '\n'
	print Xt.toString()
	print Y.toString()
	
	XtX = Xt * X
	XtY = Xt * Y
	print XtX.matrix, XtY.matrix
	print XtX.getDeterminant()
	print "XtX: row and col size", XtX.getRowSize(), XtX.getColSize()
	SOL = (XtX.getInverse() * XtY)
	SOL.transpose()

	print SOL.toString()
	print "Check work: ", SOL.dotMultiply(SOL.getCol(0), Xt.getRow(0))
	print "Check work: ", SOL.dotMultiply(SOL.getCol(0), Xt.getRow(1))
	print "Check work: ", SOL.dotMultiply(SOL.getCol(0), Xt.getRow(2))
	#print "Check work: ", SOL.dotMultiply(SOL.getCol(0), Xt.getRow(3))
	#print "Check work: ", SOL.dotMultiply(SOL.getCol(0), Xt.getRow(4))
	#print SOL.dotMultiply(SOL.getCol(0), Xt.getRow(2))
	print "\n{}{}{}\n".format("-"*25,"Uneven matrices","-"*25)

	M1 = Matrix([[1,2,3,4],[1,2,3,2]])
	#M2 = Matrix([[1,2,3,4,5,5,6],[1,2,3,4,5,5,6],[1,2,3,4,5,5,6],[1,2,3,4,5,5,6]])
	M2 = Matrix(M1.getMatrix()); M2.transpose()

	print (M1 * M2).getInverse().matrix

	print M1
	print M1.getMatrix()

	print "\nTHREE_BY_THREE:\t"
	print three_by_three.matrix

	tbtm = three_by_three.getInverse()
	print tbtm.matrix
	print (tbtm*three_by_three).matrix

	print "\nFOUR_BY_FOUR:\t"
	print four_by_four.matrix

	fbfm = four_by_four.getInverse()
	print "inverse", fbfm.matrix
	print "M^-1 * M", (fbfm*four_by_four).matrix

	print "\nFIVE_BY_FIVE:\t"

	five_by_five = Matrix([[1,9,0,1,1],[2,3,9,1,1],[2,9,4,5,6],[0,9,0,1,2],[0,4,3,1,2]])

	print five_by_five.getMatrix()
	fvbf = five_by_five.getInverse()
	print fvbf.matrix
	print (fvbf * five_by_five).matrix


	print "---------	SOLVE	EQUATION	---------"
	Y = Matrix([[-9,-6,3,-2,1,2]])
	X = Matrix([[1,1,1,1,1,1],[-8,-3,-2,-1,3,4]])
	Xt = Matrix(X)
	Xt.transpose(); Y.transpose()
	print "X-matrix", X.toString()
	print "Xt-matrix", Xt.toString()
	print "Y-matrix", Y.toString()
	XtX = (X*Xt)
	XtY = (X*Y)
	XtXY = XtX.getInverse()*XtY

	for i in xrange(len(Xt)):
		print "\tX: ", Xt.get(i,1), "\tY: ",  Y.get(i,0), "\tYh: ", (XtXY.get(0,0)+ (XtXY.get(1,0)*Xt.get(i,1)))