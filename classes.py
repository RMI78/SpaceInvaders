import pygame
from functions import *
import math



#classe which represent the aim
class Aim:
	def __init__(self, display):
		self.display = display
		self.image = pygame.transform.scale(load_file("./pictures/aim.png"), percentPix((2,2)))

	#the update method for the position
	def focusAim(self):
		self.display.blit(self.image, pygame.mouse.get_pos())

#class which represent the bullet
class Bullet:
	def __init__(self, display, x, y, height):
		self.image = pygame.transform.scale(load_file("./pictures/bullet.png"), percentPix((2,2)))
		self.x = x
		self.y = y
		self.b = y+height/2
		self.xMouse, self.yMouse = pygame.mouse.get_pos()
		self.coof = (self.yMouse-self.y)/(self.xMouse-self.x)
		if self.coof > 0.1:
			self.coof = 0.1

		elif self.coof < -0.1:
			self.coof = -0.1


	def update(self):
		self.x +=10
		self.y = self.coof * self.x +self.b

#class which represent the current player
class Player:
	def __init__(self, display):
		self.display = display
		self.image = pygame.transform.scale(load_file("./pictures/spaceShip.png"), percentPix((8,10)))
		self.rect = self.image.get_rect()
		self.height = self.rect[-1]
		self.width = self.rect[-2]
		self.widthDisplay, self.heightDisplay = pygame.display.get_surface().get_size()
		self.bullet = Bullet
		self.list_bullets = []
		self.alive = True
		self.speed = 10

	def move(self, posx, posy):
		"""
		The move method to let the player move

		:param posx, posy:
		:return:
		"""
		self.widthDisplay, self.heightDisplay = pygame.display.get_surface().get_size()
		if posy == 1 and self.rect.y <= self.heightDisplay-self.height:
			self.rect.y += self.speed
		elif posy == -1 and self.rect.y > 0:
			self.rect.y -= self.speed
		elif posx == 1 and self.rect.x <= (self.widthDisplay-self.width)//2:
			self.rect.x += self.speed
		elif posx == -1 and self.rect.x > 0 :
			self.rect.x -= self.speed

	def shoot(self):
		self.list_bullets.append(self.bullet(self.display, self.rect.x, self.rect.y, self.height))

	def update(self):
		for bullet in self.list_bullets:
			bullet.update()
			if bullet.x > pygame.display.get_surface().get_size()[0] or bullet.y > pygame.display.get_surface().get_size()[-1]:
				del(self.list_bullets[self.list_bullets.index(bullet)])

			else:
				self.display.blit(bullet.image, (bullet.x, bullet.y))

		self.display.blit(self.image, (self.rect.x, self.rect.y))


"""class which create buttons
arguments: Coords: tuple, Surface: Surface object, Size: tuple, Text: string, Font: Font object, Image = String
to use, proceed this way:
if event.type == MOUSEBUTTONDOWN and event.button == 1:
	mouse = pygame.mouse.get_pos
	if Button.imageRect.colliderect(mouse)"""
class Button:
	def __init__(self, Coords, Surface, Size, Text=None, Font=None, Image=None):
		self.coords = Coords
		self.surface = Surface
		self.size = Size
		self.surface = Surface
		if Text:
			self.text = Text
		if Image:
			#try to use the image to create and blit a button with itself
			try:
				self.image = load_file(Image)
				self.image = pygame.transform.scale(self.image, (Size))
				self.imageRect = self.image.get_rect()
				self.imageRect.center = self.coords
			except:
				Image=None
		if Image == None :
			#create and blit a basic button if any image is loaded or if the loading of the image fail
			self.reducedSize = tuple(map(operator.sub, self.size, percentPix((1,1))))
			self.image = pygame.Surface(self.size)
			self.image2 = pygame.Surface(self.reducedSize)
			self.imageRect = self.image.get_rect()
			self.image2Rect = self.image.get_rect()
			self.image.fill([255, 255, 255])
			self.image2.fill([0, 0, 0])
			self.imageRect.center = self.coords
			self.image2Rect.center = tuple(map(operator.add, self.coords, percentPix((0.5, 0.5))))

		if Font:
			if Image:
				self.font = Font.render(self.text, True, [0,0,0])
			if Image == None:
				self.font = Font.render(self.text, True, [255, 255, 255])
			self.fontRect = self.font.get_rect()
			self.fontRect.center = self.imageRect.center

		self.area = tuple(map(operator.sub, self.imageRect.bottomright, self.imageRect.topleft))


	def display(self):
		self.surface.blit(self.image, self.imageRect)
		try:
			self.surface.blit(self.image2, self.image2Rect)
		except:pass
		self.surface.blit(self.font, self.fontRect)

	def move(self, coords):
		self.imageRect.move(coords)
		self.fontRect.move(coords)
		self.display()











#class enemy(pygame.sprite.Sprite):
