#!/usr/bin/python

import sys
from random import randint

class Node:
	def __init__(self, ID=-1, maxAttempts=0):
		self.ID = ID
		self.maxAttempts = maxAttempts
		self.backoff = -1
		self.currRange = 0
		self.tryCount = 0
		self.isAwake = True
	def setBackoff(self, R):
		self.backoff = randint(0,R)
	def countDown(self):
		self.backoff = self.backoff-1;
	def setRange(self, newRange):
		self.currRange = newRange
	def collision(self):
		if(self.isAwake):
			self.tryCount = self.tryCount + 1
			if(self.tryCount >= self.maxAttempts):
				self.isAwake = False
			# todo: itereate range (need access to ranges array)
			# todo: new random number based on new range (access same array)

class Channel:
	def __init__ (self, args):
		(N,L,R,M,T) = args
		self.numNodes = N
		self.packetSize = L
		self.ranges = R # a list
		self.maxAttempts = M
		self.simTime = T
		self.channelOccupied = 0
		self.utilCount = 0
		self.idleCount = 0
		self.nodes = []
		self.collisions = 0
		for i in range(self.numNodes+1):
			self.nodes.append(Node(i, self.maxAttempts))
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
	def tick(self):
		zerolist = []
		for node in self.nodes:
			if(node.backoff==0):
				zerolist.append(node)
			node.countDown()
		if(len(zerolist) != 0):
			# zerolist[0] will own the channel
			channelOccupied = zerolist[0].ID
			self.collisions += len(zerolist) - 1
			for i in xrange(1, len(zerolist), 1):
				zerolist[i].collision()

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
	for simulation in xrange(0, channel.simTime):
		channel.tick()


if __name__ == '__main__':
	main();

