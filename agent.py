# Robert White
# ILLC @ UvA
# ai.robert.wangshuai@gmail.com

import random
import sys
from pulp import *
from strategy import *

ROW = True
COLUMN = False

class Agent:
	def __init__ (self, size, role):
		self.name = ''
		if role == True:
			self.name == 'Row Player'
		else:
			self.name == 'Column Player'
		self.size = size
		self.piN = PureStrategy(size = size).convertToMixed()
		self.N = set()
		self.M = set()
		self.NMW = set()
		self.W = None
		self.updateAll()

		self.ep = 0 # the default payoff, we will have to check later

	def updateNMW(self):
		self.NMW = set()
		self.NMW |= self.N 
		self.NMW |= self.M 
		if self.W != None:
			self.NMW |= self.W.support()
	
	def updateN(self):
		self.N = self.piN.support()

	def updateM(self):
		self.M = self.NMW - self.N  

	def updateAll(self):
		self.updateN()
		self.updateM()
		self.updateNMW()

	def info(self):
		s = ''
		s += 'name =\t' + self.name + '\n'
		s += 'piN =\t' + str(self.piN) + '\n'
		s += 'N =\t'+str(self.N) + '\n'
		s += 'M =\t'+str(self.M) + '\n'
		return s

	def search (self):
		s = MixedStrategy()
		s.set_random(self.size) 
		return s # every time return only one strategy

