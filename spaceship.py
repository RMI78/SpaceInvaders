import pygame
from functions import *
import math
import random


class Bullet:
	def __init__(self, x, y, height, angle=0,  speed=20, type=True, xTarget=None, yTarget=None):
		self.image = pygame.transform.scale(load_file("./pictures/bullet.png"), percentPix((2,2)))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = (x, y)
		self.speed = speed
		if type:
			self.xTarget, self.yTarget = pygame.mouse.get_pos()
		else:
			self.xTarget, self.yTarget = (xTarget, yTarget)
			self.speed = -self.speed

		self.coof = ((self.yTarget-height/2)-self.rect.y)/(self.xTarget-self.rect.x)
		self.b = self.rect.y - self.coof*self.rect.x+height/2
		self.angle = angle
		#print(self.angle)
		self.image = pygame.transform.rotate(self.image, self.angle)

	def update(self):
		self.rect.x +=self.speed
		self.rect.y = self.coof * self.rect.x +self.b

class SpaceShip:
	def __init__(self, display, x, y, image, direction=True, frequency=20):
		self.display = display
		self.strForImage2 = image[:len(image)-4] + '2' + image[-4:]
		self.strForImage3 = image[:len(image)-4] + '3' + image[-4:]
		self.image = pygame.transform.scale(load_file(image), percentPix((9,10)))
		self.image2 = pygame.transform.scale(load_file(self.strForImage2), percentPix((9,10)))
		self.image3 = pygame.transform.scale(load_file(self.strForImage3), percentPix((9,10)))
		if not direction:
			self.image = pygame.transform.flip(self.image, True, False)
			self.image2 = pygame.transform.flip(self.image2, True, False)
		self.currentImage = self.image
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = (x, y)
		self.height, self.width= (self.rect[-1], self.rect[-2])
		self.widthDisplay, self.heightDisplay = pygame.display.get_surface().get_size()
		self.bullet = Bullet
		self.list_bullets = []
		self.alive = True
		self.incrementFor1Second = 0
		self.frequency = frequency
		self.lastShots = self.frequency

	def shoot(self, player=None):
		if self.lastShots > 0:
			if player:
				if random.randint(0,800)<50:
					self.list_bullets.append(self.bullet(self.rect.x, self.rect.y, self.height, 0, 10, False, player.spacecraft.rect.x, player.spacecraft.rect.y+player.spacecraft.height/2))
			if not player:
				self.list_bullets.append(self.bullet(self.rect.x, self.rect.y, self.height, -1*mouseAngle(self)))
			self.lastShots = self.lastShots-1
		else: pass

	def update(self):
		self.incrementFor1Second += 1
		if self.incrementFor1Second == 1:
			self.currentImage = self.image
		elif self.incrementFor1Second == 30:
			self.currentImage = self.image2
		elif self.incrementFor1Second == 60:
			self.currentImage = self.image3
			self.lastShots = self.frequency
			self.incrementFor1Second = 0

		for bullet in self.list_bullets:
			bullet.update()
			if not self.display.get_rect().colliderect(bullet.rect):
				del(self.list_bullets[self.list_bullets.index(bullet)])

			else:
				self.display.blit(bullet.image, (bullet.rect.x, bullet.rect.y))

		self.display.blit(self.currentImage, (self.rect.x, self.rect.y))

class X11(SpaceShip):
	def __init__(self, display, x, y, direction=True, frequency=20):
		image = "./pictures/spaceShip.png"
		self.life = 100
		self.speed = 10
		self.name = "X11"
		SpaceShip.__init__(self, display, x, y, image, direction, frequency)





class Player():
	def __init__(self, name, spacecraft):
		self.name = name
		self.spacecraft = spacecraft
		self.font = pygame.font.SysFont(None, 25)

	def display_name(self):
		self.renderedName = self.font.render(self.name, True, (255,255,255))
		self.rectRenderedName = self.renderedName.get_rect()
		self.rectRenderedName.top = self.spacecraft.rect.bottom
		self.rectRenderedName.midtop = self.spacecraft.rect.midbottom
		self.spacecraft.display.blit(self.renderedName, self.rectRenderedName)


	def move(self, posx, posy):
		"""
		The move method to let the player move

		:param posx, posy:
		:return:
		"""
		self.spacecraft.widthDisplay, self.spacecraft.heightDisplay = pygame.display.get_surface().get_size()
		if posy == 1 and self.spacecraft.rect.y <= self.spacecraft.heightDisplay-self.spacecraft.height:
			self.spacecraft.rect.y += self.spacecraft.speed
		elif posy == -1 and self.spacecraft.rect.y > 0:
			self.spacecraft.rect.y -= self.spacecraft.speed
		elif posx == 1 and self.spacecraft.rect.x <= (self.spacecraft.widthDisplay-self.spacecraft.width)//2:
			self.spacecraft.rect.x += self.spacecraft.speed
		elif posx == -1 and self.spacecraft.rect.x > 0 :
			self.spacecraft.rect.x -= self.spacecraft.speed




class Enemy():
	def __init__(self, name, spacecraft):
		self.name = name
		self.spacecraft = spacecraft

	def move(self):
		"""
		The move method to let the player move

		:param posx, posy:
		:return:
		"""
		posx = random.choice([1, -1, 0])
		posy = random.choice([1, -1, 0])

		self.spacecraft.widthDisplay, self.spacecraft.heightDisplay = pygame.display.get_surface().get_size()
		if posy == 1 and self.spacecraft.rect.y <= self.spacecraft.heightDisplay-self.spacecraft.height:
			self.spacecraft.rect.y += self.spacecraft.speed
		elif posy == -1 and self.spacecraft.rect.y > 0:
			self.spacecraft.rect.y -= self.spacecraft.speed
		elif posx == 1 and self.spacecraft.rect.x >= (self.spacecraft.widthDisplay-self.spacecraft.width)//2:
			self.spacecraft.rect.x += self.spacecraft.speed
		elif posx == -1 and self.spacecraft.rect.x > 0 :
			self.spacecraft.rect.x -= self.spacecraft.speed
