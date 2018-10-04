import pygame
import os
import operator

#function in order to know what is and how load the file taken in parameter
def load_file(file):
	if file[-4::] in (".png", ".jpg", ".bmp", ".gif"):
		try:
			image = pygame.image.load(file).convert_alpha()
		except pygame.error as message:
				print("Can't load image:", file)
				raise SystemExit(message)
		return image

	elif file[-4::] in (".mp3", ".wav"):
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

#get the number of pixels in function of the screen resolution through a percentage parameter
#the second parameter: True for the width and False for the Height
def percentPix(percent, widthOrHeight):
	wRes, hRes = pygame.display.get_surface().get_size()
	if percent > 0 and percent <= 100:
		if widthOrHeight == True :
			return round((percent*wRes)/100)
		if widthOrHeight == False :
			return round((percent*hRes)/100)
	else : print("wrong percentage using precentPix function")

#get the angle beetween the mouse and a sprite in degrees
def mouseAngle(objrect):
	mouseX, mouseY = pygame.mouse.get_pos()
	distanceY = mouseY - objrect.rect.y
	distanceX = mouseX - objrect.rect.x
	if distanceX != 0 or distanceY != 0:
		finalAngle = 45 - math.degrees(math.atan(distanceX / distanceY))
		return -1*finalAngle

#functions which create buttons
#to use, proceed this way:
#if event.type == MOUSEBUTTONDOWN and event.button == 1:
#	mouse = pygame.mouse.get_pos
#	if Image[1].colliderect(mouse)
def Buttonify(image, coords, surface, text='', font=None):
	#load, scale, place and render the button
	image = pygame.transform.scale(image, (percentPix(20, True), percentPix(15, False)))
	imagerect = image.get_rect()
	imagerect.center = coords
	surface.blit(image, imagerect)

	#load, place and render the string
	if font:
		buttonStr = font.render(text, True, [0,0,0])
		fontrect = buttonStr.get_rect()
		fontrect.center = imagerect.center
		surface.blit(buttonStr,fontrect)


	return (image, imagerect)
