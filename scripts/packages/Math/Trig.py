#!/usr/bin/env Python
# -*- coding: utf-8 -*-
#
#	Name:		Trig.py
#	Author:		Glenn Abastillas
#	Version:	1.0.0
#	Date:		August 18, 2016
#
"""	A trig class that contains basic trignonometric functions as well as
functions that trig functions rely on to calculate.
"""

class Trig(object):

	def sin(self, rad, max_range=200):
		""" return the sine value at the given radians
			@param	rad: angle in radians
			@param	max_range: maximum iterations in the Taylor series
		"""
		total_sin = 0.

		for n in xrange(max_range):

			coeff = 1/self.fact((2*n)+1)
			x_one = (-1)**(n)
			x_val = (rad)**((2*n)+1)

			total_sin += x_one*coeff*x_val

		return round(total_sin, 15)

	def cos(self, rad, max_range=200):
		""" return the cosine value at the given radians
			@param	rad: angle in radians
			@param	max_range: maximum iterations in the Taylor series
		"""
		total_cos = 0.

		for n in xrange(max_range):

			coeff = 1/self.fact(2*n)
			x_one = (-1)**n
			x_val = (rad)**(2*n)

			total_cos += x_one*coeff*x_val

		return round(total_cos, 15)

	def tan(self, rad, max_range=200):
		""" return the tangent value at the given radians
			@param	rad: angle in radians
			@param	max_range: maximum iterations in the Taylor series
		"""
		
		try:
			return self.sin(rad, max_range)/self.cos(rad, max_range)
		except(ZeroDivisionError):
			return "UNDEFINED"

	def fact(self, number):
		""" return the factorial of the specified number
			@param	number: number to evaluate
		"""

		total = 1.

		for n in xrange(number):
			total *= n+1

		return total

	def isOdd(self, number):
		""" return True if number is odd, False otherwise
			@param	number: number to evaluate
		"""

		if number % 2 == 0:
			return False
		return True

if __name__=="__main__":
	import math
	print math.pi, math.cos(math.pi)
	print Trig().fact(0)
	print Trig().cos(math.pi/4)
	print Trig().sin(math.pi/4)
	print Trig().tan(math.pi/2)
	print (1+1j)**10