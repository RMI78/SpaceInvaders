import pygame
from functions import *
from widgets import *
import math
import random



class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, height, angle=0,  speed=20, type=True, xTarget=None, yTarget=None, direction=True):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(load_file("./pictures/bullet.png"), percentPix((2,2)))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = (x, y)
		self.speed = speed
		if type:
			self.xTarget, self.yTarget = pygame.mouse.get_pos()
		else:
			self.xTarget, self.yTarget = (xTarget, yTarget)

		if not direction:
			self.speed = -self.speed

		self.coof = ((self.yTarget-height/2)-self.rect.y)/(self.xTarget-self.rect.x)
		self.b = self.rect.y - self.coof*self.rect.x+height/2
		self.angle = angle
		self.image = pygame.transform.rotate(self.image, self.angle)
		self.mask = pygame.mask.from_surface(self.image)

	def update(self):
		self.rect.x +=self.speed
		self.rect.y = self.coof * self.rect.x +self.b

class SpaceShip(pygame.sprite.Sprite):
	def __init__(self, display, x, y, image, direction=True, frequency=20):
		pygame.sprite.Sprite.__init__(self)
		self.display = display
		self.direction = direction
		self.strForImage2 = image[:len(image)-4] + '2' + image[-4:]
		self.strForImage3 = image[:len(image)-4] + '3' + image[-4:]
		self.image = pygame.transform.scale(load_file(image), percentPix((9,10)))
		self.image2 = pygame.transform.scale(load_file(self.strForImage2), percentPix((9,10)))
		self.image3 = pygame.transform.scale(load_file(self.strForImage3), percentPix((9,10)))
		if not direction:
			self.image = pygame.transform.flip(self.image, True, False)
			self.image2 = pygame.transform.flip(self.image2, True, False)
			self.image3 = pygame.transform.flip(self.image3, True, False)
		self.currentImage = self.image
		self.mask = pygame.mask.from_surface(self.currentImage)
		self.rect = self.currentImage.get_rect()
		self.rect.x, self.rect.y = (x, y)
		self.height, self.width= (self.rect[-1], self.rect[-2])
		self.widthDisplay, self.heightDisplay = pygame.display.get_surface().get_size()
		self.bullet = Bullet
		self.list_bullets = pygame.sprite.Group()
		self.alive = True
		self.incrementFor1Second = 0
		self.frequency = frequency
		self.lastShots = self.frequency

	def shoot(self, player=None, x=None, y=None, angle=None):
		if self.lastShots > 0:
			if player:
				if random.randint(0,800)<50:
					self.list_bullets.add(self.bullet(self.rect.x, self.rect.y, self.height, surfAngle(self, player.spacecraft), 10, False, player.spacecraft.rect.x, player.spacecraft.rect.y+player.spacecraft.height/2, False))

			if x and  y is not None:
				self.list_bullets.add(self.bullet(self.rect.x, self.rect.y, self.height, angle, 20, False, x, y, self.direction))

			elif not player:
				self.list_bullets.add(self.bullet(self.rect.x, self.rect.y, self.height, mouseAngle(self), 20, True, None, None, self.direction))
			self.lastShots = self.lastShots-1
		else: pass


	def update(self, targets=None):
		self.incrementFor1Second += 1
		if self.incrementFor1Second == 1:
			self.currentImage = self.image
		elif self.incrementFor1Second == 30:
			self.currentImage = self.image2
		elif self.incrementFor1Second == 60:
			self.currentImage = self.image3
			self.lastShots = self.frequency
			self.incrementFor1Second = 0

		self.mask = pygame.mask.from_surface(self.currentImage)


		self.list_bullets.update()

		for bullet in self.list_bullets.sprites():
			if not self.display.get_rect().colliderect(bullet.rect):
				self.list_bullets.remove(bullet)
			else:
				self.display.blit(bullet.image, (bullet.rect.x, bullet.rect.y))
		if targets:
			for target in targets.sprites():
				if pygame.sprite.spritecollide(target, self.list_bullets, True, pygame.sprite.collide_mask):
					target.life = target.life - 1

		self.display.blit(self.currentImage, (self.rect.x, self.rect.y))

