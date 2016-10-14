#!/usr/bin/env Python
# -*- coding: utf-8 -*-
#
#	Name:		LinearRegression.py
#	Author:		Glenn Abastillas
#	Version:	1.0.0
#	Date:		June 1, 2016
#
"""	class calculates the regression line for multivariate data
"""
import sys, math
from Matrix import Matrix
sys.path.append("..")
from Document.Document import Document

class LinearRegression(object):

	def __init__(self, data=None, degree=1):
		""" initialize object
			@param	data: path to data file
			@param	degree: degree of polynomial to solve (e.g., quadratic)
		"""

		self.independent_variables = Matrix()
		self.dependent_variables = Matrix()
		self.coefficients = list()

		# make sure degree is at least 1
		if degree < 1:
			degree = 1

		# if data is specified, load it and set independent and dependent variables accordingly
		if data is not None:
			document = Document().open(filePath=data,splitLines=True,splitTabs=True)

			append_to_independent_variables = self.independent_variables.append
			append_to_dependent_variables = self.dependent_variables.append

			# loop through the rows in the document to get data
			for row in document:
				new_row = [float(value) for value in row]
				
				dependent_variable_row = [new_row[-1]]
				independent_variable_row = [new_row[0]**i for i in xrange(degree+1)]
				#print independent_variable_row, new_row, dependent_variable_row

				#append_to_independent_variables(new_row[:-1])
				append_to_independent_variables(independent_variable_row)
				#append_to_dependent_variables(new_row[-1:])
				append_to_dependent_variables(dependent_variable_row)

			#print self.independent_variables.matrix
			self.coefficients = self.getCoefficients([self.independent_variables, self.dependent_variables])

	def getCoefficients(self, data=None):
		"""	solve for the coefficient weights from the data
			@param	data:	list of independent and dependent variables
			@return list of coefficients
		"""

		# if data is specified, set X and Y matrices to it
		if data is not None:
			X = data[0].getMatrix(True)
			Y = data[1].getMatrix(True)

			Xt = data[0].getMatrix(True)
			Xt.transpose()

		# set X and Y matrices to object's data if none specified
		else:
			X = self.independent_variables.getMatrix(True)
			Y = self.dependent_variables.getMatrix(True)

			Xt = self.independent_variables.getMatrix(True)
			Xt.transpose()


		XtX = (Xt*X).getInverse()
		XtY = Xt*Y

		coefficients = XtX*XtY
		coefficients.transpose()

		return coefficients[0]

	def getResiduals(self):
		residuals = list()
		append = residuals.append

		for i in xrange(len(self.independent_variables)):

			y = self.dependent_variables[i][0]
			y_estimated = 0

			for j in xrange(len(self.coefficients)):
				y_estimated += self.coefficients[j]*self.independent_variables[i][j]

			append(y-y_estimated)

		return residuals

	def getRSquared(self):
		mean = self.getMean(self.dependent_variables)

		residuals = self.getResiduals()

		residual_variation = [r**2 for r in residuals]
		total_variation = [(y[0]-mean)**2 for y in self.dependent_variables]

		return 1-(sum(residual_variation)/sum(total_variation))

	def getCorrelationCoefficient(self):
		return math.sqrt(self.getRSquared())

	def getMean(self, data=None, predictor=0):
		if data is None:
			data = self.independent_variables

		total = len(self.independent_variables)
		predictor_sum = 0.

		for row in data:
			predictor_sum += row[predictor]

		#print predictor_sum
		return predictor_sum

	def predictValue(self, *independent_variable):

		independent_variable = [1] + list(independent_variable)
		independent_variable = [independent_variable[1]**exponent for exponent in xrange(len(self.independent_variables[0])+1)]

		#print independent_variable

		coefficients = self.coefficients

		expected_value = [coefficients[j]*independent_variable[j] for j in xrange(len(self.independent_variables[0]))]
		expected_value = sum(expected_value)
		print expected_value

	def test(self, coefficients=None):

		if coefficients is None:
			coefficients = self.coefficients

		for i in xrange(len(self.dependent_variables)):

			x = sum([coefficients[j] * self.independent_variables[i][j] for j in xrange(len(self.independent_variables[i]))])

			#print "Actual: ", self.dependent_variables[i], "\tExpected: ", x, "\tResidual: ", self.dependent_variables[i][0]-x

if __name__=="__main__":

	datafile = "./data/sample_data.txt"
	LR = LinearRegression(datafile, 7)

	#print LR.getCoefficients()
	#LR.getResiduals()
	#LR.getMean()
	#print LR.getRSquared(), LR.getCorrelationCoefficient()
	#X = LR.independent_variables.getMatrix(True)
	#Xt = LR.independent_variables.getMatrix(True); Xt.transpose()
	#Y = LR.dependent_variables
	#print "X matrix", X.matrix
	#print "Y matrix", Y.matrix

	#X1 = (Xt*X).getInverse()

	#print (Xt*X).matrix, (Xt*Y).matrix, X1.matrix
	#print ((Xt*X).getInverse()*(Xt*Y)).matrix, LR.getCoefficients()
	#print "xtx", (Xt*X).matrix
	#print "xtx.minors", (Xt*X).getMinors().matrix
	#print "xt", Xt.getMinors().matrix
	#print "xt.determinant", (Xt*X).getDeterminant()
	#LR.test()
	LR.predictValue(-9)
	LR.predictValue(-7)
	LR.predictValue(-4)
	LR.predictValue(-2)
	LR.predictValue(-1)
	LR.predictValue(1)
	LR.predictValue(2)
	LR.predictValue(4)
	LR.predictValue(7)
	LR.predictValue(9)
