# Robert White
# ILLC @ UvA
# ai.robert.wangshuai@gmail.com

# Yang Xu
# University of Liverpool
# Y.Xu58@student.liverpool.ac.uk

import random
import copy

ROCK = 0
PAPER = 1
SCISSORS = 2

class PureStrategy (object):

	def __init__ (self, step = None):
		if (step == None):
			self.step = random.choice([ROCK, PAPER, SCISSORS])
		else:
			self.step = step


	def convertToMixed(self):
		return MixedStrategy(self.step)

	def __str__(self): # override the default printing function
		if (self.step == ROCK):
			return 'ROCK'
		elif (self.step == PAPER):
			return 'PAPER'
		else:
			return 'SCISSORS'

	def __eq__(self, other): 
		return (self.step == other.step)

	def __hash__(self):
		return self.step


class MixedStrategy (object):

	def __init__(self, pure = None):
		self.d = {}
		if (pure != None): 
			self.d[pure] = 1

	def support(self):
		l = set()
		for step in self.d.keys():
			if self.d[step] != 0:
				l.add(PureStrategy(step))
		return l

	def __str__(self):
		s = ''
		for v in self.d.keys():
			if self.d[v] != 0: 
				s += str(v) + ' > '+str(self.d[v])[:5] + ' |\n'
		return s

	def reset(self):
		self.d = {} 

	def expectedPayoff(self, other): 
		return 1