import random
from PIL import Image
class Node:
	def __init__(self, x, y, population):
		self.x = x
		self.y = y
		self.population = population

nodeList = []
nodeNo = 0
xSize = 0
ySize = 0

with open("nodes.txt","r") as data:
        nodeNo,xSize,ySize=map(int, data.readline().split())
        for i in range(1,nodeNo+1):
                parser=Node(0,0,0)
                parser.x,parser.y,parser.population=map(int, data.readline().split())
                nodeList.append(parser)
        data.close()

map = Image.new('RGB', (xSize,ySize), "white")
pixels = map.load()
for x in range(0,int(nodeNo)):
        pixels[nodeList[x].x, nodeList[x].y]=(nodeList[x].population,255-nodeList[x].population,0)
        
map.save("map.png")