from graphics import *
from marSimulatorNovelty import *
from random import *

def main():

	testWorld = World("test", 1080, 280, 40)

	testWorld.readWorldConfigFile("easySmallWorld.txt")

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

	mario = Mario(testWorld, "Mario", 16, 4) 
	# mario = Mario(testWorld, "Mario", 25, 5) # test flag

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