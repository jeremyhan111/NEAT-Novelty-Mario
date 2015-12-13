from math import sqrt
import sys
import random
from time import sleep

class NoveltySearch(object):
	def __init__(self, k, limit, threshold, pointLength, behaviorLength, maxDistance):
		"""Initialize NoveltySearch object:
		-----------Parameters-----------
		self: self object
		k: number of neighbors from which to calculate distance
		limit: maximum size of archive
		threshold: sets the boundary for how novel a behavior must be 
			to be placed into archive
		pointLength: length of points (i.e (1,2,4) has pointLength of 3)
		behaviorLength: number of points within a behavior description
		"""
		self.archive = []
		self.k = k
		self.limit = limit
		self.threshold = threshold # float
		self.pointLength = pointLength
		self.behaviorLength = behaviorLength
		self.steps = 0 # incremented everytime checkArchive is run
		self.growth = [] 
		self.maxDistance = maxDistance


	def distance(self, p1, p2):
		"""Calculates distance between points p1 and p2, which can be of any 
			 length as long as they are have the same dimensions
		-----------Parameters-----------
		self: self object
		p1 and p2: finds distance between these points
		------------Return--------------
		sqrt(d): squareroots distance as part of Pythagorean's theorem
		"""

		d = 0

		for i in range(self.pointLength):
			d = d + (p1[i] - p2[i])**2

		return sqrt(d)


	def distFromkNearest(self, behavior):
		"""Calculates the sum of the distances of the given behavior with its 
			 k-nearest neighbors in the archive 
			 -----------Parameters-----------
		self: self object
		behavior: list of points that represent the behavior
		------------Return--------------
		returnDistance: sum of distances from k-nearest neighbors
		"""
		
		distanceList = [] # list of distances between behavior and each neighbor

		# print "behavior:", behavior

		for item in self.archive: # for each behavior in the archive
			summedDistance = 0 # total distance from archive behavior

			for j in range(self.behaviorLength): #for each point in behavior

				# if self.distance(behavior[j], item[0][j]) > 10:
				# 	print "UHHHH"
				# 	print self.distance(behavior[j], item[0][j])
				# 	print behavior[j], item[0][j]

				#calculate the distance(given behavior, archive behavior)
				summedDistance = summedDistance + self.distance(behavior[j], \
								 item[0][j])
				

				# print behavior[j], item[0][j], "has dist", self.distance(behavior[j], item[0][j])
				# sleep(5)

			distanceList.append(summedDistance) #store distance in list

		distanceList.sort() #sort the list of distances from low to high

		returnDistance = 0

		# print "distList:",
		for i in range(self.k): # add together the lowest k distances together
			# print distanceList[i], 
			returnDistance = returnDistance + distanceList[i]

		# sleep(5)

		# print "distance List:", distanceList

		# print "k", self.k, "returnDistance", returnDistance
		# sleep(2)
		

		return returnDistance


	def sparseness(self, behavior):
		"""Calculates the sparseness of the given behavior where sparseness is
			 the average distance of the  behavior from its k nearest neighbors.
		-----------Parameters-----------
		self: self object
		behavior: list of points that represent the behavior
		------------Return--------------
		sparseness: sparseness of appended behavior
		"""

		if len(self.archive) == 0: #no items in archive
			return 1.0

		elif len(self.archive) < self.k: #archive has less than k items
			temp = self.k #keep track of the given k
			self.k = len(self.archive) 
			toReturn = self.distFromkNearest(behavior)*1.0/self.k
			self.k = temp #revert k back to its original value

			# print "\nlessK: toReturn", toReturn, "maxDistance", self.maxDistance
			# sleep(2)
			
			return toReturn/self.maxDistance

		else: #normal case
			# print "\n normal: toReturn", self.distFromkNearest(behavior)*1.0/self.k, "maxDistance", self.maxDistance
			# sleep(2)
			return (self.distFromkNearest(behavior)*1.0/self.k)/self.maxDistance


	def checkArchive(self, behavior, otherInfo=None):
		"""Checks if the given behavior is novel enough to be added
			 to the archive. 
		 -----------Parameters-----------
		self: self object
		behavior: list of points that represent the behavior
		otherInfo: otherInfo user may want to put into archive
		------------Return--------------
		sparseness: sparseness of appended behavior
		"""
		self.steps = self.steps + 1 #increment the # of steps we've taken
		sparse = self.sparseness(behavior) #calculate sparseness

		if len(self.archive) < self.k: # archive length is less than k
			self.archive.append((behavior, sparse, otherInfo)) # append behavior

			#add growth information to growth list
			self.growth.append((self.steps, len(self.archive))) 
			
			return sparse
		
		else:
			if sparse <= self.threshold: # not novel enough, don't add
				return sparse
			
			else: # behavior is novel enough, add it to archive
				self.archive.append((behavior, sparse, otherInfo))

				if len(self.archive) > self.limit: # archive is now too long
					self.archive.pop(0) # remove the oldest behavior

				#add growth information to growth list
				self.growth.append((self.steps, len(self.archive)))
				
				return sparse


	def saveArchive(self, filename):
		"""Save archive information into an .archive file. 
		-----------Parameters-----------
		self: self object
		filename: name of file
		------------Return--------------
		None:
		"""
		
		fp = open(filename, "w")
		if fp < 0:
			print "error opening file. Exiting"
			exit()

		counter = 0
		for item in self.archive: # for each behavior in the archive
			fp.write('"Behavior%d\n' % (counter)) # write out behavior number
			counter = counter + 1
			behavior = item[0]
			
			for point in behavior: # write out all the points for the behavior
				
				for i in range(self.pointLength):
					fp.write("%.5f " % (point[i]))
				
				fp.write("\n")
			
			fp.write("\n")

		fp.close()

	def saveGrowth(self, filename):
		"""Writes out a record of when additions were made to the archive in a
		.growth file. Convention is (step #, archive size)
		 -----------Parameters-----------
		self: self object
		filename: name of file
		------------Return--------------
		None:
		"""

		fp = open(filename, "w")
		if fp < 0:
			print "error opening file. Exiting"
			exit()
			
		for item in self.growth:
			fp.write("%d %d\n" % (item[0], item[1]))

		fp.close()


