# Robert White
# ILLC @ UvA
# ai.robert.wangshuai@gmail.com

# Yang Xu
# University of Liverpool
# Y.Xu58@student.liverpool.ac.uk

import random
import sys
from pulp import *
from strategy import *

class Agent:
	def __init__ (self, name, CARDSIZE):
		self.name = name
		self.CARDSIZE = CARDSIZE
		self.piN = MixedStrategy()
		self.N = self.piN.support()
		self.M = set()
		self.NMW = set ()
		self.W = None

	def updateNMW(self):
		self.NMW =set()
		self.NMW |= self.N 
		self.NMW |= self.M 
		if self.W != None:
			self.NMW |= self.W.support()
	def updateN(self):
		self.N = self.piN.support()

	def updateM(self):
		self.M = self.NMW - self.N

	def info(self):
		s = ''
		s += 'name =\t' + self.name + '\n'
		s += 'piN =\t' + str(self.piN) + '\n'
		s += 'N =\t'+str(self.N) + '\n'
		s += 'M =\t'+str(self.M) + '\n'
		return s


