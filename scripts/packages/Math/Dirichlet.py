#!/usr/bin/env Python
# -*- encoding: utf-8 -*-

import math, numpy
import matplotlib.pyplot as plt

class Dirichlet(object):

	def __init__(self, *alphas):
		self.alphas = list()

		if alphas is not None:

			total_alphas = sum(alphas) * 1.

			self.alphas = [a/total_alphas for a in alphas]

		print self.alphas

	def getProbability(self, *outcomes):
		"""	calculate the probability of outcomes based off the multinomial dist
			@param	outcomes:	list of discrete outcomes
			@return	float probability
		"""

		sum_outcomes = sum(outcomes)
		sum_outcomes_factorial = math.factorial(sum_outcomes)

		product_outcomes_factorial = 1.
		product_outcomes_probabilities = 1.

		# loop through the outcomes and probabilities to get their products
		for o in xrange(len(outcomes)):
			product_outcomes_factorial *= math.factorial(outcomes[o])
			product_outcomes_probabilities *= self.alphas[o]**outcomes[o]

		probability = (sum_outcomes_factorial/product_outcomes_factorial) * product_outcomes_probabilities
		#probability = (sum_outcomes_factorial/product_outcomes_factorial) * product_outcomes_probabilities

		return probability

if __name__=="__main__":
	n = 25
	d = Dirichlet(*[3,3,3])
	p = [d.getProbability(i, n-i,i) for i in xrange(n)]
	#print p
	plt.scatter(range(n), p)
	plt.show()



