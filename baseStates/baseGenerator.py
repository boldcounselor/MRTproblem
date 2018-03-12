import random
from PIL import Image
nodeNo = int(input('Number of nodes: '))
xSize = int(input('Size of x-axis in units: '))
ySize = int(input('Size of y-axis in units: '))
with open("nodes.txt","w") as f:
        f.write('%d %d %d\n' % (nodeNo,xSize,ySize))
        for i in range(0, nodeNo):
                f.write('%d %d %d\n' % (random.randint(1,xSize-1),random.randint(1,ySize-1),random.randint(0,255)))
        f.close()

