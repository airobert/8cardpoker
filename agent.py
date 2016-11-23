# Robert White
# ILLC @ UvA
# ai.robert.wangshuai@gmail.com

import random
import sys
from pulp import *
from strategy import *
from pulp import *
import uuid

ROW = True
COLUMN = False

class Agent:
	def __init__ (self, size, role):
		self.role = ROW
		self.size = size
		self.piN = MixedStrategy()
		self.piN.set_random(self.size)
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

	def searchBest(self, Matrix, OpponentChoices):
		
		prob = LpProblem("solve" + str(uuid.uuid4()), LpMaximize) 
		
		# define size-many variables
		variables = []
		for w in range (self.size):
			x = LpVariable('x'+str(w), 0, 1)
			variables.append(x)

		v = LpVariable("v", -100) # what is this 100 value? 

		# Objective 
		prob += v 

		# Constraints
		acc = 0
		for k in OpponentChoices.values.keys():
			ac = 0
			for i in range(self.size):
				
				if (self.role == ROW):
					ac += Matrix[i][k] * variables[i]
				else :
					ac += Matrix[k][i] * variables[i] * -1
			acc += ac * OpponentChoices.values[k]

		prob += v == acc

		acc = 0
		for x in variables: 
			acc += x
		prob += acc == 1


		GLPK().solve(prob)
		print ('------------------Best Response calculating -------------------------')
		response = MixedStrategy()
		# Solution
		for v in prob.variables():
			for w in range (self.size): 
				if v.name == 'x'+ str(w) and v.varValue != 0:
					response.values[w] = v.varValue
					# print (w.value, ' = ', v.varValue)
		return response




