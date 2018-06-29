import math
import numpy as np
import random

#Classes
class node:
	def __init__(self, x, y, population):
		self.x = x
		self.y = y
		self.population = population

class annealer:
	def __init__(self,temperature,temperatureDecay,temperatureStop,iterationStop):
		self.temperature=temperature
		self.temperatureDecay=temperatureDecay
		self.temperatureStop=temperatureStop
		self.iterationStop=iterationStop

		#Importing the data from the text file
		with open("baseStates/nodes.txt","r") as data:
			self.nodeList=[]
			self.nodeNo,self.xSize,self.ySize=map(int, data.readline().split())
			for i in range(1,self.nodeNo+1):
				parser=node(0,0,0)
				parser.x,parser.y,parser.population=map(int, data.readline().split())
				self.nodeList.append(parser)
			data.close()

		#Initialises the starting adjacency matrix literally by connecting everything to everything else.

		#Calculating some constants.
		#Assuming where [i,k] is the element of the matrix that commuters are travelling from the ith station to the kth station.
		#The amount of people travelling from the ith station to the kth station is equivalent to the population of the ith station multiplied by the fraction that the kth station comprises of the rest of the population.
		self.population=np.zeros((1,self.nodeNo))
		for i in range(self.nodeNo):
			self.population[0,i]=self.nodeList[i].population

		#I... may have been slightly sleep-deprived when I wrote this part. No idea what the hell this does.
		self.magic=np.multiply(self.population,np.transpose(self.population))
		np.fill_diagonal(self.magic,0)

		#What this piece of hot garbage does is that it basically creates a matrix telling you the size of the commuting crowd from the station in the row to the station in the column.
		#I.e. commuterCrowdSize(1,2) is the amount of people travelling from station 1 to station 2.
		self.commuterCrowdSize=np.divide(self.magic,np.tile((np.tile(np.matrix([np.sum(self.population)]),(1,self.nodeNo))-self.population),(self.nodeNo,1)))

		self.iteration=1

		self.currentAdjMatrix= np.full([self.nodeNo,self.nodeNo],1)
		self.currentEnergy=self.energy(self.currentAdjMatrix)
		
		self.bestAdjMatrix=self.currentAdjMatrix
		self.bestEnergy=self.currentEnergy

	#Function to optimise for...
	#I have no idea what the hell I was doing when I wrote this.
	#Suffice to say this is a problem for Future Conrad to untangle.
	def energy(self,currentAdjMatrix):
		shortestPaths = np.full([self.nodeNo,self.nodeNo], np.inf)
		roadDist = np.zeros((self.nodeNo,self.nodeNo))
		for i in range(1,self.nodeNo):
				for x in range(0,i):
					if(currentAdjMatrix[x,i]==1):
						shortestPaths[i,x] = shortestPaths[x,i] = roadDist[i,x] = roadDist[x,i] = ((self.nodeList[i].x-self.nodeList[x].x)**2+(self.nodeList[i].y-self.nodeList[x].y)**2)**0.5
		#The distance of a node to itself should be zero.
		np.fill_diagonal(shortestPaths,0)
		#Calculates shortest path from one node to another using Floyd-Warshall.
		for k in range(self.nodeNo):
			for i in range(self.nodeNo):
				for j in range(self.nodeNo):
					if shortestPaths[i,j] > shortestPaths[i,k] + shortestPaths[k,j]:
						shortestPaths[i,j] = shortestPaths[i,k] + shortestPaths[k,j]
		#The first multiplication sum gives you the total distance travelled by commuters and the second gives you the total distance of road laid.
		#The idea is that we want to get a balanced mix between cost of laying down tracks and commuter efficiency by finding the minimum of their product.
		return np.sum(np.multiply(self.commuterCrowdSize,shortestPaths))*np.sum(roadDist)

	def validEdit(self,editedcurrentAdjMatrix):
		#Checks if the edit made to generate the new candidate is valid.
		#I consider a valid edit to be one that ensures the graph remains fully connected.
		toCheck=[0]
		checked=[]
		while(len(toCheck)!=0):
			checked.append(toCheck[0])
			for i in range(0,self.nodeNo):
				if (editedcurrentAdjMatrix[toCheck[0]][i] == 1 and editedcurrentAdjMatrix[toCheck[0]][i] not in checked):
					toCheck.append(i)
					toCheck.pop(0)
			else:
				toCheck.pop(0)
		if(len(checked)==self.nodeNo):
			return True
		else:
			return False

	def generateCandidate(self,currentAdjMatrix):
		generated=False
		while(generated==False):
			currentAdjMatrixCandidate=currentAdjMatrix
			station1=random.randint(0,self.nodeNo-1)
			station2=random.randint(0,self.nodeNo-1)
			if(currentAdjMatrixCandidate[station1][station2]==0):
				currentAdjMatrixCandidate[station1][station2]=1
				currentAdjMatrixCandidate[station2][station1]=1
				if(self.validEdit(currentAdjMatrixCandidate)==True):
					generated=True
			else:
				currentAdjMatrixCandidate[station1][station2]=0
				currentAdjMatrixCandidate[station2][station1]=0
				if(self.validEdit(currentAdjMatrixCandidate)==True):
					generated=True
		return currentAdjMatrixCandidate

	def probability(self,candidate):
		#Probability of accepting solution
		return math.exp(-abs(self.energy(candidate) - self.currentEnergy) / self.temperature)

	def transition(self,candidate):
		#If the candidate's energy value is lower than ours, accept with 100% certainty.
		#If not, accept according to the probability given by the probability function.
		candidateEnergy = self.energy(candidate)
		if candidateEnergy < self.currentEnergy:
			self.currentEnergy = candidateEnergy
			self.currentAdjMatrix = candidate
			if candidateEnergy < self.bestEnergy:
				self.bestEnergy = candidateEnergy
				self.bestAdjMatrix = candidate

		else:
			if random.random() < self.probability(candidate):
				self.currentEnergy = candidateEnergy
				self.currentAdjMatrix = candidate

	def anneal(self):
		while self.temperature >= self.temperatureStop and self.iteration < self.iterationStop:
			candidate = self.generateCandidate(self.currentAdjMatrix)
			self.transition(candidate)
			self.temperature *= self.temperatureDecay
			self.iteration += 1

simAnneal=annealer(1000,0.99,10,4000)
simAnneal.anneal()
