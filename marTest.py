from graphics import *
from marioSim import *
import string
from time import sleep



def main():

	

	testWorld = World("test", 1500, 500, 30, 10) # grids are then 50x50 pixels

	for x in range(30):
		testWorld.ground.append((x, 9))

	testWorld.makeVisible()

	# testWorld.readWorldConfigFile("testConfig.txt")
	# print "done loading\n"


	print "ground:", testWorld.ground






	time.sleep(100)


	# marAgent = Mario(testWorld, "Mario", 20, 20)

	# print "ground: \n", testWorld.ground




main()