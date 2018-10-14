import pygame
from classes import *
from functions import *

#ignite the window with title, size and icon
pygame.init()
infos = pygame.display.Info()
displaySize = (infos.current_w, infos.current_h)
window = pygame.display.set_mode(displaySize, pygame.RESIZABLE)
pygame.display.set_caption("Space Invaders")
Font = pygame.font.SysFont("monospace", 35, True)

#load pics and resize it, load clock, load player and aim
icon = load_file("./pictures/spaceInvaders_icon.jpg")
background = load_file("./pictures/background.png")
background = pygame.transform.scale(background, (infos.current_w, infos.current_h))
MenuSurf = pygame.transform.scale(background, (infos.current_w, infos.current_h))
pauseSurf = pygame.Surface(pygame.display.get_surface().get_size())
pauseSurf.fill(pygame.Color("black"))
pauseSurf.set_alpha(200)

pygame.display.set_icon(icon)
clock = pygame.time.Clock()
pygame.event.pump()

aim = Aim(window)
player = Player(window)
PAUSE = 0
RUNNING = 1
MENU = 2
state = MENU
INIT = False

#start the window loop
loop = True
while loop:
	clock.tick(60)

	#the menu part
	if state == MENU:
		MenuFont = Font.render("Space Invaders", True, [255,255,255])
		window.blit(MenuSurf, (0,0))
		window.blit(MenuFont, percentPix((42, 15)))
		#menuPlaySoloButton = Buttonify(defaultButton, percentPix((50,30)), MenuSurf, "Solo", Font)
		menuPlaySoloButton = Button(percentPix((50, 30)), MenuSurf, percentPix((20,15)), "Solo", Font, "./pictures/graySquareButton.png")
		menuPlayMultiButton = Button(percentPix((50,45)), MenuSurf, percentPix((20,15)), "Coop", Font, "./pictures/graySquareButton.png")
		menuSettingButton =  Button(percentPix((50,60)), MenuSurf, percentPix((20,15)), "Settings", Font, "./pictures/graySquareButton.png")
		menuLeaveButton = Button(percentPix((50,75)), MenuSurf, percentPix((20,15)),"Leave the Game", Font, "./pictures/graySquareButton.png")

		#things that need to be looped
		menuPlaySoloButton.display()
		menuPlayMultiButton.display()
		menuSettingButton.display()
		menuLeaveButton.display()
		for eventMenu in pygame.event.get():
			if eventMenu.type == pygame.QUIT:
				state = RUNNING
				loop = False
			if eventMenu.type == pygame.MOUSEBUTTONDOWN and eventMenu.button == 1:
				if menuPlaySoloButton.imageRect.collidepoint(pygame.mouse.get_pos()):
					pygame.mouse.set_visible(False)
					state = RUNNING
				if menuSettingButton.imageRect.collidepoint(pygame.mouse.get_pos()):
					pass #class to manage the settings ??
				if menuLeaveButton.imageRect.collidepoint(pygame.mouse.get_pos()):
					loop = False
			if eventMenu.type == pygame.QUIT:
				loop = False

	#the play part
	if state == RUNNING:
		pygame.mouse.set_visible(False)

		window.blit(background, (0,0))

		aim.focusAim()

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
				loop = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				player.shoot()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE: state = PAUSE
		player.update()

	#the pause part
	if state == PAUSE:
		pauseLoop = True
		PauseFont = Font.render("PAUSE", True,[255, 255, 255])
		window.blit(pauseSurf, (0,0))
		window.blit(PauseFont, percentPix((47,25)))
		backToGameButton = Button(percentPix((50,35)), pauseSurf, percentPix((20,15)), "Back to game", Font, "./pictures/graySquareButton.png")
		pauseSettingButton = Button(percentPix((50,50)), pauseSurf, percentPix((20,15)),"Settings", Font, "./pictures/graySquareButton.png")
		pauseLeaveButton = Button(percentPix((50,65)), pauseSurf, percentPix((20,15)), "Leave the Game", Font, "./pictures/graySquareButton.png")
		backToGameButton.display()
		pauseSettingButton.display()
		pauseLeaveButton.display()
		pygame.mouse.set_visible(True)
		for eventPause in pygame.event.get():
			if eventPause.type == pygame.QUIT:
				state = RUNNING
				loop = False
			if eventPause.type == pygame.MOUSEBUTTONDOWN and eventPause.button == 1:
				if backToGameButton.imageRect.collidepoint(pygame.mouse.get_pos()):
					pygame.mouse.set_visible(False)
					state = RUNNING
				if pauseSettingButton.imageRect.collidepoint(pygame.mouse.get_pos()):
					pass #definition to print the settings ??
				if pauseLeaveButton.imageRect.collidepoint(pygame.mouse.get_pos()):
					loop = False
			if eventPause.type == pygame.KEYDOWN:
				if eventPause.key == pygame.K_ESCAPE:
					pygame.mouse.set_visible(False)
					state = RUNNING
			if eventPause.type == pygame.QUIT:
				loop = False

	pygame.display.flip()

pygame.quit()
