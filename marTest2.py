from graphics import *
from marioSim2 import *

def main():

	testWorld = World("test", 520, 140, 20)

	testWorld.readWorldConfigFile("testConfig.txt")

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

	testWorld.makeVisible()

	for i in range(100):
		for goomba in testWorld.goombas:
			goomba.move()

		sleep(0.5)

	time.sleep(100)

main()