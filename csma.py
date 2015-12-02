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
		self.ranges = []
		self.numDropped = 0
		self.totalCollision = 0
		self.numSent = 0
	def setBackoff(self):
		self.backoff = randint(0,self.currRange)
	def countDown(self):
		self.backoff = self.backoff-1;
	def setRange(self, newRange):
		self.currRange = newRange
	def setRanges(self,ranges):
		self.ranges = ranges
	def getRange(self,index):
		if(len(self.ranges)==0):
			return 2**index
		if(index>=len(self.ranges)):
			return self.ranges[-1]*(2**(index-len(self.ranges)))
		else:
			return self.ranges[index]
	def setRangeAndBackoff(self):
		self.setRange(self.getRange(self.tryCount))
		self.setBackoff()
	def collision(self):
		self.tryCount = self.tryCount+1
		self.totalCollision+=1
		if(self.tryCount>=self.maxAttempts):
			self.tryCount=0
			self.numDropped = self.numDropped+1
			self.setRangeAndBackoff()
		else:
			self.setRangeAndBackoff()

class Channel:
	def __init__ (self, args):
		(N,L,R,M,T) = args
		self.numNodes = N
		self.packetSize = L
		self.ranges = R # a list
		self.maxAttempts = M
		self.simTime = T
		self.channelOccupied = 0
		self.occupiedTime = 0
		self.occupiedCount = 0
		self.idleCount = 0
		self.nodes = []
		self.collisions = 0
		self.successPackets = 0
		self.totalLocalSent = 0
		self.avgLocalSent = 0.0
		self.totalLocalCollisions = 0
		self.avgLocalCollisions = 0.0
		self.varianceSent = 0.0
		self.varianceCollisions = 0.0
		for i in range(self.numNodes):
			self.nodes.append(Node(i+1, self.maxAttempts))
	def occupyChannel(self, nodeID):
		self.channelOccupied = nodeID
	def freeChannel(self):
		self.channelOccupied = 0
	def getOccupiedPct(self):
		return (float(self.occupiedCount)/float((self.occupiedCount + self.idleCount)))*100.0
	def getIdlePct(self):
		return (float(self.idleCount)/float((self.occupiedCount + self.idleCount)))*100.0
	def getAvgST(self):
		for node in self.nodes:
			self.totalLocalSent += node.numSent
		self.avgLocalSent = float(self.totalLocalSent)/float(len(self.nodes))
	def getVarST(self):
		totalVariance = 0.0
		for node in self.nodes:
			totalVariance += float(self.avgLocalSent-node.numSent)**2.0
		self.varianceSent = float(totalVariance)/float(len(self.nodes))
	def getAvgLocalCollisions(self):
		for node in self.nodes:
			self.totalLocalCollisions += node.totalCollision
		self.avgLocalCollisions = float(self.totalLocalCollisions)/float(len(self.nodes))
	def getVarCollisions(self):
		totalVariance = 0.0
		for node in self.nodes:
			totalVariance += float(self.avgLocalCollisions-node.totalCollision)**2.0
		self.varianceCollisions = float(totalVariance)/float(len(self.nodes))
	def initNodes(self):
		for node in self.nodes:
			node.setRanges(self.ranges)
			node.setRangeAndBackoff()
	def tick(self):
		self.occupiedTime = max(0,self.occupiedTime - 1)
		if(self.occupiedTime == 0): # open channel case
			if(self.channelOccupied!=0):
				self.nodes[self.channelOccupied-1].tryCount=0
				self.nodes[self.channelOccupied-1].setRangeAndBackoff()
				self.successPackets = self.successPackets+1
				self.nodes[self.channelOccupied-1].numSent = self.nodes[self.channelOccupied-1].numSent + 1
				self.channelOccupied = 0
			zerolist = []
			for node in self.nodes:
				#print str(node.ID) + ": " + str(node.backoff)
				if(node.backoff==0):
					zerolist.append(node)
			if(len(zerolist) == 1): # claim the channel case
				self.channelOccupied = zerolist[0].ID
				self.occupiedTime = self.packetSize
				self.occupiedCount+=1
			elif(len(zerolist) > 1): # collisions case
				self.collisions += 1#len(zerolist) - 1
				for i in range(len(zerolist)):
					zerolist[i].collision()
				self.occupiedCount += 1
			else:
				for node in self.nodes:
					node.countDown()
				self.idleCount += 1
		else: # occupied channel case
			self.occupiedCount = self.occupiedCount + 1
	def printResults(self):
		self.getAvgST()
		self.getAvgLocalCollisions()
		self.getVarST()
		self.getVarCollisions()
		print "Channel Utilization percentage: " + str(self.getOccupiedPct())
		print "Channel Idle percentage: " + str(self.getIdlePct())
		print "Total number of collision: " + str(self.collisions)
		print "Variance in number of successful transmissions: " + str(self.varianceSent)
		print "Variance in number of local collisions: " + str(self.varianceCollisions)
	def getResults(self):
		results = ""
		results += (str(self.getOccupiedPct()) + str("\n"))
		results += (str(self.getIdlePct()) + str("\n"))
		results += (str(self.collisions) + str("\n"))
		results += (str(self.varianceSent) + str("\n"))
		results += (str(self.varianceCollisions) + str("\n"))
		return results

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
	# for arg in args:
	# 	 print str(arg)
	channel = Channel(args)

	channel.initNodes()
	for simulation in xrange(0, channel.simTime):
		channel.tick()
		#channel.printResults()
		#raw_input()
	# channel.printResults()

	f = open("output.txt", "w")
	f.write(channel.getResults())
	f.close()

if __name__ == '__main__':
	main();