class X11(SpaceShip):
	def __init__(self, display, x, y, direction=True, frequency=20):
		image = "./pictures/spaceShip.png"
		self.life = 100
		self.speed = 10
		self.name = "X11"
		SpaceShip.__init__(self, display, x, y, image, direction, frequency)





class Player:
	def __init__(self, name, spacecraft):
		self.name = name
		self.spacecraft = spacecraft
		self.font = pygame.font.SysFont(None, 25)
		self.lifeBar = statuBar(spacecraft.life, spacecraft.display, (spacecraft.rect.bottomleft), (spacecraft.rect.width, percentPix((5,5))[1]), [255, 255, 0], "life")
		self.currentLife  = self.spacecraft.life
		self.lifeBarDisplayed = False
		self.nameDisplayed = False

	def display_name(self):
		self.nameDisplayed = True
		self.renderedName = self.font.render(self.name, True, (255,255,255))
		self.rectRenderedName = self.renderedName.get_rect()
		self.rectRenderedName.top = self.spacecraft.rect.bottom
		self.rectRenderedName.midtop = self.spacecraft.rect.midbottom
		self.spacecraft.display.blit(self.renderedName, self.rectRenderedName)

	def display_life(self):
		self.lifeBarDisplayed = True
		if not self.nameDisplayed:
			self.lifeBar.rectMainSurf.midtop = self.spacecraft.rect.midbottom
		else:
			self.lifeBar.rectMainSurf.midtop = self.rectRenderedName.midbottom
		self.lifeBar.display()

	def update(self):
		if self.nameDisplayed:
			self.display_name()
		if self.lifeBarDisplayed:
			self.display_life()
		self.lifeBar.update(self.spacecraft.life-self.currentLife)
		self.currentLife = self.spacecraft.life


	def isDead(self):
		if self.spacecraft.life == 0:
			return True
		else: return False


	def move(self, posx, posy):
		"""
		The move method to let the player move

		:param posx, posy:
		:return:
		"""
		display = pygame.display.get_surface().get_rect()
		if self.spacecraft.direction:
			display.x, display.y, display.w, display.h = (display.x+self.spacecraft.width, display.y+self.spacecraft.height, (display.w/2)-self.spacecraft.width*2, display.h-self.spacecraft.height*2)

		else:
			display.x, display.y, display.w, display.h = (display.x+(display.w/2)+self.spacecraft.width, display.y+self.spacecraft.height, display.w-(display.x+(display.w/2)+self.spacecraft.width*2), display.h-self.spacecraft.height*2)

		self.spacecraft.rect.y += self.spacecraft.speed*posy
		self.spacecraft.rect.x += self.spacecraft.speed*posx
		if not display.colliderect(self.spacecraft.rect):
			self.spacecraft.rect.y -= self.spacecraft.speed*posy
			self.spacecraft.rect.x -= self.spacecraft.speed*posx

	def multi(self, shoot):
		xMouse, yMouse = pygame.mouse.get_pos()
		list = "{}, {}, {}, {}, {}, {}".format(self.spacecraft.rect.x,self.spacecraft.rect.y, shoot, xMouse, yMouse, mouseAngle(self.spacecraft)).encode()
		return list


class Enemy(Player):

	def move(self):
		"""
		The move method to let the player move

		:param posx, posy:
		:return:
		"""
		posx = random.choice([0, 1, -1])
		posy = random.choice([0, 1, -1])

		display = pygame.display.get_surface().get_rect()
		display.x, display.y, display.w, display.h = (display.x+(display.w/2)+self.spacecraft.width, display.y+self.spacecraft.height, display.w-(display.x+(display.w/2)+self.spacecraft.width*2), display.h-self.spacecraft.height*2)

		self.spacecraft.rect.y += self.spacecraft.speed*posy
		self.spacecraft.rect.x += self.spacecraft.speed*posx
		if not display.colliderect(self.spacecraft.rect):
			self.spacecraft.rect.y -= self.spacecraft.speed*posy
			self.spacecraft.rect.x -= self.spacecraft.speed*posx


	def __del__(self):
		self.spacecraft.kill()
		self.lifeBarDisplayed = False
		self.nameDisplayed = False
		self = None
