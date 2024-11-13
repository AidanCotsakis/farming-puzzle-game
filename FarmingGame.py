# --- import moduels ---
import pygame
import os
import random
import math

# --- initiate variables ---
gameResolution = [256, 144]
fps = 30
tileSize = 16
levelOffset = [0, 0]
crops = []
playerAction = True
click = False

#settings
cropFinishedIndicator = True
targetedCropIndicator = True
selectedTileIndicator = True
screenResolution = [1920, 1080]

# --- colours ---
waterColour = (0, 205, 255)

# --- pygame setup ---
pygame.init()
clock = pygame.time.Clock()

os.environ['SDL_VIDEO_CENTERED'] = '1'
win = pygame.display.set_mode(screenResolution, pygame.NOFRAME, 0)
pygame.display.set_caption("Farming Game")

gameSurface = pygame.Surface(gameResolution) #surface that is scaled to window

# --- sprites ---
# entities: 0 = up, 1 = left, 2 = down, 3 = right
farmerSprites = [pygame.image.load('images/farmerUp.png'), pygame.image.load('images/farmerLeft.png'), pygame.image.load('images/farmerDown.png'), pygame.image.load('images/farmerRight.png')]
crowSprites = [pygame.image.load('images/crowUp.png'), pygame.image.load('images/crowLeft.png'), pygame.image.load('images/crowDown.png'), pygame.image.load('images/crowRight.png')]
shadowSprite = pygame.image.load('images/shadow.png')
# ground: 0 = light, 1 = dark
grassSprites = [pygame.image.load('images/grassLight.png'), pygame.image.load('images/grassDark.png')]
dirtSprites = [pygame.image.load('images/dirtLight.png'), pygame.image.load('images/dirtDark.png')]
#crops
cropShadowSprite = pygame.image.load('images/cropShadow.png')
cropFinishedSprite = pygame.image.load('images/blueOutline.png')
targetedCropSprite = pygame.image.load('images/redOutline.png')
selectedTileSprite = pygame.image.load('images/whiteOutline.png')

carrotSprites = []
for i in range(1,8): carrotSprites.append(pygame.image.load('images/carrot{}.png'.format(i)))
blueberrySprites = []
for i in range(1,17): blueberrySprites.append(pygame.image.load('images/blueberry{}.png'.format(i)))

cropSprites = {
	'carrot': carrotSprites,
	'blueberry': blueberrySprites
}

#hotbar
hotbarSprite = pygame.image.load('images/hotbar.png')
hotbarCountSprites = [pygame.image.load('images/hotbarCount1.png'), pygame.image.load('images/hotbarCount2.png'), pygame.image.load('images/hotbarCount3.png'), pygame.image.load('images/hotbarCount4.png'), pygame.image.load('images/hotbarCount5.png'), pygame.image.load('images/hotbarCount6.png'), pygame.image.load('images/hotbarCount7.png')]

blueberrySeedsSprite = pygame.image.load('images/blueberrySeeds.png')
carrotSeedsSprite = pygame.image.load('images/carrotSeeds.png')

seedSprites = {
	'carrot': carrotSeedsSprite,
	'blueberry': blueberrySeedsSprite
}

blueberryIconSprite = pygame.image.load('images/blueberryIcon.png')
carrotIconSprite = pygame.image.load('images/carrotIcon.png')

iconSprites = {
	'carrot': carrotIconSprite,
	'blueberry': blueberryIconSprite
}

