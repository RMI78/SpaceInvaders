import pygame
from functions import *
import math

class Aim:
	def __init__(self, display):
		self.display = display
		self.image = pygame.transform.scale(load_file("./images/aim.png"), (percentPix(2, True), percentPix(2, False)))

	def focusAim(self):
		self.display.blit(self.image, pygame.mouse.get_pos())



class Bullet:
	def __init__(self, display, x, y):
		self.image = pygame.transform.scale(load_file("./images/bullet.png"), (percentPix(2, True), percentPix(2, False)))
		self.x = x
		self.y = y
		self.b = y
		self.xMouse, self.yMouse = pygame.mouse.get_pos()
		self.coof = (self.yMouse-self.y)/(self.xMouse-self.x)
		if self.coof > 0.1:
			self.coof = 0.1

		elif self.coof < -0.1:
			self.coof = -0.1
		print(self.coof)



	def update(self):
		self.x +=10
		self.y = self.coof * self.x +self.b


class Player:
	def __init__(self, display):
		self.display = display
		self.image = pygame.transform.scale(load_file("./images/spaceShip.png"), (percentPix(8, True), percentPix(10, False)))
		self.rect = self.image.get_rect()
		self.height = self.rect[-1]
		self.width = self.rect[-2]
		self.widthDisplay, self.heightDisplay = pygame.display.get_surface().get_size()
		self.bullet = Bullet
		self.list_bullets = []
		self.alive = True
		self.speed = 10

	def move(self, posx, posy):
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
		self.list_bullets.append(self.bullet(self.display, self.rect.x, self.rect.y))

	def update(self):
		for bullet in self.list_bullets:
			bullet.update()
			self.display.blit(bullet.image, (bullet.x, bullet.y))

		self.display.blit(self.image, (self.rect.x, self.rect.y-self.height/2))



#class enemy(pygame.sprite.Sprite):
