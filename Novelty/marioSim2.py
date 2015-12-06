from graphics import *
from string import *
from time import sleep
from math import *


class World(object):
	""" COMMENT """

	def __init__(self, name, width, height, gridDim = 10, delay = 0.15):
		""" Initializes a world object.

			name - name of world object
			width - number of pixels in the x direction
			height - number of pixels in the y direction
			gridDim - pixel width and height of each grid square.
			   By default, the grids will be 10x10 pixels.
		"""
		self.name = name
		self.width = width
		self.height = height
		self.gridDim = gridDim
		self.delay = delay

		self.numGridX = width / gridDim
		self.numGridY = height / gridDim

		# Lists of (x, y) location tuples
		self.ground = []
		self.platforms = []
		self.validStand = []
		self.validAirspace = []
		self.hiddenEntrances = [] #same indexing order as hiddenRoomBonus
		self.finishFlag = []
		self.goombaList = [] 
		self.goombaListLastDirection = []
		self.coinsList = [] # x, y list of where coins are located
		self.coinObjectList = [] # coin object list
		self.coinboxesList = [] # x, y coinbox list
		self.coinboxObjectList = []

		# objects:
		self.marios = None
		self.marioAlive = True
		self.goombas = [] # goomba object list

		# int values
		self.hiddenRoomBonuses = []

		self.madeWin = False

		#for novelty:
		self.possibleTravel = 93




	def printWorld(self):
		"""

		"""

		for i in range(self.numGridY):
			for j in range(self.numGridX):

				test = (j, i)
				
				if test in self.hiddenEntrances:
					print "$",
				elif test in self.finishFlag:
					print "%",
				elif test in self.ground:
					print "X",
				elif test in self.platforms:
					print "_",
				elif test in self.validStand:
					print " ",
				elif test in self.coinsList:
					print "0",
				elif test in self.coinboxesList:
					print "B",
				elif test in self.goombaList:
					print "G",				
				elif test in self.validAirspace:
					print "^", 
				else:
					print "?",
            
			print "\n"


	def calculateMaxCoinScore(self):
		self.maxCoinScore = len(self.goombaList) + len(self.coinsList) + len(self.coinboxesList) + 15*len(self.hiddenRoomBonuses)

	def addMario(self, mario):
		"""Adds an agent to the world"""
		self.marios = mario
	

	def step(self):
		"""Moves all of the marios in the world by stepping their brains.
		When the world is visible, sleeps for the delay time between steps"""

		self.goombaList = []
		self.goombaListLastDirection = []
		
		for goomba in self.goombas:
			goomba.moveGoomba()

		self.marios.stepBrain()

		if self.madeWin:
			sleep(self.delay)




	def makeVisible(self):
		"""Creates a graphics window making the world visible"""
		self.window = GraphWin(self.name, self.width, self.height)
		self.madeWin = True

		scale = self.gridDim

		for ground in self.ground:
			p1 = Point(ground[0]*scale, ground[1]*scale)
			p2 = Point((ground[0] + 1)*scale, (ground[1] + 1)*scale)

			groundRect = Rectangle(p1, p2)
			groundRect.setFill("green")
			groundRect.draw(self.window)

		for coin in self.coinObjectList:
			coin.drawCoin()

		for coinbox in self.coinboxObjectList:
			coinbox.drawCoinBox()	

		for goomba in self.goombas:
			goomba.drawGoomba()

		for platform in self.platforms:
			p1 = Point((platform[0])*scale, ((platform[1]) + 1)*scale)
			p2 = Point(((platform[0] + 1)*scale), ((platform[1]) + 1)*scale)

			platLine = Line(p1, p2)
			platLine.setWidth(5)
			platLine.setFill("blue")
			platLine.draw(self.window)

		self.marios.makeVisible()



	def getValidStand(self):
		""" Once the ground list is complete, call this function to create a
		list of valid grids that Mario can walk on """
		
		groundList = list(self.ground)
		platformList = list(self.platforms)

		for ground in self.ground:

			potentialValidStand = (ground[0], ground[1] - 1)

			if potentialValidStand in groundList:
				continue

			elif potentialValidStand in self.platforms:
				continue

			else:
				self.validStand.append(potentialValidStand)
				groundList.pop(0)


		for platform in self.platforms:

			if platform in self.ground:
				continue

			# elif platform in platformList:
			# 	continue

			else:
				self.validStand.append(platform)

				platformList.pop(0)

		for coinbox in self.coinboxesList:

			potentialValidStand = (coinbox[0], coinbox[1] - 1)

			if potentialValidStand in self.validStand:
				continue

			else:
				self.validStand.append(potentialValidStand)


	def getAirspace(self):
		""" Once the validStand list is complete, call this function to create a
		list of valid grids in the air that Mario can jump into """

		for i in range(self.numGridX):
			for j in range(self.numGridY):
				potentialAirspace = (i, j)


				if potentialAirspace in self.ground:
					continue
				elif potentialAirspace in self.coinboxesList:
					continue
				elif potentialAirspace in self.platforms:
					self.validAirspace.append(potentialAirspace)
				else:
					self.validAirspace.append(potentialAirspace)
				



	def readWorldConfigFile(self, filename):
		""" Takes in a file that details how the world should be set up and
			sets up the world accordingly. 

			filename - .txt file that details the world configuration
			File should be formatted as such:
		
			ground   x y x y x y ...
			platform x y x y x y ...
			goomba   x y x y x y ...
			coin     x y x y x y ...
			coinbox  x y x y x y...
			hiddenRoomEntrance x y x y x y...
			hiddenRoomBonus room1bonus room2bonus room3bonus...

			* note that whitespace and white lines do not matter
		"""

		worldFile = open(filename, "r")
		if worldFile is None:
			worldFile.close()
			self.fileError(1)

		line = worldFile.readline()
		wordList = line.split()

		fileWordList = ["ground", "platform", "goomba", "coin", "coinbox",\
		 "hiddenRoomEntrance", "hiddenRoomBonus", "finishFlag", "end"]

		word = wordList.pop(0)

		for i in range(len(fileWordList) - 1):

			if word != fileWordList[i]: #or len(wordList) <= 1:
				self.fileError(2)

			while len(wordList) == 0:
				line = worldFile.readline()
				wordList = line.split()

			word = wordList.pop(0)

			while word != fileWordList[i+1] or len(word) == 1:
				if fileWordList[i] == "hiddenRoomBonus":
					bonus = atoi(word)
					self.hiddenRoomBonuses.append(bonus)

				else:
					x = atoi(word)
					y = atoi(wordList.pop(0))

					if fileWordList[i] == "ground":
						self.ground.append((x, y))

					elif fileWordList[i] == "platform":
						self.platforms.append((x, y))

					elif fileWordList[i] == "goomba":
						dist = atoi(wordList.pop(0))
						self.goombaList.append((x, y))
						goomba = Goomba(self, x, y, dist)
						self.goombas.append(goomba)
						self.goombaListLastDirection.append(0)

					elif fileWordList[i] == "coin":
						self.coinsList.append((x, y))
						coin = Coin(self, x, y)
						self.coinObjectList.append(coin)

					elif fileWordList[i] == "coinbox":
						self.coinboxesList.append((x, y))
						coinBox = Coinbox(self, x, y)
						self.coinboxObjectList.append(coinBox)

					elif fileWordList[i] == "hiddenRoomEntrance":
						self.hiddenEntrances.append((x, y))

					elif fileWordList[i] == "finishFlag":
						self.finishFlag.append((x, y))

				while len(wordList) == 0:
					line = worldFile.readline()
					wordList = line.split()

				word = wordList.pop(0)

		# now calculate maxCoinScore
		self.calculateMaxCoinScore()
		#print self.maxCoinScore


	def fileError(self, errNum):

		if errNum == 1:
		    print "Failed to open world config file\n"
		elif errNum == 2:
		    print "\nError file format\n"
		    print "ground x y \n" \
		    	   "goomba x y rightPatrolDist \n" \
		    	   "coin x y \n" \
		    	   "coinbox x y \n" \
				   "hiddenRoomEntrance x y \n" \
				   "hiddenRoomBonus room1bonus room2bonus \n" \
				   "finishFlag \n" \
				   "end \n" 

		exit(1)


