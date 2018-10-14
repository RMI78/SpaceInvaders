import pygame
from functions import *
import random

class Bullet:
    def __init__(self, x, y, height, speed=20, type=True, xTarget=None, yTarget=None):
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

    def update(self):
        self.rect.x +=self.speed
        self.rect.y = self.coof * self.rect.x +self.b

class SpaceShip:
    def __init__(self, display, x, y, image="./pictures/spaceShip.png", speed=10):
        self.display = display
        self.image = pygame.transform.scale(load_file(image), percentPix((8,10)))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (x, y)
        self.height, self.width= (self.rect[-1], self.rect[-2])
        self.widthDisplay, self.heightDisplay = pygame.display.get_surface().get_size()
        self.bullet = Bullet
        self.list_bullets = []
        self.alive = True
        self.speed = speed


class Player(SpaceShip):

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
		self.list_bullets.append(self.bullet(self.rect.x, self.rect.y, self.height))

	def update(self):
		for bullet in self.list_bullets:
			bullet.update()
			if not self.display.get_rect().colliderect(bullet.rect):
				del(self.list_bullets[self.list_bullets.index(bullet)])

			else:
				self.display.blit(bullet.image, (bullet.rect.x, bullet.rect.y))

		self.display.blit(self.image, (self.rect.x, self.rect.y))



class Enemy(SpaceShip):

	def move(self):
		"""
		The move method to let the player move

		:param posx, posy:
		:return:
		"""
		posx = random.choice([1, -1, 0])
		posy = random.choice([1, -1, 0])

		self.widthDisplay, self.heightDisplay = pygame.display.get_surface().get_size()
		if posy == 1 and self.rect.y <= self.heightDisplay-self.height:
			self.rect.y += self.speed
		elif posy == -1 and self.rect.y > 0:
			self.rect.y -= self.speed
		elif posx == 1 and self.rect.x >= (self.widthDisplay-self.width)//2:
			self.rect.x += self.speed
		elif posx == -1 and self.rect.x > 0 :
			self.rect.x -= self.speed

	def shoot(self, player):
		if random.choice([True, False]):
			self.list_bullets.append(self.bullet(self.rect.x, self.rect.y, self.height, 10, False, player.rect.x, player.rect.y+player.height/2))

	def update(self):
		for bullet in self.list_bullets:
			bullet.update()
			if not self.display.get_rect().colliderect(bullet.rect):
				del(self.list_bullets[self.list_bullets.index(bullet)])

			else:
				self.display.blit(bullet.image, (bullet.rect.x, bullet.rect.y))

		self.display.blit(self.image, (self.rect.x, self.rect.y))
