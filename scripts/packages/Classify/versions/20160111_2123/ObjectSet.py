class ObjectSet(object):

	def __init__(self):
		self.data = list()
		self.index = 0

	def __getitem__(self, key):
		return self.data[key]

	def __len__(self):
		return len(self.data)

	def __iter__(self):
		return self

	def next(self):
		try:
			self.index += 1
			return self.data[self.index-1]
		except(IndexError, KeyError):
			self.index = 0
			raise StopIteration