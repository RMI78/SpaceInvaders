import pygame
from functions import *
import math

class Aim(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(load_file("./images/aim.png"), (percentPix(2, True), percentPix(2, False)))
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
		self.image = pygame.transform.scale(load_file("./images/spaceShip.png"), (percentPix(8, True), percentPix(10, False)))
		self.rect = self.image.get_rect()
		self.width, self.height = self.rect[-2::]
		self.widthDisplay, self.heightDisplay = pygame.display.get_surface().get_size()
		self.alive = True
		self.speed = 10

	def move(self, posx, posy):
		self.widthDisplay, self.heightDisplay = pygame.display.get_surface().get_size()
		print(self.heightDisplay, self.height)
		print(self.rect.y)
		if posy == 1 and self.rect.y <= self.heightDisplay-self.height:
			self.rect.y += self.speed
		elif posy == -1 and self.rect.y > 0:
			self.rect.y -= self.speed
		elif posx == 1 and self.rect.x <= (self.widthDisplay-self.width)//2:
			self.rect.x += self.speed
		elif posx == -1 and self.rect.x > 0 :
			self.rect.x -= self.speed



#class enemy(pygame.sprite.Sprite):
