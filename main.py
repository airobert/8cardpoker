# Robert White
# ILLC @ UvA
# ai.robert.wangshuai@gmail.com

from agent import *
from strategy import *
import random
import sys
import numpy as np
import matplotlib.pyplot as plt
import datetime
from pulp import *


def play(Matrix, r, c, termi_num):
	count = 0


	def payoff(s, t):
		ep = 0
		for ss in s.support():
			r = 0
			for tt in t.support():
				r += Matrix[ss.value][tt.value] * t.values[tt.value]
			ep += s.values[ss.value] * r
		return ep  


	while count < termi_num : # if after some runs, there is still no winning strategies
		T1 = r.search()
		T2 = c.search()
		flag = False
		if (payoff(T1, r.piN) > 0):
			# it's a winning strategy
			r.NMW |= T1.support()
			flag = True
		if (payoff(T2, c.piN) > 0):
			# it's a winning strategy
			c.NMW |= T2.support()
			flag = True

		if not flag:
			count += 1

		else:
			# we have to compute the new piN for each player this time		


			# create a matrix
			for x in r.NMW:
				print ('r.NMW: ', str(x))
			for y in c.NMW:
				print ('c.NMW: ', str(y))
			size = len(r.NMW)
			M = []
			for i in r.NMW:
				row = [] # a row
				for j in c.NMW:
					row.append(Matrix[i.value][j.value])
				M.append(row)

			print ('matrix')
			print (M)
			
			# TODO : Robert needs to document these
			
			# ------------------- for the row player
			prob = LpProblem("solve", LpMaximize) # the row player is always trying to maximise

			# define size-many variables
			variables = []
			for w in r.NMW:
				x = LpVariable('x'+str(w.value), 0, 1)
				variables.append(x)

			v = LpVariable("v", -100) # what is this 100 value? 

			# Objective 
			prob += v 

			# Constraints
			for j in range(len(c.NMW)):
				acc = 0
				for i in range(len(r.NMW)):
					acc += M[i][j] * variables[i] 
				prob += v <= acc # the column player will always want to minimise

			acc = 0
			for x in variables: 
				acc += x
			prob += acc == 1


			GLPK().solve(prob)
			print ('------------------solving-------------------------')
			# Solution
			r.piN.reset()
			for v in prob.variables():
				for w in r.NMW:
					if v.name == 'x'+ str(w.value) and v.varValue != 0:
						r.piN.values[w.value] = v.varValue
						print (w.value, ' = ', v.varValue)

			print ("objective=", value(prob.objective))
			r.ep = value(prob.objective)
			r.updateAll()

		# count += 1

			# -------------------  for the column player
			prob2 = LpProblem("solve", LpMinimize) # the row player is always trying to maximise

			# define size-many variables
			variables = []
			for w in c.NMW:
				x = LpVariable('y'+str(w.value), 0, 1)
				variables.append(x)

			v = LpVariable("-v", -100) # what is this 100 value? 

			# Objective 
			prob2 += v 

			# Constraints
			for j in range(len(r.NMW)):
				acc = 0
				for i in range(len(c.NMW)):
					acc += -1* M[j][i] * variables[i] 
				prob += v >= acc # the row player will always want to minimise

			acc = 0
			for x in variables: 
				acc += x
			prob += acc == 1


			GLPK().solve(prob)
			print ('------------------solving-------------------------')
			# Solution
			c.piN.reset() 
			for v in prob.variables():
				for w in c.NMW:
					if v.name == 'y'+ str(w.value) and v.varValue != 0:
						c.piN.values[w.value] = v.varValue
						print (w.value, ' = ', v.varValue)

			print ("objective=", value(prob.objective))
			c.ep = -1 * value(prob.objective)
			c.updateAll()

			# test if the minmax theorem holds

			if (r.ep == c.ep * -1):
				print ('r has expected payoff ', r.ep)
				print ('c has expected payoff ', c.ep)
				print ('this was due to the minmax thm')

def make_matrix(n,m):
	matrix = []
	for i in range (n):
		r = []
		for j in range (m):
			r.append(random.randint(-5, 5)) # any number between -5 and 5
		matrix.append(r)
		
	return matrix

def main():
	# zero-sum asymmetric game
	n = 3
	m = 3
	termi = 1

	M = make_matrix(n,m)
	print ('the matrix is')
	print (M)
	print ('start the game!')
	r = Agent(n, ROW) 
	c = Agent(m, COLUMN)
	play(M, r, c, termi)



if __name__ == "__main__":
	main()