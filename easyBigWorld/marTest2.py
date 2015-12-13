from graphics import *
from marSimulatorNovelty import *
from random import *

def main():

	testWorld = World("Simulator", 2000, 400, 40)
	testWorld.readWorldConfigFile("hardBigWorld.txt")

	print "\nground:\n", testWorld.ground
	print "\nplatform\n", testWorld.platforms
	print "\ngoomba:\n", testWorld.goombaList
	print "\ncoin:\n", testWorld.coinsList
	print "\ncoinbox:\n", testWorld.coinboxesList
	print "\nhiddenRoomEntrance:\n", testWorld.hiddenEntrances
	print "\nhiddenRoomBonus:\n", testWorld.hiddenRoomBonuses
	print "\nfinishFlag: \n", testWorld.finishFlag

	print "\n~~~ FINISHED LOADING DATA ~~~\n"

	testWorld.getValidStand()
	print "~~~ finished getValidStand ~~~\n"

	testWorld.getAirspace()
	print "~~~ finished getAirspace ~~~\n"

	testWorld.printWorld()

	mario = Mario(testWorld, "Mario", 0, 8) 

	mario.setBrain(randomBrain())
	testWorld.addMario(mario)

	testWorld.makeVisible()

	sleep(0.5)


	x = True
	for i in range(1000):
		if not mario.alive:
			print "mario died or got to the flag - the main loop"
			#sleep(3)
			break

		testWorld.step()
		
		print "\n\nMario's pos:", (mario.x, mario.y)
		print"nearest coin: ", mario.distanceToNearestCoin(), "|| type of coin:", mario.coinType, "|| stall:", mario.stall, "|| coin:", mario.coinScore

		sleep(1)

	print "coin Score: ", mario.coinScore
	




class randomBrain(Brain):
    """A brain that uses a NEAT neural network as the controller"""
    
    def selectAction(self):

		return [(random()*2)-1, (random()*2)-1, (random()*2)-1, (random()*2)-1, (random()*2)-1]

main()