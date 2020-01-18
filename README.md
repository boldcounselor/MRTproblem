# Two-way Distribution Network with Weighted Population Values
This uses simulated annealing to generate a transport network (a two-way distribution network with weighted population values).

# Introduction
Each station has a population value and the size of the crowd that wants to travel from one station to another is determined by the size of both the origin and destination stations.

Thus, a large origin station and a large destination station will have a large commuter crowd, a large origin station and a small destination station will have a medium commuter crowd and vice-versa and finally a small origin station and a small destination station will have a small commuter crowd.

The energy function is essentially a product of the total cost of the road (measured in Euclidean distance) and the overall Euclidean distance travelled by the crowd (assuming shortest path travelled).

While this is a great simplification of the dynamics of mass transit, it still captures some of the more important aspects of the sizes of commuting populations. For a more Singaporean context, this means that the model still captures how the crowd commuting from a high-density area like Serangoon to another high-density area like Dhoby Ghaut will be larger than the crowd commuting from a comparatively low-density area like Braddell to another low-density area like Woodleigh, barring of course real world interactions of rush-hour and city zoning.

# Masochistic introduction
Given a ![](https://latex.codecogs.com/gif.latex?$$n$$) by ![](https://latex.codecogs.com/gif.latex?$$n$$) grid, there are ![](https://latex.codecogs.com/gif.latex?$$i$$) nodes that we want to connect where ![](https://latex.codecogs.com/gif.latex?$x&space;\in&space;[1,n^2]$), each with an associated population value ![](https://latex.codecogs.com/gif.latex?$p$) where ![](https://latex.codecogs.com/gif.latex?$p&space;\in&space;[1,255]$) and an associated ![](https://latex.codecogs.com/gif.latex?$$x$$) and ![](https://latex.codecogs.com/gif.latex?$$y$$) position where ![](https://latex.codecogs.com/gif.latex?$x,&space;y&space;\in&space;[0,n]$).

Assuming that the size of any crowd that wants to travel from any node ![](https://latex.codecogs.com/gif.latex?$$j$$) to ![](https://latex.codecogs.com/gif.latex?$k$) is proportional to the percentage of the rest of the population that ![](https://latex.codecogs.com/gif.latex?$k$) makes up, we can thus formulate the size of the crowd that travels from node ![](https://latex.codecogs.com/gif.latex?$$j$$) to ![](https://latex.codecogs.com/gif.latex?$k$) as 
