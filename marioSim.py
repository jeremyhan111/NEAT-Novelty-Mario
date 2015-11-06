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

        for groundTile in self.ground:
            rectLR = Point(groundTile[0]*self.gridPixelSize, groundTile[1]*self.gridPixelSize)
            rectUL = Point(rectLR.getX()+self.gridPixelSize, rectLR.getY()+self.gridPixelSize)
            print rectLR, rectUL
            rect = Rectangle(rectLR, rectUL)
            rect.setFill("green")
            rect.draw(self.window)
            time.sleep(0.05)

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
    def __init__(self, world, name, x, y, speed = 5):
        """Commment"""
        
        
        self.world = world
        self.name = name
        self.color = color

        # Temp -> change later
        self.x = y
        self.y = x
        
        self.gridLocation = []
        self.inAir = False
        

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

class VisibleMario(object):
    """
    A visible version of an Mario object that can be viewed in a
    graphics window.
    """
    def __init__(self, agent, color):
        """Visible marios are colored sqruare objects """
        self.agent = agent
        self.window = self.agent.world.window
        self.body = Circle(Point(self.agent.x, self.agent.y), 3)
        self.body.setFill(color)

      
        self.draw()

    def translate(self, dx, dy):
        """Move the Circles representing the agent the given dx, dy amount"""
        self.body.move(dx, dy)
        
    def jump(self, dy):
        """Rotate the small Circle representing the agent's heading the 
        given amount in degrees"""
        self.body.move(0, dy)

    def draw(self):
        """Draw the agent in the world"""
        self.body.draw(self.window)
    
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

