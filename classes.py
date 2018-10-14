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
