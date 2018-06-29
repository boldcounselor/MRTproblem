import numpy as np
import random

#Classes
class node:
	def __init__(self, x, y, population):
		self.x = x
		self.y = y
		self.population = population

class organism:
	def __init__(self,nodeNo):
		self.fitness=-1
		self.adjMatrix= np.zeros((nodeNo,nodeNo))
		for i in range(1,nodeNo):
			for x in range(0,i):
				self.adjMatrix[x,i]=random.randint(0,1)
				self.adjMatrix[i,x]=self.adjMatrix[x,i]
	def __str__(self):
		return 'Fitness: ' + str(self.fitness)

#Importing the data from the text file
nodeList = []
nodeNo = 0
xSize = 0
ySize = 0
population=np.zeros((nodeNo,1))
with open("baseStates/nodes.txt","r") as data:
        nodeNo,xSize,ySize=map(int, data.readline().split())
        for i in range(1,nodeNo+1):
                parser=node(0,0,0)
                parser.x,parser.y,parser.population=map(int, data.readline().split())
                nodeList.append(parser)
        data.close()

#Calculating some constants.
#Assuming where [i,k] is the element of the matrix that commuters are travelling from the ith station to the kth station.
#The amount of people travelling from the ith station to the kth station is equivalent to the population of the ith station multiplied by the fraction that the kth station comprises of the rest of the population.
population=np.zeros((1,nodeNo))
for i in range(nodeNo):
	population[0,i]=nodeList[i].population

magic=np.multiply(population,np.transpose(population))
np.fill_diagonal(magic,0)

#This is the part where you can prepare the noose if you're refactoring the code.
commuterCrowdSize=np.divide(magic,np.tile((np.tile(np.matrix([np.sum(population)]),(1,nodeNo))-population),(nodeNo,1)))

#Genetic algorithm settings
population=15
generations=400
cutoff=0.2

#Genetic algorithm functions
def ga():
	organisms = init_organisms(population, nodeNo)
	for generation in range(generations):
		print("Generation: " + str(generations))
		organisms = fitness(organisms)
		organisms = selection(organisms)
		organisms = crossover(organisms)
		organisms = mutate(organisms)

def init_organisms(population, nodeNo):
	return [organism(nodeNo,nodesInfo) for _ in range(population)]

def fitnessCalc(adjMatrix,nodeNo,nodesInfo):
	shortestPaths = np.full([nodeNo,nodeNo], np.inf)
	roadDist = np.zeros((nodeNo,nodeNo))
	for i in range(1,nodeNo):
			for x in range(0,i):
				if(adjMatrix[x,i]==1):
					shortestPaths[i,x] = shortestPaths[x,i] = roadDist[i,x] = roadDist[x,i] = ((nodesInfo[i].x-nodesInfo[x].x)**2+(nodesInfo[i].y-nodesInfo[x].y)**2)**0.5
	np.fill_diagonal(shortestPaths,0)
	for k in range(nodeNo):
		for i in range(nodeNo):
			for j in range(nodeNo):
				if shortestPaths[i,j] > shortestPaths[i,k] + shortestPaths[k,j]:
					shortestPaths[i,j] = shortestPaths[i,k] + shortestPaths[k,j]
	return np.sum(np.multiply(commuterCrowdSize,shortestPaths))*np.sum(roadDist)

def fitness(organisms):
	for organism in organisms:
		organism.fitness = fitnessCalc(organism.adjMatrix,nodeNo,nodesInfo)
	return organisms

def selection(organisms):
	organisms = sorted(organisms, key=lambda organism: organism.fitness)
	organisms = organisms[:int(cutoff*len(organisms))]

def crossover(organisms):
	childs = []
	for _ in range((population - len(organisms))/2):
		daddy = random.choice(organisms)
		mommy = random.choice(organisms)
		son = organism(nodeNo)
		daughter = organism(nodeNo)
		for i in range(nodeNo):
			split=random.randint(i,nodeNo)
		childs.append(son)
		childs.append(daughter)
	organisms.extend(childs)
	return organisms