def unitTests():
	"""Testing functions that help us verify the correctness of our code
	-----------Parameters-----------
	None:
	------------Return--------------
	None:
	"""
	
	# creates various noveltySearch objects for testing purposes


	k = 3
	limit = 10
	threshold = 0.5
	pointLength = 3
	behaviorLength = 3

	# for testDistance and testDistFromkNearest
	Novel = NoveltySearch(k, limit, threshold, pointLength, behaviorLength, 10)

	k1 = 5
	limit1 = 8
	threshold1 = 0.75
	pointLength1 = 2
	behaviorLength1 = 4	

	# for testDistance1 and testSparseness
	Novel1 = NoveltySearch(k1, limit1, threshold1, pointLength1, behaviorLength1, 8*sqrt(2)) 
	
	# for testCheckArchive
	Novel3 = NoveltySearch(k1, limit1, threshold1, pointLength1, behaviorLength1, 10)
	
	# for testSaveArchive
	Novel4 = NoveltySearch(k1, limit1, threshold1, pointLength1, 2, 10)

	k2 = 4
	limit2 = 6
	threshold2 = 0.3
	pointLength2 = 4
	behaviorLength2 = 6

	# for testDist2
	Novel2 = NoveltySearch(k2, limit2, threshold2, pointLength2, behaviorLength2, 10)

	print "Unit testing ... ... ..."

	if not testDistance(Novel):
		print "testDistance not passed"
		exit()

	if not testDistance1(Novel1):
		print "testDistance1 not passed"
		exit()

	if not testDistance2(Novel2):
		print "testDistance2 not passed"
		exit()

	if not testDistFromkNearest(Novel):
		print "testDistFromkNearest not passed"
		exit()

	if not testSparseness(Novel1):
		print "testSparseness not passed"

	if not testCheckArchive(Novel3):
		print "testCheckArchive not passed"

	if not testSaveArchive(Novel4):
		print "testSaveArchive not passed"

	if not testSaveGrowth(Novel3):
		print "testSaveGrowth not passed"

	print "Passed unit tests!"


def testDistance(noveltySearch):
	""" Check distance function for 3 dimension points
	-----------Parameters-----------
	noveltySearch: object used to test our distance function
	------------Return--------------
	boolean: true if passed
	"""
	
	if noveltySearch.distance((0, 0, 0), (10, 11, 15)) != sqrt(446):
		return False

	if noveltySearch.distance((-4, 5, -8),(1, 9, 14)) != sqrt(525):
		return False

	return True

