import numpy
import random
class Node:
	def __init__(self, x, y, population):
		self.x = x
		self.y = y
		self.population = population
class Organism:
	def __init__(self,noNodes,nodesInfo):
		self.fitness=-1
		self.adjMatrix= numpy.zeros((noNodes,noNodes))
		self.edgeWeightMatrix= numpy.zeros((noNodes,noNodes))
		self.shortestPaths= numpy.zeros((noNodes,noNodes))
		for i in range(1,noNodes):
			for x in range(0,i):
				self.adjMatrix[x,i]=random.randint(0,1)
				self.adjMatrix[i,x]=self.adjMatrix[x,i]
				if(self.adjMatrix[x,i]==1):
					self.edgeWeightMatrix[i,x]=((nodesInfo[i].x-nodesInfo[x].x)**2+(nodesInfo[i].y-nodesInfo[x].y)**2)**0.5
					self.edgeWeightMatrix[x,i]=self.edgeWeightMatrix[i,x]
		print(self.adjMatrix)
	def __str__(self):
		return 'Fitness: ' + str(self.fitness)

#Importing the data from the text file
nodeList = []
nodeNo = 0
xSize = 0
ySize = 0
with open("baseStates/nodes.txt","r") as data:
        nodeNo,xSize,ySize=map(int, data.readline().split())
        for i in range(1,nodeNo+1):
                parser=Node(0,0,0)
                parser.x,parser.y,parser.population=map(int, data.readline().split())
                nodeList.append(parser)
        data.close()

#Largest possible distance between two points, NSFW: Magic number (Can't do anything because too lazy to deal with transfinites etc to get the right ordering relation)
largestD=100+(xSize**2+ySize**2)**0.5

#GA Data
population=15
generations=400
test=Organism(nodeNo,nodeList)