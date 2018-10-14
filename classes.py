import pygame
from functions import *
import math
import random


class Aim:
	def __init__(self, display):
		self.display = display
		self.image = pygame.transform.scale(load_file("./pictures/aim.png"), percentPix((2,2)))

	#the update method for the position
	def focusAim(self):
		self.display.blit(self.image, pygame.mouse.get_pos())

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

