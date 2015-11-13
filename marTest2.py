from graphics import *
from marioSim2 import *
from random import *

def main():

	testWorld = World("test", 1080, 280, 40)

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

	mario = Mario(testWorld, "Mario", 10, 4)
	testWorld.addMario(mario)

	testWorld.makeVisible()
	

	x = True

	for i in range(100):
		for goomba in testWorld.goombas:
			goomba.moveGoomba()
		
		
		#if x:
		mario.update((random()*2)-1)
			#x = False

		# else:
		# 	mario.update(-0.3)
		# 	x = True


		




		sleep(0.5)

main()