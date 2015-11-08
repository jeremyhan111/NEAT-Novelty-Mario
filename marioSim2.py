from graphics import *
from string import *
from time import sleep


class World(object):
	""" COMMENT """

	def __init__(self, name, width, height, gridDim = 10):
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
		self.coinsList = []
		self.coinboxesList = []


		# objects:
		self.marios = None
		self.goombas = []

		# int values
		self.hiddenRoomBonuses = []

		self.madeWin = False




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

		for coin in self.coinsList:
			center = Point(coin[0]*scale + scale/2, coin[1]*scale + scale/2)
			coinCircle = Circle(center, scale/2)
			coinCircle.setFill("yellow")
			coinCircle.draw(self.window)

		for coinbox in self.coinboxesList:
			p1 = Point(coinbox[0]*scale, coinbox[1]*scale)
			p2 = Point((coinbox[0] + 1)*scale, (coinbox[1] + 1)*scale)

			coinRect = Rectangle(p1, p2)
			coinRect.setFill("brown")
			coinRect.draw(self.window)

		for goomba in self.goombas:
			goomba.drawGoomba()

		for platform in self.platforms:
			p1 = Point((platform[0])*scale, ((platform[1]) + 1)*scale)
			p2 = Point(((platform[0] + 1)*scale), ((platform[1]) + 1)*scale)

			platLine = Line(p1, p2)
			platLine.setWidth(5)
			platLine.setFill("blue")
			platLine.draw(self.window)



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

			elif platform in platformList:
				continue

			else:
				self.validStand.append(platform)
				print "validstand", platform

				platformList.pop(0)


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

			if word != fileWordList[i] or len(wordList) <= 1:
				self.fileError(2)

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
					elif fileWordList[i] == "coin":
						self.coinsList.append((x, y))
					elif fileWordList[i] == "coinbox":
						self.coinboxesList.append((x, y))
					elif fileWordList[i] == "hiddenRoomEntrance":
						self.hiddenEntrances.append((x, y))
					elif fileWordList[i] == "finishFlag":
						self.finishFlag.append((x, y))

				while len(wordList) == 0:
					line = worldFile.readline()
					wordList = line.split()

				word = wordList.pop(0)



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


	def drawGoomba(self):
			
			self.goombaOval.draw(self.world.window)

	def move(self):

		if self.x == self.leftMax:
			if self.moveRight:
				self.x += 1
				self.goombaOval.move(1*self.scale, 0)

			else:
				self.moveRight = True

		elif self.x == self.rightMax:
			if self.moveRight:
				self.moveRight = False
			else:
				self.x -= 1
				self.goombaOval.move(-1*self.scale, 0)

		else:
			if self.moveRight:
				self.x += 1
				self.goombaOval.move(1*self.scale, 0)

			else:
				self.x -= 1
				self.goombaOval.move(-1*self.scale, 0)


