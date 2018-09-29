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
		self.image = pygame.transform.scale(load_file("./images/bullet.jpg"), (percentPix(2, True), percentPix(2, False)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.xMouse, self.yMouse = pygame.mouse.get_pos()
		self.coof = (self.yMouse-self.rect.y)//(self.xMouse-self.rect.x)

	def update(self):
		self.rect.x +=10
		self.rect.y =  self.coof * self.rect.x


class Player:
	def __init__(self, display):
		self.display = display
		self.image = pygame.transform.scale(load_file("./images/spaceShip.png"), (percentPix(8, True), percentPix(10, False)))
		self.rect = self.image.get_rect()
		self.width, self.height = self.rect[-2::]
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
			self.display.blit(bullet.image, (bullet.rect.x, bullet.rect.y))

		self.display.blit(self.image, (self.rect.x, self.rect.y))



#class enemy(pygame.sprite.Sprite):
