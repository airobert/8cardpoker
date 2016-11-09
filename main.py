# Robert White
# ILLC @ UvA
# ai.robert.wangshuai@gmail.com

# Yang Xu
# University of Liverpool
# Y.Xu58@student.liverpool.ac.uk

from agent import *
from strategy import *
import random
import sys
import numpy as np
import matplotlib.pyplot as plt
import datetime

class Team:
	def __init__ (self, agentNum, gameSize):
		self.agents = []

		if agentNum == 2:
			self.agents.append(Agent('Rob', gameSize))
			self.agents.append(Agent('Jan', gameSize))
		else:
			for i in range(agentNum):
				self.agents.append(Agent('agent'+str(i), gameSize))


	def info(self):
		s = 'this team contains two agents: \n'
		for a in self.agents:
			s += a.info() + '\n'
		return s

	# TODO: Yang
	def bestResponse(self): # note that this is differnt from before!!!
		T = []
		for i in self.agents:
			T.append(PureStrategy().convertToMixed())
		return T
	def evaluate(self,T): # corresponds to the G function on page 69
		if len(self.agents) == 2:
			return (T[0].expectedPayoff(self.agents[0].piN)) + (T[1].expectedPayoff(self.agents[1].piN))
		else:
			pass



	def play(self):
		W = []
		T = self.bestResponse()
		if T != []:
			# find W
			if self.evaluate(T) > 0 :
				#update W
				self.agents[0].W = T[1] # player 1
				self.agents[1].W = T[0] # player 2

				self.agents[0].updateNMW()
				self.agents[1].updateNMW()
				# linear programming part
				(self.agents[0].piN, self.agents[1].piN) = self.solve()
				self.agents[0].updateN()
				self.agents[0].updateM()

		else:
			# end of the play
			print ('this is the end!')
			print (self.info())

	def solve(self):
		# I don't know how to solve this. I am confused
		return (MixedStrategy(), MixedStrategy())

		
		
def main():
	size = 8
	team = Team(2, size)

	print (team.info())

	team.play()

if __name__ == "__main__":
	main()