from marioSim2 import *
from neat import config, population, chromosome, genome, visualize
from neat.nn import nn_pure as nn

"""
This program allows you to EVOLVE NEAT networks. Most of the parameter
settings for the evolution are provided in the vacuum_config file. Each
run of evolution will save a file for the best individual from each
generation (called best_chromo_0, best_chromo_1, etc).  Each run also 
saves files called avg_fitness.svg and speciation.svg that can be viewed
using the unix command xv. 
"""


def main():
    # set up NEAT
    config.load("mar2_config")
    chromosome.node_gene_type = genome.NodeGene
    population.Population.evaluate = coverageFitness #function name 
    pop = population.Population()
    # set how many generations you want evolution to run
    generations = 30
    pop.epoch(generations, report=True, save_best=True)
    # Plots the best/average fitness across the evolution
    visualize.plot_stats(pop.stats)
    # Creates a visualization of speciation that occurred
    visualize.plot_species(pop.species_log)

def coverageFitness(population):
    """Given a NEAT population, compute the fitness of each individual"""
    for i in range(len(population)):
        chromo = population[i]
        
        # set up your simulator
        myworld = World("Simulator", 2000, 400, 40)
        myworld.readWorldConfigFile("finalWorld.txt")
        myworld.getValidStand()
        myworld.getAirspace()

        mario = Mario(myworld, "Mario", 0, 8)
        
        mario.setBrain(neatBrain(chromo))
        myworld.addMario(mario)
        
        # let the agent move for 1500 steps
        for i in range(1500):
            if not mario.alive:
                break

            myworld.step()

        # set fitness to the coverage
        #print "fitness: ", mario.getFitness()
        chromo.fitness = mario.getFitness()

class neatBrain(Brain):
    """A brain that uses a NEAT neural network as the controller"""
    
    def __init__(self, chromo):
        # Turn the flat chromosome into a neural network
        self.nnet = nn.create_ffphenotype(chromo)
    
    def selectAction(self):
        nearestCoin = self.agent.distanceToNearestCoin()

        # Set up the sensor data as input for the network
        #print "inputs: ", nearestCoin[0], nearestCoin[1]
        inputs = [nearestCoin, self.agent.coinScore, self.agent.stall] 
        self.nnet.flush()
        #print "coinscore: ", self.agent.coinScore

        # Propagate the inputs throught the network and get the outputs
        outputs = self.nnet.sactivate(inputs)
        #print "output: ", outputs[0]

        # Use the outputs to control the agent's translation and rotation
        #print outputs[0]#, outputs[1], outputs[2], outputs[3], outputs[4]) 
        return [outputs[0], outputs[1], outputs[2], outputs[3], outputs[4]]

main()
