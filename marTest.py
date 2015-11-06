from graphics import *
from marioSim import *
import string
from time import sleep



def main():

	

	testWorld = World("test", 1500, 500, 30, 10) # grids are then 50x50 pixels

	for x in range(30):
		testWorld.ground.append((x, 9))

	print "ground:", testWorld.ground, "\n"

	testWorld.makeVisible()

	# testWorld.readWorldConfigFile("testConfig.txt")
	# print "done loading\n"



	marAgent = Mario(testWorld, "Mario", 0, 9)
	marAgent.makeVisible("red")

	for i in range(100):
		marAgent.translate(2)

	time.sleep(50)

	# print "ground: \n", testWorld.ground




main()