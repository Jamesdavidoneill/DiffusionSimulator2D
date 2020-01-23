#Boiler plate code to make sure everything works
%matplotlib inline
import numpy as np
import matplotlib.pylab as plt


#Number of particles to be simulated
N = 400
#Number of time steps to be simulated
T = 5000
#Length of sides of lattice on which particles dwell
l = 200
#How often should program save a snapshot of the particle difusion
SaveRate = 50

#Creates an array of N particles, each with an x and y commponent
particles = np.zeros([N,2])
#Creates an array of length T to store the entropy at each moment in time
entropy = np.zeros([T])
#Create and array to store the particle density in each region of 8 * 8 grid
density = np.zeros([64])

def InitialiseParticles():
    #Set the initial position for all the particles
    for p in particles:
        p[0] = 100
        p[1] = 100

def GenerateSnapshot(n):
    #Creates an image of where the particles currently are in the l * l lattice
    if n%SaveRate == 0:
        #Clear current graph
        plt.cla()
        
        plt.xlim(0, l)
        plt.ylim(0, l)

        plt.plot(particles[:,0], particles[:,1],  marker=".", ms=5, lw=0, c="g")
        plt.savefig("Difusionplot"+str(n)+ ".png")

def SimulateStep():
    #Moves simulation forward by a step of 1
    for p in particles:
        #Pick a random direction to move in
        
        #First, decide to move in either the x or y direction
        #Then decide to move "up or down" or "left or right"
        if np.random.randint(0, 2, 1):
            #Move in x direction
            if np.random.randint(0, 2, 1):
                #Move right
                p[0] += 1
            else:
                #Move left
                p[0] -= 1
        else:
            #Move in y direction
            if np.random.randint(0, 2, 1):
                #Move up
                p[1] += 1
            else:
                #Move down
                p[1] -= 1
        #Need to check for collisions
        if p[0] < 0:
            #Too far to left
            p[0] += 2 # Reflected back
        if p[0] > l-1:
            #Too far to right
            p[0] -= 2 # Reflected back
        if p[1]<0:
            #Too far down
            p[1] += 2 # Reflected back
        if p[1] > l-1:
            #Too far up
            p[1] -= 2 # Reflected back
def GenerateDensityDistribution():
    #Counts number of particles in each grid cell
    #Set all elements in density to 0
    density.fill(0)
    #Length of grid square
    g = l/8
    #Position of particle in grid
    x = 0
    y = 0
    #Index to store particle count in density array
    for p in particles:
        x = np.floor(p[0]/g)
        y = np.floor(p[1]/g)
        i = int (8 * y + x)
        density[i] += 1
    
def CalculateEntropy(t):
    #Calcultes the entropy for a given snapshot of the simulation
    #Creates array of the densities of each region
    GenerateDensityDistribution()
    #Running tally for entropy
    S = 0
    for i in density:
        pi = i/N
        if pi != 0:
            S -= pi * np.log(pi)
        else:
            #If pi is 0, log function undefined. A small, non zero value is used instead
            S -= 0#pi * np.log(1e15)
    entropy[t] = S

def EntropyPlot():
    plt.cla()
    
    plt.title("Graph of entropy over time", fontsize ="xx-large")
    plt.xlabel('t', fontsize ="xx-large")
    plt.ylabel('S/k', fontsize ="xx-large")
    plt.xlim(0, T)
    plt.ylim(0, 10)

    plt.plot(range(T), entropy[:],"-r")
    plt.savefig("Images/Entropyplot.png")


#Set size of figure
plt.figure(figsize=(20,10))
#Set initial positions for particles
InitialiseParticles()
#Loop through the particles
for i in range(T):
    #Create an image of particles if appropriate
    GenerateSnapshot(i)
    #Calculate the entropy at each point in time
    CalculateEntropy(i)
    #Move on to the next step of the simulation
    SimulateStep()
#Create a plot of the entropy with respect to number of steps t
EntropyPlot()

