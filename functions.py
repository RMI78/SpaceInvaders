import pygame
import os
import operator
import math

#function in order to know what is and how load the file taken in parameter
def load_file(file):
	if file[-4::] in (".png", ".jpg", ".bmp", ".gif"):
		try:
			image = pygame.image.load(file).convert_alpha()
		except pygame.error as message:
				print("Can't load image:", file)
				raise SystemExit(message)
		return image

	elif file[-4::] in (".mp3", ".wav", ".flac"):
		class NoneSound:
			def play(self): pass
		if not pygame.mixer:
			return NoneSound()
		try:
			sound = pygame.mixer.Sound(file)
		except pygame.error as message:
				print("Can't load sound: ", file)
				raise SystemExit(message)
		return sound

	else:
		print("Your file is not supported.")
		return False

#get the pixels coords in function of the screen resolution through a percentage tuple parameter
def percentPix(percent):
	wRes, hRes = pygame.display.get_surface().get_size()
	if percent[0] > 0 and percent[0] <= 100:
		if percent[1] > 0 and percent[1] <= 100:
			return (int(round((percent[0]*wRes)/100)), int(round((percent[1]*hRes)/100)))
	else : print("wrong percentage using precentPix function")

#get the angle beetween the mouse and a rect object in degrees
def mouseAngle(objrect):
	mouseX, mouseY = pygame.mouse.get_pos()
	distanceY = mouseY - objrect.rect.y
	distanceX = mouseX - objrect.rect.x
	if distanceX != 0 or distanceY != 0:
		return -1*(math.degrees(math.atan(distanceY/distanceX)))
	else: return 0

#get the angle beetween 2 surfaces in degrees
def surfAngle(surf1, surf2):
	DistanceX = surf1.rect.centerx - surf2.rect.centerx
	DistanceY = surf1.rect.centery - surf2.rect.centery
	if DistanceX != 0 or DistanceY != 0:
		return -1*(math.degrees(math.atan(DistanceY/DistanceX)))
	else: return 0


def reverseColor(color):
	middleColor = (127, 127, 127)
	red = int(math.sqrt(pow((color[0] - middleColor[0]), 2)))
	green = int(math.sqrt(pow((color[1] - middleColor[1]), 2)))
	blue = int(math.sqrt(pow((color[2] - middleColor[2]), 2)))
	if color[0] >= 127:
		r = 127 - red
	elif color[0] < 127:
		r = 127 + red
	if color[1] >= 127:
		g = 127 - green
	elif color[1] < 127:
		g = 127 + green
	if color[2] >= 127:
		b = 127 -blue
	elif color[2] < 127:
		b = 127 + blue
	colors = (r, g, b)
	return colors