# --- classes ---
class player(object):
	def __init__(self, location, facing, inventory):
		self.location = location
		self.facing = facing
		self.inventory = inventory
		self.offset = [0,0]
		self.moving = False
		self.verticalOffset = 0
		self.jumpHeight = 2
		self.jumpDelay = [3,3]
		self.speed = 2
		self.inventory = []
		self.selectedAction = True
		self.hotbar = [['blueberry', 2, 'seeds'],['', 0, ''],['', 0, ''],['', 0, ''],['', 0, '']]
		self.hotbarSlot = 0

	def move(self, direction):
		global playerAction

		targetTile = [-1,-1]
		if direction == 0 and self.location[1] != 0: # if moving up and not on top of board
			targetTile = [self.location[0], self.location[1]-1]
		if direction == 1 and self.location[0] != 0: # if moving left and not on top of board
			targetTile = [self.location[0]-1, self.location[1]]
		if direction == 2 and self.location[1] != (len(gameBoard)-1): # if moving down and not on top of board
			targetTile = [self.location[0], self.location[1]+1]
		if direction == 3 and self.location[0] != (len(gameBoard[0])-1): # if moving right and not on top of board
			targetTile = [self.location[0]+1, self.location[1]]

		if targetTile[0] >= 0:
			if gameBoard[targetTile[1]][targetTile[0]] == 'grass': #if target tile is grass
				# check if an entity is on target tile
				success = True
				for crow in crows:
					if targetTile == crow.location:
						success = False
				if success:
					playerAction = False
					self.moving = True
					# move player and start animation
					self.facing = direction
					self.location = targetTile

					# offset player sprite for animation
					if direction == 0: self.offset = [0,tileSize]
					if direction == 1: self.offset = [tileSize,0]
					if direction == 2: self.offset = [0,-tileSize]
					if direction == 3: self.offset = [-tileSize,0]

	def plant(self):
		global crops, playerAction

		# check if player is in range and plot is avalible
		if gameBoard[mouseCords[1]][mouseCords[0]] == 'dirt' and (mouseCords == [self.location[0] - 1, self.location[1]] or mouseCords == [self.location[0] + 1, self.location[1]] or mouseCords == [self.location[0], self.location[1] - 1] or mouseCords == [self.location[0], self.location[1] + 1]):
			success = True
			for crop in crops:
				if crop.location == mouseCords:
					success = False
			if success:
				self.selectedAction = True

				if click and self.hotbar[self.hotbarSlot][2] == 'seeds':
					playerAction = False

					crops.append(plant(self.hotbar[self.hotbarSlot][0], mouseCords))
					
					if mouseCords == [self.location[0], self.location[1] - 1]: self.facing = 0
					if mouseCords == [self.location[0] - 1, self.location[1]]: self.facing = 1
					if mouseCords == [self.location[0], self.location[1] + 1]: self.facing = 2
					if mouseCords == [self.location[0] + 1, self.location[1]]: self.facing = 3

					#remove seed from inventory
					self.hotbar[self.hotbarSlot][1] -= 1
					if self.hotbar[self.hotbarSlot][1] <= 0:
						self.hotbar[self.hotbarSlot] = ['', 0, '']

					gameAction()

	def pickup(self):
		global crops, playerAction

		# check if player is in range and plot is avalible
		if gameBoard[mouseCords[1]][mouseCords[0]] == 'dirt' and (mouseCords == [self.location[0] - 1, self.location[1]] or mouseCords == [self.location[0] + 1, self.location[1]] or mouseCords == [self.location[0], self.location[1] - 1] or mouseCords == [self.location[0], self.location[1] + 1]):
			success = False
			pickupType = ''
			for crop in crops:
				if crop.location == mouseCords and crop.age == len(cropSprites[crop.cropType]):
					success = True
					pickupType = crop.cropType
			if success:
				self.selectedAction = True

				#check if player has inventory space avalible for new crop
				if click:
					success = False
					for slot in self.hotbar:
						if slot[0] == pickupType and slot[2] == 'crops':
							success = True
					if ['',0,''] in self.hotbar:
						success = True

					#pickup crop
					if success:
						playerAction = False
							
						if mouseCords == [self.location[0], self.location[1] - 1]: self.facing = 0
						if mouseCords == [self.location[0] - 1, self.location[1]]: self.facing = 1
						if mouseCords == [self.location[0], self.location[1] + 1]: self.facing = 2
						if mouseCords == [self.location[0] + 1, self.location[1]]: self.facing = 3

						#add items to inventory
						indexCount = 0
						success = False
						for slot in self.hotbar:
							if slot[0] == pickupType and slot[2] == 'crops':
								self.hotbar[indexCount][1] += 1
								success = True
								break
							indexCount += 1

						if not success:
							indexCount = 0
							for slot in self.hotbar:
								if slot == ['', 0, '']:
									self.hotbar[indexCount] = [pickupType, 1, 'crops']
									break
								indexCount += 1

						#remove crop from tile
						indexCount = 0
						for crop in crops:
							if crop.location == mouseCords:
								crops.pop(indexCount)
							indexCount += 1



						gameAction()
					
	def draw(self):
		#update player offset movement animation
		if self.offset[0] > 0:
			self.offset[0] -= self.speed
		if self.offset[0] < 0:
			self.offset[0] += self.speed
		if self.offset[1] > 0:
			self.offset[1] -= self.speed
		if self.offset[1] < 0:
			self.offset[1] += self.speed

		#animate player jump
		if abs(self.offset[0] + self.offset[1]) > self.jumpDelay[0] and abs(self.offset[0] + self.offset[1]) < tileSize - self.jumpDelay[1]:
			if self.verticalOffset != self.jumpHeight:
				self.verticalOffset += 1
		elif self.verticalOffset != 0:
			self.verticalOffset -= 1

		#draw sprites
		gameSurface.blit(shadowSprite, (self.location[0]*tileSize+levelOffset[0]+self.offset[0],self.location[1]*tileSize+levelOffset[1]+self.offset[1]))
		gameSurface.blit(farmerSprites[self.facing], (self.location[0]*tileSize+levelOffset[0]+self.offset[0],self.location[1]*tileSize-tileSize+levelOffset[1]+self.offset[1]-self.verticalOffset))

		#end animation
		if self.moving and self.offset == [0,0]:
			self.moving = False
			gameAction()

