class Leaf(object):

	def __init__(self, examples = None):
		self.labels   = [e.getLabel() for e in examples]
		self.labelSet = [self.labels.count(l) for l in list(set(self.labels))]
		self.label    = self.labels[self.labelSet.index(max(self.labelSet))]

	def getLabel(self):
		return self.label

	def getLabels(self):
		return self.labels

	def isLeaf(self):
		return True
