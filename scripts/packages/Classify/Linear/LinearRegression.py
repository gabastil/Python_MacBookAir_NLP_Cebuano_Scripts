import math

class LinearRegression(object):

	def __init__(self, x, y):

		self.mean_x = self.mean(x)
		self.mean_y = self.mean(y)

		self.x = x
		self.y = y

		self.x_difference = self.difference(x, self.mean_x)
		self.y_difference = self.difference(y, self.mean_y)

		self.x_squared = self.squared(x, self.mean(x))
		self.x_times_y = self.multiply(self.x_difference, self.y_difference)

		self.b_1 = sum(self.x_times_y)/sum(self.x_squared)
		self.b_0 = self.mean_y - (self.mean_x*self.b_1)

		self.estimated_values = [self.getValueOf(x_value) for x_value in self.x]

		print "X:", self.x_difference, self.mean(x)
		print "Y:", self.y_difference, self.mean(y)
		print "x squared:", self.x_squared
		print "x times y:", self.x_times_y
		print "b_0", self.b_0
		print "b_0", self.getValueOf(3)
		print "Estimated Value:", self.estimated_values
		print "R-Squared:", self.getRSquared()
		print "Standard Error:", self.getSquaredError()

	def mean(self, vector):
		return sum(vector)/(len(vector)*1.)

	def difference(self, vector, mean):
		return [value-mean for value in vector]

	def squared(self, vector, mean):
		return [value**2 for value in self.difference(vector, mean)]

	def multiply(self, x, y):
		return [x[i]*y[i] for i in xrange(len(x))]

	def getValueOf(self, x):
		return self.b_0 + (self.b_1*x)

	def getRSquared(self):
		actual_difference = sum(self.squared(self.y, self.mean_y))
		estimate_difference = sum(self.squared(self.estimated_values, self.mean_y))
		return estimate_difference/actual_difference

	def getSquaredError(self):
		estimated_actual_difference = [self.estimated_values[i]-self.y[i] for i in xrange(len(self.y))]
		squared_estimated_actual_difference = [value**2 for value in estimated_actual_difference]

		numerator = sum(squared_estimated_actual_difference)
		denominator = len(self.y)-2

		return math.sqrt(numerator/denominator)


if __name__=="__main__":
	LR = LinearRegression([1,2,3,4,5], [2,4,5,4,5])

	xes = [1,2,3,4,5]
	#for x in xes:
	#	print LR.getValueOf(x)
