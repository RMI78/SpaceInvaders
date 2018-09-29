import pygame
from classes import *
from functions import *

#ignite the window with title and size
displaySize = (1920, 1200)
pygame.init()
display = pygame.display.set_mode(displaySize, pygame.RESIZABLE)
pygame.display.set_caption("Space Invaders")

#load pics and resize it, load clock, load player and aim
icon = load_file("./images/spaceInvaders_icon.jpg")
background = load_file("./images/background.png")
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
	#the play part
	if state == RUNNING:
		clock.tick(60)
		display.blit(background, (0,0))
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
	pygame.display.flip()

pygame.quit()
