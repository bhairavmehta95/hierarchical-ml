from math import sqrt


class Node:
	def __init__(self, key, feature_vector=None, is_root=False):
		self.key = key
		self.is_root = is_root
		''' 
		Definition of Feature Vector:
		Index	:	Description
		0		:	Feature 1
		1		:	Feature 2
		2		:	Feature 3
		'''
		self.feature_description = ['F1', 'F2', 'F3']
		self.score = 0.0

		self.parent = None
		self.children = 0
		self.depth = len(key)

		if feature_vector:
			self.feature_vector = feature_vector
		else:
			self.feature_vector = [0, 0, 0]


	def __str__(self):
		return "Key: {}, Score: {}".format(self.key, self.score)


	def update_features(self):
		self.feature_vector = [x + 1 for x in self.feature_vector]


	def calculate_score(self):
		self.score = sqrt(sum(self.feature_vector + [self.depth]) / len(self.feature_vector))


	def print_info(self):
		print("Key: {}, Score: {}".format(self.key, self.score))


	def serialize(self):
		serialized_node = dict()
		serialized_node['key'] = self.key
		serialized_node['is_root'] = self.is_root
		serialized_node['score'] = self.score
		serialized_node['depth'] = self.depth
		serialized_node['feature_vector'] = self.feature_vector
