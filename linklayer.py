#!/usr/bin/python

import sys

class Node:
	def __init__(self, ID=-1):
		self.ID = ID
		self.backoff = -1
	def setBackoff(self, R):
		self.backoff = randint(0,R)
	def countDown(self):
		self.backoff = self.backoff-1;

class Channel:
	def __init__ (self, N, L, R, M, T):
		self.numNodes = N
		self.packetSize = L
		self.ranges = R # a list
		self.maxAttempt = M
		self.simTime = t
		self.channelOccupied = 0
		self.utilCount = 0
		self.idleCount = 0
	def occupyChannel(self, nodeID):
		self.channelOccupied = nodeID
	def freeChennel(self):
		self.channelOccupied = 0
	def getOccupiedPct(self):
		return self.occupiedCount/(self.occupiedCount + self.idleCount)
	def getIdlePct(self):
		return self.idleCount/(self.idleCount + self.occupiedCount)

def parse(filename):
	f = open(filename, "r")
	lines = f.readlines()
	numNodes = 0
	packetSize = 0
	ranges = []
	simTime = 0
	for line in lines:
		#grab initialization vars
		curr = line.split(" ")
		if(curr[0] == "N"):
			# print "numNodes: " + curr[1]
			numNodes = int(curr[1])	
		elif(curr[0] == "L"):
			# print "packetSize: " + curr[1]
			packetSize = int(curr[1])
		elif(curr[0] == "R"):
			for i in xrange(1, len(curr)-1, 1):
				# print "range: " + curr[i]
				ranges.append(int(curr[i]))
		elif(curr[0] == "M"):
			# print "maxAttempts: " + curr[1]
			maxAttempts = int(curr[1])
		elif(curr[0] == "T"):
			# print "simTime: " + curr[1]
			simTime = int(curr[1])
		else:
			print "Error: Invalid input file"
	print "numNodes: " + numNodes
	print "packetSize: " + packetSize
	print "ranges: " +  '[%s]' % ', '.join(map(str, ranges))
	print "simTime: " + simTime

def main():
	print "test"
	parse("input.txt")

	for i in xrange(10):
		print "iteration"
	
if __name__ == '__main__':
	main();

