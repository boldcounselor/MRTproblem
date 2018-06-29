import numpy as np
import random

#Classes
class node:
	def __init__(self, x, y, population):
		self.x = x
		self.y = y
		self.population = population

class simAnneal:
	#Some set-up.
	def __init__(self,nodeList,nodeNo,xSize,ySize,adjMatrix):
		#Importing the data from the text file
		with open("baseStates/nodes.txt","r") as data:
			self.self.nodeNo,self.xSize,self.ySize=map(int, data.readline().split())

		for i in range(1,self.nodeNo+1):
			parser=node(0,0,0)
			parser.x,parser.y,parser.population=map(int, data.readline().split())
			nodeList.append(parser)
			data.close()

		#Initialises the starting adjacency matrix randomly. May change to greedy.
		self.adjMatrix= np.zeros((self.nodeNo,self.nodeNo))
		for i in range(1,self.nodeNo):
			for x in range(0,i):
				self.adjMatrix[x,i]=random.randint(0,1)
				self.adjMatrix[i,x]=self.adjMatrix[x,i]

		#Calculating some constants.
		#Assuming where [i,k] is the element of the matrix that commuters are travelling from the ith station to the kth station.
		#The amount of people travelling from the ith station to the kth station is equivalent to the population of the ith station multiplied by the fraction that the kth station comprises of the rest of the population.
		self.population=np.zeros((1,self.nodeNo))
		for i in range(self.nodeNo):
			self.population[0,i]=nodeList[i].population

		#I... may have been slightly sleep-deprived when I wrote this part. No idea what the hell this does.
		self.magic=np.multiply(population,np.transpose(population))
		np.fill_diagonal(magic,0)

		#What this piece of hot garbage does is that it basically creates a matrix telling you the size of the commuting crowd from the station in the row to the station in the column.
		#I.e. commuterCrowdSize(1,2) is the amount of people travelling from station 1 to station 2.
		self.commuterCrowdSize=np.divide(magic,np.tile((np.tile(np.matrix([np.sum(population)]),(1,self.nodeNo))-population),(self.nodeNo,1)))

	#Function to optimise for...
	#I have no idea what the hell I was doing when I wrote this.
	#Suffice to say this is a problem for Future Conrad to untangle.
	def energy(adjMatrix,self.nodeNo,nodesInfo):
		shortestPaths = np.full([self.nodeNo,self.nodeNo], np.inf)
		roadDist = np.zeros((self.nodeNo,self.nodeNo))
		for i in range(1,self.nodeNo):
				for x in range(0,i):
					if(adjMatrix[x,i]==1):
						shortestPaths[i,x] = shortestPaths[x,i] = roadDist[i,x] = roadDist[x,i] = ((nodesInfo[i].x-nodesInfo[x].x)**2+(nodesInfo[i].y-nodesInfo[x].y)**2)**0.5
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
		return np.sum(np.multiply(commuterCrowdSize,shortestPaths))*np.sum(roadDist)

	def p_accept(self, candidate_fitness):
        """
        Probability of accepting if the candidate is worse than current
        Depends on the current temperature and difference between candidate and current
        """
        return math.exp(-abs(candidate_fitness - self.cur_fitness) / self.T)

    def accept(self, candidate):
        """
        Accept with probability 1 if candidate is better than current
        Accept with probabilty p_accept(..) if candidate is worse
        """
        candidate_fitness = self.fitness(candidate)
        if candidate_fitness < self.cur_fitness:
            self.cur_fitness = candidate_fitness
            self.cur_solution = candidate
            if candidate_fitness < self.best_fitness:
                self.best_fitness = candidate_fitness
                self.best_solution = candidate

        else:
            if random.random() < self.p_accept(candidate_fitness):
                self.cur_fitness = candidate_fitness
                self.cur_solution = candidate
	def transition():
		pass
	def anneal(self):
        while self.T >= self.stopping_temperature and self.iteration < self.stopping_iter:
            candidate = list(self.cur_solution)
            l = random.randint(2, self.N - 1)
            i = random.randint(0, self.N - l)
            candidate[i:(i + l)] = reversed(candidate[i:(i + l)])
            self.accept(candidate)
            self.T *= self.alpha
            self.iteration += 1

            self.fitness_list.append(self.cur_fitness)

        print('Best fitness obtained: ', self.best_fitness)
        print('Improvement over greedy heuristic: ',
              round((self.initial_fitness - self.best_fitness) / (self.initial_fitness), 4))



