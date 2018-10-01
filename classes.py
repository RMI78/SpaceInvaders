import pygame
from Functions import *
import math

#classe which create buttons
#to use, proceed this way:
#if event.type == MOUSEBUTTONDOWN and event.button == 1:
#	mouse = pygame.mouse.get_pos
#	if Image[1].colliderect(mouse)
def Buttonify(Picture, coords, surface):
	image = load_file(Picture)
	image = pygame.transform.scale(image, (percentPix(20, True), percentPix(15, False)))
	imagerect = image.get_rect()
	imagerect.topright = coords
	surface.blit(image, imagerect)
	return (image, imagerect)

#classe which represent the aim
class Aim(pygame.sprite.Sprite):
	#the init method
	def __init__(self):
		super().__init__()
		picAim = pygame.transform.scale(load_file("pictures/aim.png"), (percentPix(2, True), percentPix(2, False)))
		self.image = picAim
		self.rect = self.image.get_rect()
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
	#the update method for the position
	def focusAim(self):
		Xmouse, Ymouse = pygame.mouse.get_pos()
		self.rect.x = Xmouse
		self.rect.y = Ymouse


#class which represent the bullets
class Bullet(pygame.sprite.Sprite):
	#the init method
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

	#the update method for the position
	def update(self, element):
		self.rect.x = self.rect.x + 10
		if self.distanceX != 0 or self.distanceY != 0 or self.posXElement != 0 or self.rect.x != 0 or self.posYElement != 0 or self.rect.y != 0:
			self.rect.y = self.posYElement - ((self.distanceY / self.distanceX ) *  (self.posXElement - self.rect.x ))



#class which represent the player
class Player(pygame.sprite.Sprite):
	#the init method for the player
	def __init__(self):
		super().__init__()
		avatar = pygame.transform.scale(load_file("pictures/SpaceShip.png"), (percentPix(8, True), percentPix(10, False)))
		self.image = avatar
		self.rect = self.image.get_rect()
		self.width, self.height = pygame.display.get_surface().get_size()
		self.alive = True
		self.speed = 10

	#the move method to let the player move
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
