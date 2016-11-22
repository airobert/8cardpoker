# Robert White
# ILLC @ UvA
# ai.robert.wangshuai@gmail.com

import random
import copy

class PureStrategy (object):

	def __init__ (self, size = 0, value = -1):
		self.value = 0
		if value == -1:
			self.value = random.randint(0, size-1) # any number in this range
		else:
			self.value = value

	def convertToMixed(self):
		m = MixedStrategy()
		m.values[self.value] = 1
		return m

	def __str__(self): # override the default printing function
		return str(self.value)

	def __eq__(self, other): 
		return (self.value == other.value)

	def __hash__(self):
		return self.value


class MixedStrategy (object):

	def __init__(self):
		self.values = {}

	def set_random(self, size):
		pc = {}
		total = 0
		for i in range(size):
				c = random.randint(0, size-1)
				rd = random.randint(1, 5)
				if c in pc.keys():
					pc[c] = pc[c] + rd
				else:
					pc[c] = rd 
				total += rd 
		for p in pc.keys(): 
			self.values[p] = pc[p] / total 

	def support(self):
		l = set()
		for k in self.values.keys():
			if self.values[k] != 0:
				l.add(PureStrategy(value = k))
		return l

	def __str__(self):
		s = ''
		for v in self.values.keys():
			if self.values[v] != 0: 
				s += str(v) + ' > '+str(self.values[v])[:5] + ' |\n'
		return s

	def reset(self):
		self.values = {}