class crow(object):
	def __init__(self, location, facing):
		self.location = location
		self.facing = facing
		self.offset = [0,0]
		self.verticalOffset = 0
		self.speed = 2
		self.verticalOffset = 0
		self.jumpHeight = 2
		self.jumpDelay = [3,3]
		self.moving = False

	def pathfind(self):
		#make a copy of game board
		gamestate = []
		for row in gameBoard:
			gamestate.append(row[:])

		#scan and isolate grass tiles
		for i in range(len(gamestate)):
			for j in range(len(gamestate[0])):
				if gamestate[i][j] == 'grass':
					gamestate[i][j] = -1
				else:
					gamestate[i][j] = -2

		gamestate[farmer.location[1]][farmer.location[0]] = -2

		for bird in crows:
			gamestate[bird.location[1]][bird.location[0]] = -2
		
			gamestateOld = []
			for row in gamestate:
				gamestateOld.append(row[:])

		#start pathfinding
		direction = -1
		if len(crops) > 0:
			if gamestate[crops[0].location[1]+1][crops[0].location[0]] == -1: gamestate[crops[0].location[1]+1][crops[0].location[0]] = 1
			if gamestate[crops[0].location[1]-1][crops[0].location[0]] == -1: gamestate[crops[0].location[1]-1][crops[0].location[0]] = 1
			if gamestate[crops[0].location[1]][crops[0].location[0]+1] == -1: gamestate[crops[0].location[1]][crops[0].location[0]+1] = 1
			if gamestate[crops[0].location[1]][crops[0].location[0]-1] == -1: gamestate[crops[0].location[1]][crops[0].location[0]-1] = 1

			#flood board with distance from primary crop
			distance = 1
			while gamestate != gamestateOld:
				#save gamestate for comparison
				gamestateOld = []
				for row in gamestate:
					gamestateOld.append(row[:])

				for i in range(len(gamestate)):
					for j in range(len(gamestate[0])):
						if gamestate[i][j] == -1 and gamestate[i+1][j] == distance: gamestate[i][j] = distance + 1
						if gamestate[i][j] == -1 and gamestate[i-1][j] == distance: gamestate[i][j] = distance + 1
						if gamestate[i][j] == -1 and gamestate[i][j+1] == distance: gamestate[i][j] = distance + 1
						if gamestate[i][j] == -1 and gamestate[i][j-1] == distance: gamestate[i][j] = distance + 1

				distance += 1

			smallestTartget = math.inf
			#check facing direction
			if self.facing == 0 and gamestate[self.location[1]-1][self.location[0]] > 0:
				smallestTartget = gamestate[self.location[1]-1][self.location[0]]
				direction = 0
			elif self.facing == 1 and gamestate[self.location[1]][self.location[0]-1] > 0:
				smallestTartget = gamestate[self.location[1]][self.location[0]-1]
				direction = 1
			elif self.facing == 2 and gamestate[self.location[1]+1][self.location[0]] > 0:
				smallestTartget = gamestate[self.location[1]+1][self.location[0]]
				direction = 2
			elif self.facing == 3 and gamestate[self.location[1]][self.location[0]+1] > 0:
				smallestTartget = gamestate[self.location[1]][self.location[0]+1]
				direction = 3

			#check if other directions has a faster result
			if gamestate[self.location[1]-1][self.location[0]] > 0 and gamestate[self.location[1]-1][self.location[0]] < smallestTartget:
				smallestTartget = gamestate[self.location[1]-1][self.location[0]]
				direction = 0
			if gamestate[self.location[1]][self.location[0]-1] > 0 and gamestate[self.location[1]][self.location[0]-1] < smallestTartget:
				smallestTartget = gamestate[self.location[1]][self.location[0]-1]
				direction = 1
			if gamestate[self.location[1]+1][self.location[0]] > 0 and gamestate[self.location[1]+1][self.location[0]] < smallestTartget:
				smallestTartget = gamestate[self.location[1]+1][self.location[0]]
				direction = 2
			if gamestate[self.location[1]][self.location[0]+1] > 0 and gamestate[self.location[1]][self.location[0]+1] < smallestTartget:
				smallestTartget = gamestate[self.location[1]][self.location[0]+1]
				direction = 3
				
		if direction >= 0:
			self.move(direction)

	def move(self, direction):
		targetTile = [-1,-1]
		if direction == 0: # if moving up
			targetTile = [self.location[0], self.location[1]-1]
		if direction == 1: # if moving left
			targetTile = [self.location[0]-1, self.location[1]]
		if direction == 2: # if moving down
			targetTile = [self.location[0], self.location[1]+1]
		if direction == 3: # if moving right
			targetTile = [self.location[0]+1, self.location[1]]

		self.moving = True
		# move crow and start animation
		self.facing = direction
		self.location = targetTile

		# offset crow sprite for animation
		if direction == 0: self.offset = [0,tileSize]
		if direction == 1: self.offset = [tileSize,0]
		if direction == 2: self.offset = [0,-tileSize]
		if direction == 3: self.offset = [-tileSize,0]

	def draw(self):
		#update player offset movement animation
		if self.offset[0] > 0:
			self.offset[0] -= self.speed
		if self.offset[0] < 0:
			self.offset[0] += self.speed
		if self.offset[1] > 0:
			self.offset[1] -= self.speed
		if self.offset[1] < 0:
			self.offset[1] += self.speed

		#animate player jump
		if abs(self.offset[0] + self.offset[1]) > self.jumpDelay[0] and abs(self.offset[0] + self.offset[1]) < tileSize - self.jumpDelay[1]:
			if self.verticalOffset != self.jumpHeight:
				self.verticalOffset += 1
		elif self.verticalOffset != 0:
			self.verticalOffset -= 1

		#draw sprites
		gameSurface.blit(shadowSprite, (self.location[0]*tileSize+levelOffset[0]+self.offset[0],self.location[1]*tileSize+levelOffset[1]+self.offset[1]))
		gameSurface.blit(crowSprites[self.facing], (self.location[0]*tileSize+levelOffset[0]+self.offset[0],self.location[1]*tileSize-tileSize+levelOffset[1]+self.offset[1]-self.verticalOffset))

		#end animation
		if self.moving and self.offset == [0,0]:
			self.moving = False

