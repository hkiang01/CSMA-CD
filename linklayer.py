#!/usr/bin/python

import sys
from random import randint

class Node:
	def __init__(self, ID=-1):
		self.ID = ID
		self.backoff = -1
		self.currRange = 0
	def setBackoff(self, R):
		self.backoff = randint(0,R)
	def countDown(self):
		self.backoff = self.backoff-1;
	def setRange(self, newRange):
		self.currRange = newRange

class Channel:
	def __init__ (self, args):
		(N,L,R,M,T) = args
		self.numNodes = N
		self.packetSize = L
		self.ranges = R # a list
		self.maxAttempt = M
		self.simTime = T
		self.channelOccupied = 0
		self.utilCount = 0
		self.idleCount = 0
		self.nodes = []
		for i in range(self.numNodes+1):
			self.nodes.append(Node(i))
	def occupyChannel(self, nodeID):
		self.channelOccupied = nodeID
	def freeChennel(self):
		self.channelOccupied = 0
	def getOccupiedPct(self):
		return self.occupiedCount/(self.occupiedCount + self.idleCount)
	def getIdlePct(self):
		return self.idleCount/(self.idleCount + self.occupiedCount)
	def initNodes(self):
		for node in self.nodes:
			node.setRange(self.ranges[0])
			node.setBackoff(node.currRange)	
			print node.backoff
def parse(filename):
	f = open(filename, "r")
	lines = f.readlines()
	numNodes = 0
	packetSize = 0
	ranges = []
	maxAttempts = 0
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
			for i in xrange(1, len(curr), 1):
				# print "range: " + curr[i]
				ranges.append(int(curr[i]))
		elif(curr[0] == "M"):
			# print "maxAttempts: " + curr[1]
			maxAttempts = int(curr[1])
		elif(curr[0] == "T"):
			# print "simTime: " + curr[1]
			simTime = int(curr[1].replace(',', ''))
		else:
			print "Error: Invalid input file"
	# print "numNodes: " + str(numNodes)
	# print "packetSize: " + str(packetSize)
	# print "ranges: " +  '[%s]' % ', '.join(map(str, ranges))
	# print "simTime: " + str(simTime)
	result = []
	result.append(numNodes)
	result.append(packetSize)
	result.append(ranges)
	result.append(maxAttempts)
	result.append(simTime)
	f.close()
	return result

def main():
	args = parse("input.txt")
	for arg in args:
		 print str(arg)
	channel = Channel(args)

	channel.initNodes()
	


if __name__ == '__main__':
	main();

