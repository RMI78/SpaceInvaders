import math
import pygame
from functions import *



"""class which create buttons
arguments: Coords: tuple, Surface: Surface object, Size: tuple, Text: string, Font: Font object, Image = String
to use, proceed this way:
if event.type == MOUSEBUTTONDOWN and event.button == 1:
	mouse = pygame.mouse.get_pos
	if Button.imageRect.colliderect(mouse)
	"""

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

				self.imageCliked = load_file(Image[:len(Image)-4] + 'Cliked' + Image[-4:])
				self.imageCliked = pygame.transform.scale(self.imageCliked, (Size))
				self.imageRectCliked = self.imageCliked.get_rect()
				self.isImage = True
			except:
				Image=None
				print("failed to load your image button :'(")
		if Image == None :
			#create and blit a basic button if any image is loaded or if the loading of the image fail
			self.isImage = False
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

	def isCliked(self):
		if self.imageRect.collidepoint(pygame.mouse.get_pos()):
			if self.isImage:
				self.image = self.imageCliked
			else:
				self.image2.fill((0, 255, 0))
			return True
		else: return False


	def move(self, coords):
		self.imageRect.move(coords)
		self.fontRect.move(coords)
		self.display()

"""class that create text input,
	to use it, some code need to be implemented into the event loop in
	order to get the keys, proceed this way to get the keys:
	if event.type == pygame.KEYDOWN:
		if playerName.isFocused:
			playerName.update(event.key)
	if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
		if playerName.isCliked():
			pass

	"""
class inputBox():

	def __init__(self, surface, position, size , color, text=""):
		if len(text) != 0:
			self.text = text + ": "
		self.isFocused = False
		self.message = self.text
		self.surf = surface
		self.colorBox = color
		self.Font = pygame.font.Font(None,round(size[1]*0.6))
		self.frame = pygame.Rect(position, size)
		self.input = pygame.Rect(tuple(map(operator.add, position, percentPix((1,1)))), tuple(map(operator.sub, size, percentPix((0.5,0.5)))))
		self.input.center = self.frame.center
		pygame.draw.rect(self.surf, reverseColor(self.colorBox), self.frame)
		pygame.draw.rect(self.surf, self.colorBox, self.input)
		self.inputFont = self.Font.render(self.message, True, (255,255,255))
		self.inputFontRect = self.inputFont.get_rect()
		self.inputFontRect.center = self.input.center
		self.surf.blit(self.inputFont, self.inputFontRect)


	def update(self, key):
		if key == pygame.K_BACKSPACE and len(self.message) > len(self.text):
			self.message = self.message[0:-1]
		elif key == pygame.K_RETURN:
			pass
		elif key <= 127 and len(self.message) < 20:
			self.message = self.message + chr(key)
		pygame.draw.rect(self.surf, reverseColor(self.colorBox), self.frame)
		pygame.draw.rect(self.surf, self.colorBox, self.input)
		self.inputFont = self.Font.render(self.message, True, (255,255,255))
		self.input.center = self.frame.center
		self.inputFontRect = self.inputFont.get_rect()
		self.inputFontRect.center = self.input.center
		self.surf.blit(self.inputFont, self.inputFontRect)

	def isCliked(self):
		if self.frame.collidepoint(pygame.mouse.get_pos()):
			if self.isFocused:
				self.isFocused = False
			else: self.isFocused = True

	def get_text(self):
		return self.message[len(self.text):]