class plant(object):
	def __init__(self, cropType, location):
		self.location = location
		self.cropType = cropType
		self.offset = [random.randint(0,1), random.randint(0,1)]
		self.age = 0

	def draw(self):
		if self.age > 0:
			gameSurface.blit(cropShadowSprite, (self.location[0]*tileSize+levelOffset[0]+self.offset[0],self.location[1]*tileSize+levelOffset[1]+self.offset[1]))
			gameSurface.blit(cropSprites[self.cropType][self.age-1], (self.location[0]*tileSize+levelOffset[0]+self.offset[0],self.location[1]*tileSize-tileSize+levelOffset[1]+self.offset[1]))
		
		if self.age == len(cropSprites[self.cropType]) and cropFinishedIndicator:
			gameSurface.blit(cropFinishedSprite, (self.location[0]*tileSize+levelOffset[0],self.location[1]*tileSize+levelOffset[1]))

	def grow(self):
		if self.age < len(cropSprites[self.cropType]):
			self.age += 1

# --- functions ---
def levelSetup(level):
	global gameBoard, farmer, crows
	# game array
	gameBoard = [
	['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
	['', '', '', '', '', 'grass', 'grass', 'grass', '', 'grass', 'grass', '', '', '', '', ''],
	['', '', '', '', '', 'grass', 'dirt', 'grass', '', 'grass', 'grass', '', '', '', '', ''],
	['', '', '', '', '', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', '', '', '', '', ''],
	['', '', '', '', '', 'grass', 'grass', 'grass', 'grass', 'grass', 'grass', '', '', '', '', ''],
	['', '', '', '', '', 'grass', 'dirt', 'grass', '', 'grass', 'grass', '', '', '', '', ''],
	['', '', '', '', '', 'grass', 'grass', 'grass', '', 'grass', 'grass', '', '', '', '', ''],
	['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
	['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
	]
	#init members of player and crow classes
	farmer = player([5,1], 2, [])
	crows = [crow([10,6], 1)]

def gameAction():
	global playerAction
	
	for bird in crows:
		bird.pathfind()

	for crop in crops:
		crop.grow()

	playerAction = True

def draw():
	#water
	gameSurface.fill(waterColour)

	#tiles
	lightTile = True
	for y in range(len(gameBoard)):

		# reset tile brightness after each line
		if y % 2 == 0:
			lightTile = True
		else:
			lightTile = False

		for x in range(len(gameBoard[0])):
			#grassTiles
			if gameBoard[y][x] == 'grass':
				if lightTile:
					gameSurface.blit(grassSprites[0], (x * tileSize + levelOffset[0], y * tileSize + levelOffset[1]))
				else:
					gameSurface.blit(grassSprites[1], (x * tileSize + levelOffset[0], y * tileSize + levelOffset[1]))

			#grassTiles
			if gameBoard[y][x] == 'dirt':
				if lightTile:
					gameSurface.blit(dirtSprites[0], (x * tileSize + levelOffset[0], y * tileSize + levelOffset[1]))
				else:
					gameSurface.blit(dirtSprites[1], (x * tileSize + levelOffset[0], y * tileSize + levelOffset[1]))

			lightTile = not lightTile

	#draw entities
	for crop in crops:
		crop.draw()

	# draw indicators
	if targetedCropIndicator and len(crops) > 0: 
		gameSurface.blit(targetedCropSprite, (crops[0].location[0]*tileSize+levelOffset[0],crops[0].location[1]*tileSize+levelOffset[1]))

	if farmer.selectedAction:
		gameSurface.blit(selectedTileSprite, (mouseCords[0]*tileSize+levelOffset[0],mouseCords[1]*tileSize+levelOffset[1]))
		farmer.selectedAction = False

	farmer.draw()

	for crow in crows:
		crow.draw()

	#hotbar
	hotbarCords = [gameResolution[0]/2-(10*math.floor(len(farmer.hotbar)/2))-4, gameResolution[1]-2]
	for i in range(len(farmer.hotbar)):
		# draw slots
		if farmer.hotbarSlot == i:
			gameSurface.blit(hotbarSprite, (hotbarCords[0], hotbarCords[1]-2))
		else:
			gameSurface.blit(hotbarSprite, (hotbarCords[0], hotbarCords[1]-1))

		#draw counters
		if farmer.hotbar[i][1] > 0 and farmer.hotbar[i][1] < 7:
			gameSurface.blit(hotbarCountSprites[farmer.hotbar[i][1]-1], (hotbarCords[0] + 7, hotbarCords[1]-10))
		elif farmer.hotbar[i][1] >= 7:
			gameSurface.blit(hotbarCountSprites[6], (hotbarCords[0] + 7, hotbarCords[1]-10))

		#draw icons
		if farmer.hotbar[i][2] == 'seeds':
			gameSurface.blit(seedSprites[farmer.hotbar[i][0]], (hotbarCords[0], hotbarCords[1]-10))

		if farmer.hotbar[i][2] == 'crops':
			gameSurface.blit(iconSprites[farmer.hotbar[i][0]], (hotbarCords[0], hotbarCords[1]-10))

		hotbarCords[0] += 10

	#update screen
	gameBlit = pygame.transform.scale(gameSurface, screenResolution)
	win.blit(gameBlit, (0,0))
	pygame.display.update()

levelSetup(1) #run initial setup of board
# --- game loop ---
while True:
	clock.tick(fps) # run loop 'fps' times per second
	
	for event in pygame.event.get(): #check pygame events
		if event.type == pygame.QUIT:
			pygame.quit()
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				click = True
			if event.button == 4:
				farmer.hotbarSlot -= 1
				if farmer.hotbarSlot < 0:
					farmer.hotbarSlot = len(farmer.hotbar)-1

			if event.button == 5:
				farmer.hotbarSlot += 1
				if farmer.hotbarSlot >= len(farmer.hotbar):
					farmer.hotbarSlot = 0

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w and playerAction: #listen for 'w'
				farmer.move(0)
			if event.key == pygame.K_a and playerAction: #listen for 'a'
				farmer.move(1)
			if event.key == pygame.K_s and playerAction: #listen for 's'
				farmer.move(2)
			if event.key == pygame.K_d and playerAction: #listen for 's'
				farmer.move(3)

	if playerAction:
		mouseX, mouseY = pygame.mouse.get_pos()
		#convert full screen mouse cords into grid cords
		mouseCords = [math.floor(mouseX/((screenResolution[0]/gameResolution[0])*tileSize)), math.floor(mouseY/((screenResolution[1]/gameResolution[1])*tileSize))]

		farmer.plant()
		farmer.pickup()

	#draw screen
	draw()

	if click:
		click = False
