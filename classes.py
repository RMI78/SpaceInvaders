import pygame
from functions import *
import math
import random
from spaceship import *
from widgets import *

class Aim:
	def __init__(self, display):
		self.display = display
		self.image = pygame.transform.scale(load_file("./pictures/aim.png"), percentPix((2,2)))

	#the update method for the position
	def focusAim(self):
		self.display.blit(self.image, pygame.mouse.get_pos())




class Manager():
	def __init__(self, confFile):
		#opening and reading or creating the conf file
		self.confFile = confFile
		self.loadSetting()

		#load the screen
		self.displayInfos = pygame.display.Info()
		self.displaySize = (self.displayInfos.current_w, self.displayInfos.current_h)
		if self.screen == "windowed\n":
			self.window = pygame.display.set_mode(self.displaySize, pygame.RESIZABLE)
		if self.screen == "fullscreen\n":
			self.window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

		pygame.display.set_caption("Space Invaders")
		self.Font = pygame.font.SysFont("monospace", 35, True)

		self.pauseSurf = pygame.Surface(pygame.display.get_surface().get_size())
		self.pauseSurf.fill(pygame.Color("black"))
		self.pauseSurf.set_alpha(200)
		self.loadPictures()

		pygame.display.set_icon(self.icon)
		self.clock = pygame.time.Clock()

		#set the flags
		self.LEAVE = 0
		self.SOLO = 1
		self.MENU = 2
		self.SETTINGS = 3
		self.MULTI = 4


	def menu(self):
		#things that need to be ignited once
		MenuFont = self.Font.render("Space Invaders", True, [255,255,255])

		pygame.mouse.set_visible(True)
		self.menuPlaySoloButton.display()
		self.menuPlayMultiButton.display()
		self.menuSettingButton.display()
		self.menuLeaveButton.display()

		while True:
			#in this loop place things that need to be looped in the menu
			self.clock.tick(60)
			pygame.mouse.set_visible(True)
			self.window.blit(self.MenuSurf, (0,0))
			self.window.blit(MenuFont, percentPix((42, 15)))
			self.menuPlaySoloButton.display()
			self.menuPlayMultiButton.display()
			self.menuSettingButton.display()
			self.menuLeaveButton.display()
			for eventMenu in pygame.event.get():
				if eventMenu.type == pygame.QUIT:
					return self.LEAVE
				if eventMenu.type == pygame.MOUSEBUTTONDOWN and eventMenu.button == 1:
					if self.menuPlaySoloButton.isCliked():
						return self.SOLO
					if self.menuSettingButton.isCliked():
						return self.SETTINGS
					if self.menuLeaveButton.isCliked():
						return self.LEAVE
				if eventMenu.type == pygame.QUIT:
					return self.LEAVE
			pygame.display.flip()


	def solo(self):
		stateGame = True #if True, mode is on play, if not, mode is on pause
		self.loadSetting()
		#things that need to be ignited once for the play part
		aim = Aim(self.window)
		player = Player(self.playername, X11(self.window, 10, 10))
		enemy = Enemy("Simple ennemy", X11(self.window, 1600, 500, False))
		enemy2 = Enemy("a second enemy",X11(self.window, 1600, 600, False))

		#things that need to be ignited once for the solo pause part
		PauseFont = self.Font.render("PAUSE", True,[255, 255, 255])

		pygame.mouse.set_visible(False)

		#in this loop place things that need to be looped in the game and the pause
		while True:
			if stateGame:
				self.clock.tick(60)
				self.window.blit(self.gameSurf, (0,0))
				keypress = pygame.key.get_pressed()
				if keypress[pygame.K_z]:
					player.move(0, -1)
				if keypress[pygame.K_s]:
					player.move(0, 1)
				if keypress[pygame.K_d]:
					player.move(1, 0)
				if keypress[pygame.K_q]:
					player.move(-1, 0)
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						return self.LEAVE
					if event.type == pygame.MOUSEBUTTONDOWN:
						player.spacecraft.shoot()
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							stateGame = False

				enemy.move()
				enemy2.move()
				enemy.spacecraft.shoot(player)
				enemy2.spacecraft.shoot(player)
				enemy.spacecraft.update()
				enemy2.spacecraft.update()
				player.spacecraft.update()
				player.display_name()
				aim.focusAim()

			if not stateGame:
				pygame.mouse.set_visible(True)
				self.window.blit(self.pauseSurf, (0,0))
				self.window.blit(PauseFont, percentPix((47,20)))
				self.backToGameButton.display()
				self.backToMenuButton.display()
				self.pauseSettingButton.display()
				self.pauseLeaveButton.display()
				for eventPause in pygame.event.get():
					if eventPause.type == pygame.QUIT:
						stateGame = True
					if eventPause.type == pygame.MOUSEBUTTONDOWN and eventPause.button == 1:
						if self.backToGameButton.isCliked():
							pygame.mouse.set_visible(False)
							stateGame = True
						if self.backToMenuButton.isCliked():
							return self.MENU
						if self.pauseSettingButton.isCliked():
							self.settings()
							self.loadSetting()
							player = Player(self.playername, X11(self.window, player.spacecraft.rect.x, player.spacecraft.rect.y))
						if self.pauseLeaveButton.isCliked():
							return self.LEAVE
					if eventPause.type == pygame.KEYDOWN:
						if eventPause.key == pygame.K_ESCAPE:
							stateGame = True
					if eventPause.type == pygame.QUIT:
						return LEAVE
				pygame.mouse.set_visible(False)

			pygame.display.flip()

	def mutli(self):
			#place here things that need to be ignited once

			#in this loop place things that need to be looped in the multi
			pass

	def settings(self):
				#place here things that need to be ignited once
				SettingFont = self.Font.render("Settings", True, [255, 255, 255])
				playerName = inputBox(self.SettingSurf, percentPix((35, 20)), percentPix((20, 8)), [0,0,0], "Name")
				self.backButton = Button(percentPix((5, 90)), self.SettingSurf, percentPix((5.50,6.00)), "back", self.Font)
				#in this loop place things that need to be looped in the menu
				while True:
					self.clock.tick(60)
					pygame.mouse.set_visible(True)
					self.window.blit(self.SettingSurf, (0,0))
					self.window.blit(SettingFont, percentPix((47, 15)))
					self.fullscreenButton.display()
					self.windowedButton.display()
					self.saveButton.display()
					self.backButton.display()
					for eventSetting in pygame.event.get():
						if eventSetting.type == pygame.QUIT:
							return self.LEAVE
						if eventSetting.type == pygame.KEYDOWN:
							if playerName.isFocused:
								playerName.update(eventSetting.key)
						if eventSetting.type == pygame.MOUSEBUTTONDOWN and eventSetting.button == 1:
							if playerName.isCliked():
								pass
							if self.fullscreenButton.isCliked():
								self.screen = "fullscreen\n"
							if self.windowedButton.isCliked():
								self.screen = "windowed\n"
							if self.saveButton.isCliked():
								self.playername = playerName.get_text()
								self.writeConfig()
							if self.backButton.isCliked():
								return self.MENU
					pygame.display.flip()

	def writeConfig(self):
		"""
		The close method to write the current
		config and close the config file

		:param:
		:return:
		"""
		self.config = open(self.confFile, 'w')
		self.config.write(self.screen + self.playername)
		self.config.close()

	def loadSetting(self):
		try:
			config = open(self.confFile, 'r')
			configList = config.readlines()
			self.screen = configList[0]
			self.playername = configList[1]

		except:
			self.screen = "windowed\n"
			self.playername = "player"
			self.config = open(self.confFile, 'w')
			self.config.write(self.screen  + self.playername)

	def loadPictures(self):
		self.icon = pygame.image.load("./pictures/spaceInvaders_icon.jpg")
		self.gameSurf = pygame.transform.scale(load_file("./pictures/background.png"), self.displaySize)
		self.MenuSurf = pygame.transform.scale(load_file("./pictures/background.png"), self.displaySize)
		self.SettingSurf = pygame.transform.scale(load_file("./pictures/background.png"), self.displaySize)
		self.menuPlaySoloButton = Button(percentPix((50, 30)), self.MenuSurf, percentPix((20,15)), "Solo", self.Font, "./pictures/graySquareButton.png")
		self.menuPlayMultiButton = Button(percentPix((50,47)), self.MenuSurf, percentPix((20,15)), "Multi", self.Font, "./pictures/graySquareButton.png")
		self.menuSettingButton =  Button(percentPix((50,64)), self.MenuSurf, percentPix((20,15)), "Settings", self.Font, "./pictures/graySquareButton.png")
		self.menuLeaveButton = Button(percentPix((50,81)), self.MenuSurf, percentPix((20,15)),"Leave the Game", self.Font, "./pictures/graySquareButton.png")
		self.backToGameButton = Button(percentPix((50,35)), self.pauseSurf, percentPix((20,15)), "Back to game", self.Font, "./pictures/graySquareButton.png")
		self.backToMenuButton = Button(percentPix((50, 50)), self.pauseSurf, percentPix((20, 15)), "Back to menu", self.Font, "./pictures/graySquareButton.png")
		self.pauseSettingButton = Button(percentPix((50,65)), self.pauseSurf, percentPix((20,15)),"Settings", self.Font, "./pictures/graySquareButton.png")
		self.pauseLeaveButton = Button(percentPix((50,80)), self.pauseSurf, percentPix((20,15)), "Leave the Game", self.Font, "./pictures/graySquareButton.png")
		self.fullscreenButton = Button(percentPix((65, 50)), self.SettingSurf, percentPix((20, 15)), "Fullscreen",self.Font, "./pictures/graySquareButton.png")
		self.windowedButton = Button(percentPix((35, 50)), self.SettingSurf, percentPix((20, 15)), "Windowed",self.Font, "./pictures/graySquareButton.png")
		self.saveButton = Button(percentPix((65, 25)), self.SettingSurf, percentPix((10, 15)), "Save",self.Font, "./pictures/graySquareButton.png")