def testDistance1(noveltySearch):
	""" Check distance function for 2 dimension points
	-----------Parameters-----------
	noveltySearch: object used to test our distance function
	------------Return--------------
	boolean: true if passed
	"""
	
	if noveltySearch.distance((0, 0), (3, 4)) != 5:
		return False
	
	if noveltySearch.distance((-7, 10), (1, 9)) != sqrt(65):
		return False

	return True

def testDistance2(noveltySearch):
	""" Check distance function for 4 dimension points
	-----------Parameters-----------
	noveltySearch: object used to test our distance function
	------------Return--------------
	boolean: true if passed
	"""
	
	if noveltySearch.distance((0, 0, 0, 0), (1, 2, 3, 4)) != sqrt(30):
		return False
	
	if noveltySearch.distance((9, -9, 7, 2), (1, 15, 9, 0)) != sqrt(648):
		return False

	return True

def testDistFromkNearest(noveltySearch):
	""" Check distFromkNearest function for 3 dimension points
	-----------Parameters-----------
	noveltySearch: object used to test our distfromknearest function
	------------Return--------------
	boolean: true if passed
	"""
	
	behavior1 = ((7, -9, 0), (13, 4, 1), (-11, 9, 3))
	behavior2 = ((0, 5, -3), (17, 3, 8), (4, 9, 0))
	behavior3 = ((19, 25, 81), (17, 20, 14), (90, 91, 93))
	behavior4 = ((100, 500, 900), (700, 60, 10), (90, 100, 7))
	behavior5 = ((3, 4, 5), (1, 2, 3), (7, 8, 9))

	noveltySearch.archive.append((behavior1, 0, 0))
	noveltySearch.archive.append((behavior2, 0, 0))
	noveltySearch.archive.append((behavior3, 0, 0))
	noveltySearch.archive.append((behavior4, 0, 0))
	noveltySearch.archive.append((behavior5, 0, 0))

	testBehavior = ((2, 5, 6), (1, 3, 4), (3, 6, 7))

	# hand calculated expected distance
	answer = sqrt(257) + sqrt(154) + sqrt(221) + sqrt(85) + sqrt(272) + \
	sqrt(59) + sqrt(3) + sqrt(2) + sqrt(24)

	# rounding error prevents us from using equal sign
	if answer - noveltySearch.distFromkNearest(testBehavior) > 0.0000000001:
		return False
	
	return True

def testSparseness(noveltySearch):
	""" Check sparseness function for 2 dimension points
	-----------Parameters-----------
	noveltySearch: object used to test our sparseness function
	------------Return--------------
	boolean: true if passed
	"""
	
	testBehavior = ((0, 0), (0, 0), (0, 0), (0, 0))

	#testing case where nothing is in archive
	if noveltySearch.sparseness(testBehavior) != 1:
		return False

	#testing case where len(archive) < k
	behavior1 = ((1, 1), (1, 1), (1, 1), (1, -1))
	behavior2 = ((-1, -1), (-1, -1), (-1, -1), (-1, 1))
	behavior3 = ((-1, 1), (-1, 1), (1, -1), (1, 1))
	noveltySearch.archive.append((behavior1, 0, 0))
	noveltySearch.archive.append((behavior2, 0, 0))
	noveltySearch.archive.append((behavior3, 0, 0))

	if noveltySearch.sparseness(testBehavior) != 4*sqrt(2)/noveltySearch.maxDistance:
		return False

	#testing case where len(archive) >= k
	behavior4 = ((1, 1), (1, 1), (1, 1), (1, -1))
	behavior5 = ((-1, -1), (-1, -1), (-1, -1), (-1, 1))
	behavior6 = ((-1, 1), (-1, 1), (1, -1), (1, 1))
	noveltySearch.archive.append((behavior4, 0, 0))
	noveltySearch.archive.append((behavior5, 0, 0))
	noveltySearch.archive.append((behavior6, 0, 0))

	if noveltySearch.sparseness(testBehavior) != 4*sqrt(2)/noveltySearch.maxDistance:
		return False

	return True

