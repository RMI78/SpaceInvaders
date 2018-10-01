import pygame
from classes import *
from functions import *


#ignite pygame
pygame.init()

#ignite the window with title and size
infos = pygame.display.Info()
window = pygame.display.set_mode((infos.current_w, infos.current_h), pygame.RESIZABLE)
pygame.display.set_caption("Space Invaders")

#ignite fonts
Font = pygame.font.SysFont("monospace", 15)

#load pics and resize it, load clock, load player and aim

icon = load_file("./pictures/spaceInvaders_icon.jpg")
background = load_file("./pictures/Background.png")
background = pygame.transform.scale(background, displaySize)

pygame.display.set_icon(icon)
clock = pygame.time.Clock()

aim = Aim(display)
player = Player(display)
pygame.mouse.set_visible(False)
PAUSE = 0
RUNNING = 1
state = RUNNING

#start the window loop
loop = True
while loop:
	clock.tick(60)
	#the play part
	if state == RUNNING:

		window.blit(background, (0,0))
		window.blit(pauseSurf, (0,0))
		allsprites.draw(window)
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

		bullet_list.update(player)

	#the pause part
	if state == PAUSE:
		pauseSurf.set_alpha(255)
		pauseLoop = True
		PauseFont = Font.render("PAUSE", True,[255, 255, 255])
		window.blit(pauseSurf, (0,0))
		window.blit(PauseFont, (percentPix(47, True),percentPix(35, False)))
		image = Buttonify("pictures/GraySquareButton.png", (percentPix(60, True), percentPix(45, False)), pauseSurf)
		pygame.mouse.set_visible(True)
		for eventPause in pygame.event.get():
			if eventPause.type == pygame.QUIT:
				state = RUNNING
				loop = False
			if eventPause.type == pygame.MOUSEBUTTONDOWN and eventPause.button == 1:
				mouse = pygame.mouse.get_pos
				if image[1].colliderect(mouse):
					print("test reussi!")
			if eventPause.type == pygame.KEYDOWN:
				if eventPause.key == pygame.K_ESCAPE:
					pauseSurf.set_alpha(0)
					pygame.mouse.set_visible(False)
					state = RUNNING
			if event.type == pygame.QUIT:
				loop = False




	player.update()
	pygame.display.flip()

pygame.quit()
