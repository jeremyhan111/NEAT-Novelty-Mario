from marSimulatorNovelty import *
from neat import config, population, chromosome, genome, visualize
from neat.nn import nn_pure as nn
from noveltySearch import *
import cPickle as pickle
from math import sqrt

# Global variables to set up novelty search 
novSearch = NoveltySearch(15, 100, 0.25, 2, 156, 50*9*sqrt(2402.0)) # For final world

bestChromos = []
bestScore = 0


def main():
    global novSearch

    # myworld = World("Simulator", 1080, 280, 40)
    # myworld.readWorldConfigFile("testConfig.txt")

    myworld = World("Simulator", 2000, 400, 40)
    myworld.readWorldConfigFile("easyBigWorld.txt")

    myworld.getValidStand()
    myworld.getAirspace()


    mario = Mario(myworld, "Mario", 0, 8) 

    # set up NEAT
    config.load("novelty_config")
    chromosome.node_gene_type = genome.NodeGene

    # use the noveltyFitness function to determine fitness scores
    population.Population.evaluate = noveltyFitness 
    pop = population.Population()

    # set how many generations you want evolution to run
    generations = 30
    pop.epoch(generations, report=True)
    
    # After evolution completes...

    # Plot the best/average fitness across the evolution
    visualize.plot_stats(pop.stats)

    # Create a visualization of speciation that occurred
    visualize.plot_species(pop.species_log)

    # save the archive and growth data from novelty search
    novSearch.saveArchive("mario")
    novSearch.saveGrowth("mario")

    # Save the best coverage chormosomes found
    print "\nFound behaviors with the following coverage scores:"

    for i in range(len(bestChromos)):
        print bestChromos[i][1]
        f = open("bestChromo%d" % (i), "w")
        pickle.dump(bestChromos[i][0], f)
        f.close()

    # Save the most recently added chromosomes in the archive
    print "\nNovelty scores for 10 most recently added behaviors:"

    i = 0
   
    for saved in novSearch.archive[-10:]:
        print saved[1]
        f = open("novelty%d" % (i), "w")
        pickle.dump(saved[2], f)
        f.close()
        i += 1
    
def noveltyFitness(population):

    global novSearch, bestChromos, bestScore
    bestScoreOfGen = 0
    bestChromoOfGen = None

    for i in range(len(population)):
        # print "\n\n\nstart"
        chromo = population[i]

        # set up your simulator
        # myworld = World("Simulator", 1080, 280, 40)
        # myworld.readWorldConfigFile("testConfig.txt")

        myworld = World("Simulator", 2000, 400, 40)
        myworld.readWorldConfigFile("easyBigWorld.txt")

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

        # check the coverage score
        objectiveFitness = mario.getFitness()
        # print objectiveFitness
        
        if objectiveFitness > bestScoreOfGen:
            bestScoreOfGen = objectiveFitness
            bestChromoOfGen = chromo
        
        behavior = mario.getBehavior()
        novelty = novSearch.checkArchive(behavior, chromo)

        chromo.fitness = novelty
    
    if bestScoreOfGen > bestScore:
        print "!!! New best coverage behavior found", bestScoreOfGen
        print
        bestScore = bestScoreOfGen
        bestChromos.append((bestChromoOfGen, bestScoreOfGen))


class neatBrain(Brain):
    """A brain that uses a NEAT neural network as the controller"""

    def __init__(self, chromo):

        # Turn the flat chromosome into a neural network
        self.nnet = nn.create_ffphenotype(chromo)
        #self.timer = 1500

    def selectAction(self):

        # Set up the sensor data as input for the network
        inputs = [self.agent.distanceToNearestCoin(), self.agent.coinScore, self.agent.stall, self.agent.coinType]

       # print inputs
        self.nnet.flush()

        # Propagate the inputs throught the network and get the outputs
        outputs = self.nnet.sactivate(inputs)
        # Use the outputs to control the agent's translation and rotation
        return [outputs[0], outputs[1], outputs[2], outputs[3], outputs[4]]

main()


