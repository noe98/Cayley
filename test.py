import networks
from monte import MonteCarlo

lattice = networks.Lattice(3,3)

print(type(lattice.getNeighbors(3)))

sim = MonteCarlo(lattice)

sim.startRandom(.3)

print(lattice.getFeature("state"))


print("Neighbors of 1: ",lattice.getNeighbors(1))
print(sim.stateDegree(1,0))
