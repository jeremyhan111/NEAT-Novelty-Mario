import sys
from marSimNovelty import *
from neat import config, population, chromosome, genome, visualize
from neat.nn import nn_pure as nn
import cPickle as pickle

"""
This program allows you to evaluate an evolved NEAT network, visualizing
it's behavior and logging each input and output.
"""

def main(argv=None):
    # Use a command line argument to pass in the chromo file of an evolved net
    argv = sys.argv[1:]
    print argv
    if len(argv) != 1:
        print "Usage: You must pass a chromosome file to be evaluated"
        return
    else:
        chromo_file = argv[0]
        log_file = argv[0] + ".log"

    # set up NEAT
    logFP = open(log_file, "w")
    chromoFP = open(chromo_file, "r")
    chromo = pickle.load(chromoFP)
    chromoFP.close()
    print chromo
    # Creates a visualization of the network's topology
    visualize.draw_net(chromo, "_"+chromo_file)
    config.load("marNovelty_config")
    chromosome.node_gene_type = genome.NodeGene


    # set up your simulator
    myworld = World("Simulator", 1080, 280, 40)
    
    # myworld.readWorldConfigFile("easyConfig.txt")
    # myworld.readWorldConfigFile("intermediateConfig.txt")
    myworld.readWorldConfigFile("testConfig.txt")

    myworld.getValidStand()
    myworld.getAirspace()

    mario = Mario(myworld, "Mario", 0, 5)
    myworld.addMario(mario)
    myworld.makeVisible()
    mario.setBrain(neatBrain(chromo, logFP))


    for i in range(1500):
        if not mario.alive:
            break

        myworld.step()


    fitness = mario.getFitness()

    print "Objective fitness:", fitness
    print "Behavior:", mario.getBehavior()
    # wait for a mouse click before ending the program
    myworld.window.getMouse()
    logFP.write("Fitness %f\n" % fitness)
    logFP.close()


class neatBrain(Brain):

    def __init__(self, chromo, logfile):
        self.nnet = nn.create_ffphenotype(chromo)
        # used to save information about the agent's behavior
        self.logfile = logfile 
        self.timer = 1500

    def selectAction(self):
        nearestCoin = self.agent.distanceToNearestCoin()


        inputs = [nearestCoin[0]/26.0, nearestCoin[1]/6.0, self.agent.coinScore/55.0, 1]
        self.timer -= 1
        self.logfile.write("Dist to Coin: %.2f %.2f CoinScore: %.2f, bias: %.2f" % tuple(inputs))
        self.nnet.flush()

        outputs = self.nnet.sactivate(inputs)
        self.logfile.write(" motionChoice: %.2f %.2f %.2f %.2f %.2f \n" % tuple(outputs))
        return outputs

main()


