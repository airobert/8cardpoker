# Robert White
# ILLC @ UvA
# ai.robert.wangshuai@gmail.com

# from agent import *
import random
import sys
# from strategy import *
from pulp import *

import numpy as np
import matplotlib.pyplot as plt

import datetime
@profile
def solve(M):
	size = 9
	names = range (size)
	result = [0] * size
	
	prob = LpProblem("solve", LpMaximize) # the row player is always trying to maximise

	# define size-many variables
	variables = []
	for i in range(size):
		# print ('w as '+str(w))
		x = LpVariable('x'+str(names[i]), 0, 1) 
		variables.append(x)

	v = LpVariable("v", 0)

	# Objective
	prob += v

	# Constraints
	for i in range(size):
		acc = 0
		for j in range(size):
			acc += M[j][i] * variables[j] 
		prob += v <= acc # the column player will always want to minimise

	acc = 0
	for x in variables:
		acc += x
	prob += acc == 1


	# GLPK().solve(prob)
	prob.solve()
	if (LpStatus[prob.status] == 'Infeasible'):
		print('There is no solution because you can not add more weight on a particular player without adding more weight on the other. ')
	else:
		print ('------------------solving-------------------------')
		# Solution
		vectors = [] 
		probabilities = [] 

		for v in prob.variables():
			print ('decoding ', v.name, v.varValue)
			if (v.name[0] == 'x'):
				index = int(v.name[1])
				print ('index = ', index)
				result[index] = v.varValue

		print ("objective=", value(prob.objective))
		
		for i in range(size):
			print ('result = ', result[i])


def main():
	meanM = []
	TERMI = 40
	ITER = 10

	# M = [[0,-1,1], [1,0,-1], [-1,1,0]] # can be solved using naive method
	M = [[0,-2,3], [1,0,-2], [-1,1,0]] # can't be solved using naive method
	# Status: Infeasible

	size = 9
	E = []
	for i in range (size):
		row = []
		for j in range (size):
			R1 = int(i/3)
			R2 = i%3
			C1 = int(j/3)
			C2 = j%3
			row.append(M[R1][C2] + M[C1][R2])
		E.append(row)
	for row in E:
		print (row)

	solve(E)


if __name__ == "__main__":
	main()
