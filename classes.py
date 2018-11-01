import pygame
from functions import *
import math
import random
from spaceship import *
from widgets import *
import socket
import pickle
from networking import Networking

class Aim:
	def __init__(self, display):
		self.display = display
		self.image = pygame.transform.scale(load_file("./pictures/aim.png"), percentPix((2,2)))

	#the update method for the position
	def focusAim(self):
		self.display.blit(self.image, pygame.mouse.get_pos())




class Manager():
	def __init__(self, confFile):
		"""
		The  __init__  method to load everything
		that needs to be loaded such as Settings,
		screen, etc...

		:param confFile:
		:return:
		"""
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
		"""
		The menu method to print the menu
		on the screen to welcome the player

		:param:
		:return:
		"""
		#things that need to be ignited once
		MenuFont = self.Font.render("Space Invaders", True, [255,255,255])
		self.button_list = self.loadButtons(self.MENU)
		pygame.mouse.set_visible(True)

		while True:
			#in this loop place things that need to be looped in the menu
			self.clock.tick(60)
			pygame.mouse.set_visible(True)
			self.window.blit(self.MenuSurf, (0,0))
			self.window.blit(MenuFont, percentPix((42, 15)))
			for buttons in self.button_list:
				buttons.display()

			for eventMenu in pygame.event.get():
				if eventMenu.type == pygame.QUIT:
					return self.LEAVE
				if eventMenu.type == pygame.MOUSEBUTTONDOWN and eventMenu.button == 1:
					if self.menuPlaySoloButton.isCliked():
						return self.SOLO
					if self.menuPlayMultiButton.isCliked():
						return self.MULTI
					if self.menuSettingButton.isCliked():
						return self.SETTINGS
					if self.menuLeaveButton.isCliked():
						return self.LEAVE
				if eventMenu.type == pygame.QUIT:
					return self.LEAVE
			pygame.display.flip()


	def solo(self):
		"""
		The solo method ignite and
		print the game for one player
		the game is splitted in 2 parts
		the play and the pause part

		:param:
		:return:
		"""

		#things that need to be  ignited for both pause and play part
		stateGame = 0
		PLAY = 0
		PAUSE = 1
		GAMEOVER = 2
		self.loadSetting()

		#things that need to be ignited once for the play part
		aim = Aim(self.window)
		player = Player(self.playername, X11(self.window, 10, 10))
		enemy = Enemy("Simple ennemy", X11(self.window, 1600, 500, False))
		enemy2 = Enemy("a second enemy",X11(self.window, 1600, 600, False))
		left_team = pygame.sprite.Group()
		right_team = pygame.sprite.Group()
		left_team.add(player.spacecraft)
		right_team.add(enemy.spacecraft, enemy2.spacecraft)
		entityList = [player, enemy, enemy2]
		for entity in entityList:
			entity.display_life()
			entity.display_name()
		pygame.mouse.set_visible(False)


		#things that need to be ignited once for the solo pause part
		PauseFont = self.Font.render("PAUSE", True,[255, 255, 255])
		self.button_list = self.loadButtons(self.SOLO)

		#things that need to be ignited once for the game over part
		GameOverFont = self.Font.render("GAME OVER", True, [255,255,255])


		#in this loop place things that need to be looped in the game and the pause
		while True:
			#the play part
			if stateGame == PLAY:
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
							stateGame = PAUSE

				right_team.update(left_team)
				left_team.update(right_team)
				for entity in entityList:
					entity.update()

				if player.isDead():
					stateGame = GAMEOVER
				if enemy:
					enemy.move()
					enemy.spacecraft.shoot(player)
					if enemy.isDead():
						print("something")
						right_team.remove(enemy)
						entityList.remove(enemy)
						enemy.__del__()
						enemy = None
				if enemy2:
					enemy2.move()
					enemy2.spacecraft.shoot(player)
					if enemy2.isDead():
						print("something2")
						right_team.remove(enemy2)
						entityList.remove(enemy2)
						enemy2.__del__()
						enemy2 = None

				aim.focusAim()

			#the pause part
			if stateGame == PAUSE:
				pygame.mouse.set_visible(True)
				self.window.blit(self.pauseSurf, (0,0))
				self.window.blit(PauseFont, percentPix((47,20)))
				for buttons in self.button_list:
					buttons.display()
				for eventPause in pygame.event.get():
					if eventPause.type == pygame.QUIT:
						stateGame == PLAY
					if eventPause.type == pygame.MOUSEBUTTONDOWN and eventPause.button == 1:
						if self.backToGameButton.isCliked():
							pygame.mouse.set_visible(False)
							stateGame == PLAY
							self.button_list = self.loadButtons(self.SOLO)
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
							pygame.mouse.set_visible(False)
							stateGame == PLAY
							self.button_list = self.loadButtons(self.SOLO)
					if eventPause.type == pygame.QUIT:
						return self.LEAVE

			#the game over part
			if stateGame == GAMEOVER:
				self.window.blit(self.pauseSurf, (0,0))
				self.window.blit(GameOverFont, percentPix((47,20)))
				self.loadButtons(self.SOLO)[1].display()
				pygame.mouse.set_visible(True)
				for eventPause in pygame.event.get():
					if eventPause.type == pygame.KEYDOWN:
						if eventPause.key == pygame.K_ESCAPE:
							return self.MENU
							self.button_list = self.loadButtons(self.SOLO)
					if eventPause.type == pygame.QUIT:
						return self.LEAVE
					if eventPause.type == pygame.MOUSEBUTTONDOWN and eventPause.button == 1:
						if self.backToMenuButton.isCliked():
							return self.MENU



			pygame.display.flip()

	def mutli(self):
		aim = Aim(self.window)
		self.loadSetting()
		self.loadButtons()

		networking = Networking()
		socket = networking.connect()
		r = networking.sync(socket)
		if r.decode() == "True":
			player = Player(self.playername, X11(self.window, 10, 10))
			ennemi = Player(self.playername, X11(self.window, 1600, 600, False))

		else:
			player = Player(self.playername, X11(self.window, 1600, 600, False))
			ennemi = Player(self.playername, X11(self.window, 10, 10))


		pygame.mouse.set_visible(False)

		while True:
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

			_str = networking.send(socket, player.multi())
			_str = _str.decode()
			list_str = _str.split(",")
			list_int = []
			for i in list_str:
				list_int.append(int(i))

			ennemi.spacecraft.rect.x, ennemi.spacecraft.rect.y = (list_int[0], list_int[-1])
			ennemi.spacecraft.update()
			player.spacecraft.update()
			player.display_name()
			aim.focusAim()
			pygame.display.flip()


	def settings(self):
		"""
		The settings method to print
		settings on the screen and let
		the player custom the game

		:param:
		:return:
		"""
		#place here things that need to be ignited once
		SettingFont = self.Font.render("Settings", True, [255, 255, 255])
		playerName = inputBox(self.SettingSurf, percentPix((35, 20)), percentPix((20, 8)), [0,0,0], "Name")
		self.button_list = self.loadButtons(self.SETTINGS)
		#in this loop place things that need to be looped in the settings
		while True:
			self.clock.tick(60)
			pygame.mouse.set_visible(True)
			self.window.blit(self.SettingSurf, (0,0))
			self.window.blit(SettingFont, percentPix((47, 15)))
			for buttons in self.button_list:
				buttons.display()

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
		"""
		The loadSetting method to read
		the configuration file and
		load everything into the game

		:param:
		:return:
		"""
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
		"""
		The loadPictures method to load,
		scale and copy the background image
		into some useful surfaces

		:param:
		:return:
		"""
		self.icon = pygame.image.load("./pictures/spaceInvaders_icon.jpg")
		self.gameSurf = pygame.transform.scale(load_file("./pictures/background.png"), self.displaySize)
		self.gameSurf = self.gameSurf.convert()
		self.MenuSurf = self.gameSurf.copy()
		self.SettingSurf = self.gameSurf.copy()

	def loadButtons(self, state=None):
		"""
		The loadButtons method to load
		differents buttons in function
		of the argument given

		:param state:
		:return an array of buttons:
		"""
		if state  == self.MENU:
			self.menuPlaySoloButton = Button(percentPix((50, 30)), self.MenuSurf, percentPix((20,15)), "Solo", self.Font, "./pictures/graySquareButton.png")
			self.menuPlayMultiButton = Button(percentPix((50,47)), self.MenuSurf, percentPix((20,15)), "Multi", self.Font, "./pictures/graySquareButton.png")
			self.menuSettingButton =  Button(percentPix((50,64)), self.MenuSurf, percentPix((20,15)), "Settings", self.Font, "./pictures/graySquareButton.png")
			self.menuLeaveButton = Button(percentPix((50,81)), self.MenuSurf, percentPix((20,15)),"Leave the Game", self.Font, "./pictures/graySquareButton.png")
			return [self.menuPlaySoloButton, self.menuPlayMultiButton, self.menuSettingButton, self.menuLeaveButton]
		elif state == self.SOLO:
			self.backToGameButton = Button(percentPix((50,35)), self.pauseSurf, percentPix((20,15)), "Back to game", self.Font, "./pictures/graySquareButton.png")
			self.backToMenuButton = Button(percentPix((50, 50)), self.pauseSurf, percentPix((20, 15)), "Back to menu", self.Font, "./pictures/graySquareButton.png")
			self.pauseSettingButton = Button(percentPix((50,65)), self.pauseSurf, percentPix((20,15)),"Settings", self.Font, "./pictures/graySquareButton.png")
			self.pauseLeaveButton = Button(percentPix((50,80)), self.pauseSurf, percentPix((20,15)), "Leave the Game", self.Font, "./pictures/graySquareButton.png")
			return [self.backToGameButton, self.backToMenuButton, self.pauseSettingButton, self.pauseLeaveButton]
		elif state == self.SETTINGS:
			self.fullscreenButton = Button(percentPix((65, 50)), self.SettingSurf, percentPix((20, 15)), "Fullscreen",self.Font, "./pictures/graySquareButton.png")
			self.windowedButton = Button(percentPix((35, 50)), self.SettingSurf, percentPix((20, 15)), "Windowed",self.Font, "./pictures/graySquareButton.png")
			self.saveButton = Button(percentPix((65, 25)), self.SettingSurf, percentPix((10, 15)), "Save",self.Font, "./pictures/graySquareButton.png")
			self.backButton = Button(percentPix((5, 90)), self.SettingSurf, percentPix((5.50,6.00)), "back", self.Font)
			return [self.fullscreenButton, self.windowedButton, self.saveButton, self.backButton]
