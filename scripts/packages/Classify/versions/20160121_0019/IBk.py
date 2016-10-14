from Distance import Distance

class IBk(object):

	def __init__(self):
		self.examples = None

	def train(self, dataSet, trainAll = False):
		if trainAll == True:
			self.examples = dataSet.getExample()
		elif trainAll == False:
			self.examples = dataSet.getTestTrainSet()

	def test(self, data = None, i = 3):
		if data is None: return None

		#print n
		functions = {
					"hamming":   	Distance().hamming, 	"h": Distance().hamming, 		0: Distance().hamming,
					"levenshtein": 	Distance().levenshtein, "l": Distance().levenshtein, 	1: Distance().levenshtein,
					"chebyshev": 	Distance().chebyshev, 	"c": Distance().chebyshev, 		2: Distance().chebyshev,
					"euclidean": 	Distance().euclidean, 	"e": Distance().euclidean, 		3: Distance().euclidean,
					"manhattan": 	Distance().manhattan, 	"m": Distance().manhattan, 		4: Distance().manhattan
					}

		#print self.examples
		#distances = [functions[d](n, x[:-1]) for x in self.examples]

		#print self.examples[distances.index(min(distances))][-1]

		results = list()

		for x in self.examples:
			results.append(functions[i](data, x.getValues()))

		return enumerate(results)

	def classify(self, data = None, i = 3):
		results = self.test(data, i)
		results = sorted(results, key = lambda x:x[1])[:3]
		results = [self.examples[r].getLabel() for r,n in results]

		print results

		kernel  = set(results)
		kernel  = [(k, results.count(k)) for k in kernel]
		kernel  = sorted(kernel, key = lambda x:x[1], reverse = True)
		print kernel
		return kernel[0][0]


if __name__=="__main__":
	from DataSet import DataSet
	f = "/Users/ducrix/Documents/Research/Python/data/ml/test_weather.gla"
	ds = DataSet(f)

	k = IBk()
	"""
	f1 = [1, 9, 10, 100, 77, 1]
	f2 = [2, 8, 13, 105, 70, 1]
	f3 = [3, 7, 16, 110, 63, 1]
	f4 = [4, 6, 19, 115, 56, 1]
	f5 = [5, 5, 22, 120, 49, 1]
	f6 = [6, 4, 25, 125, 42, 0]
	f7 = [7, 3, 28, 130, 35, 0]
	f8 = [8, 2, 31, 135, 28, 0]
	f9 = [9, 1, 34, 140, 21, 0]

	f0 = [f1,f2,f3,f4,f5,f6,f7,f8,f9]
	fn = list()

	fu = [8, 3, 31, 123, 49]
	"""
	k.train(ds)
	#print k.examples
	print k.classify([1,1,2])