class Coin(object):
	"""COMMENT"""

	def __init__(self, world, x, y):
		self.world = world
		self.x = x
		self.y = y

	def drawCoin(self):
		scale = self.world.gridDim

		center = Point(self.x*scale + scale/2, self.y*scale + scale/2)

		self.coinCircle = Circle(center, scale/2)
		self.coinCircle.setFill("yellow")
		self.coinCircle.draw(self.world.window)		

	def undrawCoin(self):
		self.coinCircle.undraw()


class Coinbox(object):
	""" COMMENT """

	def __init__(self, world, x, y):
		
		self.world = world
		self.x = x
		self.y = y
		self.stillContainsCoin = True		


	def drawCoinBox(self):
		scale = self.world.gridDim

		p1 = Point(self.x*scale, self.y*scale)
		p2 = Point((self.x + 1)*scale, (self.y + 1)*scale)

		self.coinRect = Rectangle(p1, p2)
		self.coinRect.setFill("brown")

		self.coinRect.draw(self.world.window)

	def undrawCoin(self):
		self.coinRect.undraw()
	
	def hit(self, visible):

		if self.stillContainsCoin:
			self.stillContainsCoin = False

			if visible:
				self.coinRect.setFill("white")
			
			return 1

		else:
			return 0
			

class Goomba(object):
	""" COMMENT """

	def __init__(self, world, x, y, roamRightDist):
		
		self.world = world
		self.x = x
		self.y = y
		self.leftMax = x
		self.rightMax = x + roamRightDist - 1
		self.moveRight = True

		self.scale = self.world.gridDim
		p1 = Point((x+0.125)*self.scale, y*self.scale)
		p2 = Point((x + 0.875)*self.scale, (y + 1)*self.scale)
		self.goombaOval = Oval(p1, p2)
		self.goombaOval.setFill("brown")
		self.makeVisible = False

	def drawGoomba(self):
		self.makeVisible = True	
		self.goombaOval.draw(self.world.window)

	def undrawGoomba(self):
		self.goombaOval.undraw()

	def moveGoomba(self):

		if not self.world.marioAlive:
			return

		if self.x == self.leftMax: #if goomba is at the max left point
			if self.moveRight: # goomba wants to move right now
				self.x += 1
				self.world.goombaListLastDirection.append(1)
				if self.makeVisible:
					self.goombaOval.move(1*self.scale, 0)

			else: # goomba should wait at max point for one time step
				self.world.goombaListLastDirection.append(0)
				self.moveRight = True

		elif self.x == self.rightMax: #if goomba is at the max right point
			if self.moveRight: #if it still wants to move right, wait there for one time step
				self.world.goombaListLastDirection.append(0)
				self.moveRight = False
			else: # otherwise start moving left
				self.x -= 1
				self.world.goombaListLastDirection.append(-1)

				if self.makeVisible:
					self.goombaOval.move(-1*self.scale, 0)

		else: # normal moving situations
			if self.moveRight: 
				self.x += 1
				self.world.goombaListLastDirection.append(1)
				if self.makeVisible:
					self.goombaOval.move(1*self.scale, 0)

			else:
				self.x -= 1
				self.world.goombaListLastDirection.append(-1)
				if self.makeVisible:
					self.goombaOval.move(-1*self.scale, 0)

		self.world.goombaList.append((self.x, self.y))


