import pygame
from functions import *
import math

class Aim(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(load_file("aim.png"), (percentPix(2, True), percentPix(2, False)))
		self.rect = self.image.get_rect()
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()

	def focusAim(self):
		Xmouse, Ymouse = pygame.mouse.get_pos()
		self.rect.x = Xmouse
		self.rect.y = Ymouse



class Bullet(pygame.sprite.Sprite):
	def __init__(self, element, power):
		super().__init__()
		self.image = pygame.Surface((percentPix(2, True), percentPix(2, False)))
		self.rect = self.image.get_rect()
		self.rect.y = element.rect.y
		self.rect.x = element.rect.x
		self.mouseX, self.mouseY = pygame.mouse.get_pos()
		self.distanceY = self.mouseY - self.rect.y
		self.distanceX = self.mouseX - self.rect.x
		self.posXElement = element.rect.x
		self.posYElement = element.rect.y

	def update(self, element):
		self.rect.x = self.rect.x + 10
		if 0 not in (self.distanceX, self.distanceY, self.posXElement, self.rect.x, self.posYElement, self.rect.y):
			self.rect.y = self.posYElement - ((self.distanceY / self.distanceX ) *  (self.posXElement - self.rect.x ))



class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(load_file("SpaceShip.png"), (percentPix(8, True), percentPix(10, False)))
		self.rect = self.image.get_rect()
		self.width, self.height = pygame.display.get_surface().get_size()
		self.alive = True
		self.speed = 10

	def move(self, posx, posy):
		if posy == 1 and self.rect.y <= self.height - 400:
			self.rect.y += self.speed
		if posy == -1 and self.rect.y > 0:
			self.rect.y -= self.speed
		if posx == 1 and self.rect.x <= (self.width/2)-150:
			self.rect.x += self.speed
		if posx == -1 and self.rect.x > 0 :
			self.rect.x -= self.speed



#class enemy(pygame.sprite.Sprite):
