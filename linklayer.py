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
	def occupyChannel(self, nodeID):
		self.channelOccupied = nodeID
	def freeChennel(self):
		self.channelOccupied = 0

def parse(filename):
	f = open(filename, "r")
	lines = f.readlines()
	for line in lines:
		#grab initialization vars
		print line

def main():
	print "test"
	parse("input.txt")

	for i in xrange(10):
		print "iteration"
	
if __name__ == '__main__':
	main();