class Mario(object):
	"""docstring for Mario"""

	def __init__(self, world, name, x, y, color = "red"):
		""" COMMENT """

		self.world = world
		self.name = name
		self.x = x # in terms of grid coords
		self.y = y # in terms of grid coords
		self.radius = self.world.gridDim / 2
		self.color = color
		self.visible = False
		self.visibleAgent = None
		self.brain = None

		self.lastX = x
		self.lastY = y
		self.nextX = x
		self.nextY = y
		self.dx = 0
		self.dy = 0

		self.uniqueLocations = []

		self.inTheAir = False
		self.jumpingUp = False
		self.jumpNextMove = None
		self.falling = False
		self.duck = False
		self.drawValid = True

		self.coinScore = 0
		self.maxCoinScore = self.world.maxCoinScore
		#print self.maxCoinScore
		self.movingScore = 0

		self.stall = False
		self.stallCount = 0

		# novelty
		self.behavior = []

		self.alive = True

	def makeVisible(self):
		if self.world.madeWin == False:
			self.world.makeVisible()
			self.world.madeWin = True;
		self.visibleAgent = VisibleMario(self, self.color)
		self.visible = True


	def getFitness(self):
		#print (self.coinScore) / (self.maxCoinScore)
		#print "coinScore: ", self.coinScore
		#print "maxCoinScore: ", self.maxCoinScore
		return self.coinScore*1.0 / self.maxCoinScore
		#return 0.1

	def translate(self, amt):
		""" where amt is -1, 0, 1 """

		self.nextX = self.x + amt
		self.nextY = self.y + 0

		self.dx = amt
		self.dy = 0

		#check for goombas and marios switching spots
		if amt == 1: # if mario is moving right, check that goomba didn't just move to the left of mario
			if (self.x, self.y) in self.world.goombaList:
				index = self.world.goombaList.index((self.x, self.y))
				
				# if goomba is moving left
				if self.world.goombaListLastDirection[index] == -1:
					# mario is now dead because he walked past a goomba
					# print "Mario is now dead mar right goomb left"
					self.world.marioAlive = False
					#print "1"
					self.alive = False

		elif amt == -1: # mario is moving left, check that a goomba didn't just move to the right of mario
			if (self.x, self.y) in self.world.goombaList:
				index = self.world.goombaList.index((self.x, self.y))

				# if goomba is moving right
				if self.world.goombaListLastDirection[index] == 1:
					# mario is now dead because he walked past a goomba
					# print "Mario is now dead mar left goomb right"
					self.world.marioAlive = False
					self.alive = False
					#print "2"


	def jump(self, direction):
		""" where direction is -1 for left and 1 for right"""
		self.nextX = self.x + 0
		self.nextY = self.y - 1

		self.dx = 0
		self.dy = -1

		self.jumpingUp = True

		self.jumpNextMove = direction

	def translateAir(self):
		self.nextX = self.x + self.jumpNextMove
		self.nextY = self.y + 0

		self.dx = self.jumpNextMove
		self.dy = 0

		self.jumpNextMove = None
		self.falling = True

	def fall(self):
		self.nextX = self.x + 0
		self.nextY = self.y + 1

		self.dx = 0
		self.dy = +1

	def gotCoinMakeBank(self):
		""" Increment the coinScore, undraw the coin and remove the coin
			from related coin lists """

		self.coinScore += 1
		coinIndex = self.world.coinsList.index((self.x, self.y))
		coinToDelete = self.world.coinObjectList[coinIndex]

		if self.visible:
			coinToDelete.undrawCoin() # undraw coin

		self.world.coinsList.remove((self.x, self.y)) # remove coins from list
		self.world.coinObjectList.remove(coinToDelete)


	def checkBounds(self):

		
		self.drawValid = True

		if not self.alive:
			# print "mario's dead?"
			pass

		elif (self.nextX, self.nextY) in self.world.finishFlag:
			# print "Mario got to the finish flag"
			self.x = self.nextX
			self.y = self.nextY
			self.coinScore += 5
			self.alive = False
			self.world.marioAlive = False
			#print "next: ", self.nextX, self.nextY
			#print "finish: ", self.world.finishFlag
			#print "3"



		elif self.jumpingUp:
			# If jumping up into the air
			if (self.nextX, self.nextY) in self.world.validAirspace:
				self.x = self.nextX
				self.y = self.nextY
				self.inTheAir = True
				self.jumpingUp = False

				if (self.x, self.y) in self.world.coinsList:
					self.gotCoinMakeBank()
					
					# print "lens: list:", len(self.world.coinsList), "object:", len(self.world.coinObjectList)				

			elif (self.nextX, self.nextY) in self.world.coinboxesList:
				self.jumpingUp = False
				self.jumpNextMove = None
				self.drawValid = False

				coinBoxIndex = self.world.coinboxesList.index((self.nextX, self.nextY))
				self.coinScore += self.world.coinboxObjectList[coinBoxIndex].hit(self.visible)


			# else:
			# 	self.jumpingUp = False


		elif self.inTheAir:
			# If currently in the air
			if (self.nextX, self.nextY) in self.world.validStand or (self.nextX, self.nextY) in self.world.platforms:
				# jumped onto a valid standing spot
				self.inTheAir = False
				self.falling = False
				#todo: set all other air variables to what they should be ?
				self.x = self.nextX
				self.y = self.nextY

				
				#check for goombas
				if (self.x, self.y) in self.world.goombaList:
					# print "Goomba is now dead"
					
					index = self.world.goombaList.index((self.x, self.y))

					goombaToDelete = self.world.goombas[index]

					goombaToDelete.undrawGoomba()

					self.world.goombaList.remove((self.x, self.y))
					self.world.goombas.remove(goombaToDelete)

					self.coinScore += 1



				elif (self.x, self.y) in self.world.coinsList:
					self.gotCoinMakeBank()
			

			elif (self.nextX, self.nextY) in self.world.validAirspace:
				#jumped into a valid airspace
				# print "valid airspace"
				self.falling = True
				self.x = self.nextX
				self.y = self.nextY

				if (self.x, self.y) in self.world.coinsList:
					self.gotCoinMakeBank()


			else:
				# not a valid place to jump into
				# print "not valid jump"
				self.dx = 0 
				self.dy = 0
				self.drawValid = False

	
		elif (self.nextX, self.nextY) in self.world.validStand or (self.nextX, self.nextY) in self.world.platforms:
			# print "is a valid standing spot"

			self.x = self.nextX
			self.y = self.nextY

			#print "potential duck"
			#print "mario:", self.x, self.y
			#print "goomba: "
			#for goomb in self.world.goombaList:
				#print goomb

			if self.duck and (self.x, self.y) in self.world.hiddenEntrances:
				bonusIndex = self.world.hiddenEntrances.index((self.x, self.y))
				self.coinScore += self.world.hiddenRoomBonuses[bonusIndex]
				#print "length of hiddenroomBonus: ", len(self.world.hiddenRoomBonuses)
				#print "length of hiddenEntrances: ", len(self.world.hiddenEntrances)
				self.world.hiddenEntrances.remove((self.x, self.y))
				self.world.hiddenRoomBonuses.remove(self.world.hiddenRoomBonuses[bonusIndex])
				#p#rint "length of hiddenroomBonus: ", len(self.world.hiddenRoomBonuses)
				#print "length of hiddenEntrances: ", len(self.world.hiddenEntrances)


				#self.world.hiddenRoomBonuses[bonusIndex] = 0
				self.world.hiddenEntrances

				self.duck = False

			#check for goombas
			if (self.x, self.y) in self.world.goombaList:
				# print "Mario is now dead"
				self.alive = False
				self.world.marioAlive = False
				#print "4"

				#print "mario died"

			elif (self.x, self.y) in self.world.coinsList:
				self.gotCoinMakeBank()


		
		elif (self.nextX, self.nextY) in self.world.validAirspace:
			# print "got into a valid airspace "
			self.inTheAir = True
			self.falling = True
			self.x = self.nextX
			self.y = self.nextY

			if(self.x, self.y) in self.world.coinsList:
				self.gotCoinMakeBank()



		else:
			# print "not valid move"
			self.dx = 0 
			self.dy = 0
			self.drawValid = False

			#check for goombas
			if (self.x, self.y) in self.world.goombaList:
				# print "Mario is now dead"
				self.alive = False
				self.world.marioAlive = False


		# if self.visible and drawValid:
  		# 	move by 1 grid size
		# 	self.visibleAgent.moveMario(self.dx, self.dy)

        
        

	def update(self, cmd):
		"""Ensure that the given translate and rotate commands are in the
		expected bounds of [-1, 1], then using the speed of the agent
		determine the amount of movement to make. Calls the translate and
		rotate methods to do the movement"""

		# print "\n\n this step", self.x, self.y
		# print "inTheAir: ", self.inTheAir, " falling: ", self.falling
        

		#print "command", cmd,


		# if cmd > 1 or cmd < -1:
		# 	print "Invalid move. Has to be between [-1, 1]\n"
		# 	exit()

		maxCmd = cmd.index(max(cmd))


		if not self.inTheAir and not self.falling:
			#print "Excecuting command"

			if maxCmd == 0: # move left
				#print "move left"
				self.translate(-1)
				self.duck = False

			elif maxCmd == 1: # move right
				#print "move right"
				self.translate(1)
				self.duck = False

			elif maxCmd == 2: # jump left
				#print "jump left"
				self.jump(-1)
				self.duck = False
				# if (self.coinScore > 0):
				# 	self.coinScore -= 0.2

			elif maxCmd == 3:  # jump right
				#print "jump right"
				self.jump(1)
				self.duck = False
				# if (self.coinScore > 0):
				# 	self.coinScore -= 0.2

			elif maxCmd == 4: # duck
				#print "duck"
				self.duck = True
				self.nextX = self.x
				self.nextY = self.y

		if self.inTheAir and self.jumpNextMove:
			#already in the air and need to move left or right
			# print "calling translateAir"
			self.translateAir()

		elif self.falling:
			# print "falling"
			self.fall()


		if (abs(self.x - self.lastX) == 0):
			self.stallCount += 1
		else:
			self.stallCount = 0

		if (self.stallCount > 3):
			self.stall = True
		else:
			self.stall = False

		self.lastX = self.x
		self.lastY = self.y

		if (self.x, self.y) not in self.behavior:
			self.behavior.append((self.x, self.y))

		self.checkBounds()
		# print "mario:", (self.x, self.y)
		# print "goomba:", (self.world.goombaList)
		# print "coins", len(self.world.coinsList)
		# print "coinboxes", len(self.world.coinboxesList)
		# print "coinscore", self.coinScore

		if self.visible and self.drawValid:
			# move by 1 grid size
			dx = self.x - self.lastX
			dy = self.y - self.lastY
			self.visibleAgent.moveMario(dx, dy)

	def getBehavior(self):
		while len(self.behavior) < self.world.possibleTravel:
			self.behavior.append((0, 0))
		return self.behavior


	def calculateDistance(self, a, b):
		return sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)    


	def distanceToNearestCoin(self):
		"""Calculates distance to nearest coin, coinbox, goomba or entrance"""
		minDistance = 100000000000
		minTuple = None

		#print self.world.finishFlag[0], self.world.finishFlag[1]


		for coin in self.world.coinsList:
			distance = self.calculateDistance(coin, (self.x, self.y))

			if distance < minDistance:
				minDistance = distance
				minTuple = coin
				#print "1", minTuple


		for coinbox in self.world.coinboxObjectList:
			if coinbox.stillContainsCoin:
				distance = self.calculateDistance((coinbox.x, coinbox.y), (self.x, self.y))
				#print "in coinbox, and distance is: ", distance
				if distance < minDistance:
					minDistance = distance
					minTuple = (coinbox.x, coinbox.y)
					#print "and tuple is: ", minTuple


		for goomba in self.world.goombaList:
			distance = self.calculateDistance(goomba, (self.x, self.y))
			if distance < minDistance:
				minDistance = distance
				minTuple = goomba
				#print "2", minTuple


		for entrance in self.world.hiddenEntrances:
			distance = self.calculateDistance(entrance, (self.x, self.y))
			if distance < minDistance:
				minDistance = distance
				minTuple = entrance
				#p#rint "3", minTuple


		if minTuple is None: 
		# if something went wrong, give mario the finish location
		# this should never happen because the hidden entrances should always exist
			#return (self.world.finishFlag[0]-self.x, self.world.finishFlag[1]-self.y)
			return "hi"
		else:
			#print "just before: ", (minTuple[0]-self.x, minTuple[1]-self.y)
			#print "minTuple0: ", minTuple[0], "minTuple1: ", minTuple[1]
			#print "self.x: ", self.x, "self.y: ", self.y
			#return (minTuple[0]-self.x, minTuple[1]-self.y
			if (self.x - minTuple[0] > 0):
				return -1*minDistance
			else:
				return minDistance


	def minDxDyToNearestCoin(self):
		"""Calculates min dx, dy to nearest coin, coinbox, goomba or entrance"""
		minDistance = 100000000000
		minTuple = None


		for coin in self.world.coinsList:
			distance = self.calculateDistance(coin, (self.x, self.y))

			if distance < minDistance:
				minDistance = distance
				minTuple = coin


		for coinbox in self.world.coinboxObjectList:
			if coinbox.stillContainsCoin:
				distance = self.calculateDistance((coinbox.x, coinbox.y), (self.x, self.y))
				
				if distance < minDistance:
					minDistance = distance
					minTuple = (coinbox.x, coinbox.y)


		for goomba in self.world.goombaList:
			distance = self.calculateDistance(goomba, (self.x, self.y))
			if distance < minDistance:
				minDistance = distance
				minTuple = goomba


		for entrance in self.world.hiddenEntrances:
			distance = self.calculateDistance(entrance, (self.x, self.y))
			if distance < minDistance:
				minDistance = distance
				minTuple = entrance


		if minTuple is None: 
		# if something went wrong, give mario the finish location
		# this should never happen because the hidden entrances should always exist
			return (self.world.finishFlag[0]-self.x, self.world.finishFlag[1]-self.y)
		else:		
			return (minTuple[0] - self.x, self.y - minTuple[1])




	def setBrain(self, brain):
		"""Set the agent's brain to be the given brain"""
		self.brain = brain
		self.brain.agent = self

	def stepBrain(self):
		"""Get the next action, which is a move command amount in the 
		range [-1,1], from the brain and execute it"""
		move = self.brain.selectAction()
		self.update(move)


class VisibleMario(object):
	"""
    A visible version of an Agent object that can be viewed in a
    graphics window.
    """

	def __init__(self, mario, color):
		"""Mario agents are Circles objects """
		self.mario = mario
		self.window = self.mario.world.window

		scale = self.mario.world.gridDim
		center = Point(self.mario.x*scale + scale/2, self.mario.y*scale + scale/2)

		self.body = Circle(center, scale/2)
		self.body.setFill(color)

		self.draw()


	def moveMario(self, dx, dy):
		"""Move the Circles representing the agent the given dx, dy amount"""

		dx = dx * self.mario.world.gridDim
		dy = dy * self.mario.world.gridDim

		self.body.move(dx, dy)


	def draw(self):
		"""Draw the agent in the world"""
		self.body.draw(self.window)
    
	def undraw(self):
		"""Hide the agent"""
		self.body.undraw()

class Brain(object):
    """
    Abstract class for representing brains of agents.
    """
    def __init__(self):
        self.agent = None
    def selectAction(self):
        """
        Should return two float values in the range [-1,1] representing
        translate and rotate commands.
        """
        abstract()

