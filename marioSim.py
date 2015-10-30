from graphics import *
# from time import sleep
# from math import sin, cos, radians, sqrt, floor
# from random import random, randrange


class World(object):
	"""
	comment
	"""

	def __init__(self, name, width, height, delay = 0.025):
		""" comment """

		self.name = name
		self.width = width
		self.height = height
		self.delay = delay
        self.marios = []
        self.coins = []
        self.goombas = []
        self.boxes = []
        self.hiddenRoom = []

        self.madeWin = False


    def makeVisible(self):
        """Creates a graphics window making the world visible"""
        self.window = GraphWin(self.name, self.width, self.height)

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
    def __init__(self, name, color = "red"):
        """Commment"""

        self.name = name
        self.color = color

        # Temp -> change later
        self.x = 0
        self.y = 0
        self.inAir = False


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

