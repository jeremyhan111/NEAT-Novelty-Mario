from graphics import *
from time import sleep
# from math import sin, cos, radians, sqrt, floor
# from random import random, randrange


class World(object):
    """
    comment
    """

    def __init__(self, name, width, height, gridX = 30, gridY = 10, delay = 0.025):
    	""" comment """

        self.name = name
        self.width = width
        self.height = height
        self.gridX = gridX
        self.gridY = gridY
        self.delay = delay
        self.ground = []
        self.validStand = []
        self.jumpAirspace = []
        self.marios = []
        self.coins = []
        self.goombas = []
        self.boxes = []
        self.hiddenRoom = []
        self.gridPixelSize = 50 #hard code for now, change later

        self.madeWin = False


    def makeVisible(self):
        """Creates a graphics window making the world visible"""
        self.window = GraphWin(self.name, self.width, self.height)
        self.madeWin = True

        for groundTile in self.ground:
            rectLR = Point(groundTile[0]*self.gridPixelSize, groundTile[1]*self.gridPixelSize)
            rectUL = Point(rectLR.getX()+self.gridPixelSize, rectLR.getY()+self.gridPixelSize)
            rect = Rectangle(rectLR, rectUL)
            print rect
            rect.setFill("green")
            rect.draw(self.window)

        time.sleep(0.01)


    def addMario(self, mario):
        """Adds a mario to the world"""
        self.marios.append(mario)

    def addGoomba(self, goomba):
    	""" Adds a Goomba to the world"""
        self.goombas.append(mario)


    def step(self):
        """Moves all of the agents in the world by stepping their brains.
        When the world is visible, sleeps for the delay time between steps"""
        for i in range(len(self.agents)):
            self.agents[i].stepBrain()
        if self.madeWin:
            sleep(self.delay)



class Mario(object):
    """
  	comment
    """
    def __init__(self, world, name, x, y, dx = 10, color = "red"):
        """Commment"""
        
        self.world = world
        self.name = name
        self.x = x
        self.y = y
        self.dx = dx
        self.inAir = False
        self.radius = self.world.gridPixelSize/2

    def makeVisible(self, color):
        """Create a VisibleAgent as the visible body of this agent"""
        if self.world.madeWin == False:
            self.world.makeVisible()
            self.world.madeWin = True;

        self.visibleMario = VisibleMario(self, color)
        self.visible = True

    def getGrid(self):
        """ find the grid location that (x, y) is in"""
        pass

    def interpretCommand(self, command):
        if command >= -1 and command < -0.6:
            self.moveRight()
        elif command >= -0.6 and command < -0.2:
            self.moveLeft()
        # elif command >= -0.2 and command < 0.2:
        #     self.jumpRight()
        # elif command >= 0.2 and command < 0.6:
        #     self.jumpLeft()
        # else:
        #     self.duck()


    def moveRight(self):
        self.x = self.x + self.dx
        if self.visible:
            self.visibleMario.translate()

    def moveLeft(self):
        self.x = self.x - self.dx
        if self.visible:
            self.visibleMario.translate()


    def update(self, command):
        if command > 1 or command < -1:
            print "Invalid translate. Has to be between [-1, 1]\n"
            exit()

        self.interpretCommand(command)
        self.checkStall()
        self.updateGrid()

        pass


    def checkStall(self):
        """Make the world boundary be a barrier for the agent. When agent
        goes beyond the world boundary, a flag called stall is set to True
        and the agent is placed back within the boundary. Otherwise stall
        is set to False."""

        

        #checks if stalled in x-direction

    def setBrain(self, brain):
        """Set the agent's brain to be the given brain"""
        self.brain = brain
        self.brain.agent = self

    def stepBrain(self):
        """Get the next action, which is a translate and rotate amount in the 
        range [-1,1], from the brain and execute it"""
        command = self.brain.selectAction()
        self.update(command)


class VisibleMario(object):
    """
    A visible version of an Mario object that can be viewed in a
    graphics window.
    """
    def __init__(self, mario, color):
        """Visible marios are colored sqruare objects """
        self.mario = mario
        self.window = self.mario.world.window
        x = self.mario.x * self.mario.world.gridPixelSize + self.mario.world.gridPixelSize/2
        y = self.mario.y * self.mario.world.gridPixelSize - self.mario.world.gridPixelSize/2
        print Point(x,y)
        self.body = Circle(Point(x,y), self.radius)
        self.body.setFill(color)

      
        self.draw()

        time.sleep(1)

    def translate(self, dx):
        """Move the Circles representing the agent the given dx, dy amount"""
        self.body.move(dx, 0)
        time.sleep(0.01)
        
    def jump(self, dy):
        """Rotate the small Circle representing the agent's heading the 
        given amount in degrees"""
        self.body.move(0, dy)

    def draw(self):
        """Draw the agent in the world"""
        self.body.draw(self.window)
        print "drew body"
        time.sleep(0.01)
    
    def undraw(self):
        """Hide the agent"""
        self.body.undraw()

class Goomba(object):
	"""
	comment 
	"""

	def __init__(self, name, x, y, p1, p2, color = "brown"):
		""" comment """

		self.name = name
		self.x = x
		self.y = y
		self.p1 = p1
		self.p2 = p2
		self.color = color



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