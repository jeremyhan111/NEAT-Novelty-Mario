from graphics import *
from marioSim2 import *
from random import *

def main():

	testWorld = World("test", 2000, 400, 40)

	testWorld.readWorldConfigFile("finalWorld.txt")

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

	mario = Mario(testWorld, "Mario", 3, 8)
	testWorld.addMario(mario)

	testWorld.makeVisible()

	sleep(0.5)
	

	x = True
	for i in range(3000):
		if not mario.alive:
			print "mario died or got to the flag - the main loop"
			#sleep(3)
			break

		testWorld.goombaList = []
		testWorld.goombaListLastDirection = []
		for goomba in testWorld.goombas:
			goomba.moveGoomba()
		
		print "mario nearest coin: ", mario.distanceToNearestCoin()
		#mario.update((random()*2)-1)
		mario.update([1, 0, 0, 0, 0])
		sleep(4)

	print "coin Score: ", mario.coinScore
	

main()