def testCheckArchive(noveltySearch):
	""" Check checkArchive function for 2 dimension points
	-----------Parameters-----------
	noveltySearch: object used to test if checkArchive works
	------------Return--------------
	boolean: true if passed
	"""

	behavior1 = ((-1, 1), (1, 1), (1, 1), (1, -1))

	noveltySearch.checkArchive(behavior1)

	# check that behavior was added because archive len < k
	if len(noveltySearch.archive) != 1:
		return False

	# list of behaviors
	behavior2 = ((-20, -1), (-1, -1), (-1, -1), (-1, 1))
	behavior3 = ((-1, 1), (-1, 1), (1, -1), (1, 1))
	behavior4 = ((1, 2), (1, 13), (1, 51), (1, -14))
	behavior5 = ((-5, 19), (-4, 1), (7, -4), (3, 9))
	behavior6 = ((-1, -1), (-1, -1), (-1, -1), (-1, 1))
	behavior7 = ((-1, -1), (-1, -1), (-1, -1), (-12, 1))
	behavior8 = ((-1, 14), (-1, 61), (1, -1), (18, 1))
	behavior9 = ((-21, -1), (-1, -12), (-1, -1), (-12, 1))
	behavior10 = ((-121, -1), (-12, -12), (-17, -41), (-12, 991))

	noveltySearch.checkArchive(behavior2)

	if len(noveltySearch.archive) != 2: # check that behavior was added
		return False

	noveltySearch.checkArchive(behavior3)
	noveltySearch.checkArchive(behavior4)
	noveltySearch.checkArchive(behavior5)

	if len(noveltySearch.archive) != 5: # check that behavior was added
		return False

	#increase threshold so that behavior 6 is not added
	newThresh = noveltySearch.sparseness(behavior6)*1.01
	noveltySearch.threshold = newThresh

	# check to see that behavior6 was not added
	noveltySearch.checkArchive(behavior6)
	if len(noveltySearch.archive) != 5:
		return False

	noveltySearch.checkArchive(behavior7)
	noveltySearch.checkArchive(behavior8)
	noveltySearch.checkArchive(behavior9)
	noveltySearch.checkArchive(behavior10)

	# check that length of archive is still at limit
	if len(noveltySearch.archive) != noveltySearch.limit: 
		return False

	# check that oldest behavior was indeed removed
	if noveltySearch.archive[0][0] == behavior1:
		return False

	return True


def testSaveArchive(noveltySearch):
	""" Check saveArchive function for 2 dimension points
	-----------Parameters-----------
	noveltySearch: object used to save and graph archive
	------------Return--------------
	boolean: true if passed
	"""

	behavior1 = ((0, 0), (1, 1))
	behavior2 = ((1, 0), (0, 1))

	noveltySearch.archive.append((behavior1, 0, 0))
	noveltySearch.archive.append((behavior2, 0, 0))


	#When graphed, should create cross
	noveltySearch.saveArchive("hi.archive")

	# Look, it's a cross. Passed!
	return True

def testSaveGrowth(noveltySearch):
	""" Check saveGrowth function for 3 dimension points
	-----------Parameters-----------
	noveltySearch: noveltySearch object we used in testCheckArchive
	to see if its growth graph reflects our appends to its archive
	------------Return--------------
	boolean: true if passed
	"""

	noveltySearch.saveGrowth("bye.growth")

	# Looks good. Passed. Graphs the appends done in testCheckArchive
	return True


if __name__ == '__main__':
	unitTests()
	# Max sparseness is 3*sqrt(2)
	k = 5
	limit = 30
	pointLength = 2
	behaviorLength = 3

	# thresholds above 35% of max sparseness will cause archive to hit the limit
	# very quickly. Below 30% of max sparseness, the archive doesn't hit the
	# limit in 1000 loops. The smallest value that allows the archive to just
	# hit the limit of 30 in 1000 loops is 1.302, which is about 30.7% of the 
	# max sparseness
	threshold = 0.307*3*sqrt(2)
	NovelTest = NoveltySearch(k, limit, threshold, pointLength, behaviorLength, 3*sqrt(2))

	for i in range(1000):
		behavior = ((random.random(), random.random()), \
		(random.random(), random.random()), (random.random(), random.random()))
		NovelTest.checkArchive(behavior)

	NovelTest.saveArchive("main.archive")
	NovelTest.saveGrowth("main.growth")



