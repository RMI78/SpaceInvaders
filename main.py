import pygame
from classes import *
from functions import *

#ignite the window with title and size
pygame.init()
infos = pygame.display.Info()
displaySize = (infos.current_w, infos.current_h)
window = pygame.display.set_mode(displaySize, pygame.RESIZABLE)
pygame.display.set_caption("Space Invaders")
Font = pygame.font.SysFont("monospace", 15)

#load pics and resize it, load clock, load player and aim
icon = load_file("./pictures/spaceInvaders_icon.jpg")
background = load_file("./pictures/background.png")
defaultButton = load_file("./pictures/graySquareButton.png")
background = pygame.transform.scale(background, (infos.current_w, infos.current_h))
pauseSurf = pygame.Surface((infos.current_w, infos.current_h))
pauseSurf.fill((0,0,0))

pygame.display.set_icon(icon)
clock = pygame.time.Clock()

aim = Aim(window)
player = Player(window)
pygame.mouse.set_visible(False)
PAUSE = 0
RUNNING = 1
state = RUNNING

pauseSurf = pygame.Surface(pygame.display.get_surface().get_size())
pauseSurf.fill(pygame.Color("black"))
pauseSurf.set_alpha(0)

#start the window loop
loop = True
while loop:
	clock.tick(60)
	#the play part
	if state == RUNNING:
		window.blit(background, (0,0))
		pygame.event.pump()
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
		pauseSurf.set_alpha(255)
		pauseLoop = True
		PauseFont = Font.render("PAUSE", True,[255, 255, 255])
		window.blit(pauseSurf, (0,0))
		window.blit(PauseFont, (percentPix(48, True),percentPix(25, False)))
		backToGameButton = Buttonify(defaultButton, (percentPix(50, True), percentPix(35, False)), pauseSurf, "Back to the game", Font)
		settingButton = Buttonify(defaultButton, (percentPix(50, True), percentPix(50, False)), pauseSurf,"Settings", Font)
		leaveButton = Buttonify(defaultButton, (percentPix(50, True), percentPix(65, False)), pauseSurf, "Leave the Game", Font)
		pygame.mouse.set_visible(True)
		for eventPause in pygame.event.get():
			if eventPause.type == pygame.QUIT:
				state = RUNNING
				loop = False
			if eventPause.type == pygame.MOUSEBUTTONDOWN and eventPause.button == 1:
				if backToGameButton[-1].collidepoint(pygame.mouse.get_pos()):
					pygame.mouse.set_visible(False)
					state = RUNNING
				if settingButton[-1].collidepoint(pygame.mouse.get_pos()):
					pass #definition to print the settings ??
				if leaveButton[-1].collidepoint(pygame.mouse.get_pos()):
					loop = False
			if eventPause.type == pygame.KEYDOWN:
				if eventPause.key == pygame.K_ESCAPE:
					pygame.mouse.set_visible(False)
					state = RUNNING
			if event.type == pygame.QUIT:
				loop = False

	pygame.display.flip()

pygame.quit()
