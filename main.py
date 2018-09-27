import pygame
from classes import *
from functions import *

#ignite the window with title and size
pygame.init()
window = pygame.display.set_mode((1920, 1200), pygame.RESIZABLE)
pygame.display.set_caption("Space Invaders")

#load pics and resize it, load clock, load player and aim
icon = load_file("./images/spaceInvaders_icon.jpg")
background = load_file("./images/background.png")
background = pygame.transform.scale(background, (1920, 1200))

pygame.display.set_icon(icon)
clock = pygame.time.Clock()

aim = Aim()
player = Player()
allsprites = pygame.sprite.RenderPlain((player, aim))
bullet_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
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
	#the play part
	if state == RUNNING:
		clock.tick(30)
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
				bullet = Bullet(player, 7)
				allsprites.add(bullet)
				bullet_list.add(bullet)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE: state = PAUSE
		bullet_list.update(player)

	#the pause part
	if state == PAUSE:
		pauseSurf.set_alpha(255)
		pauseLoop = True
		for eventPause in pygame.event.get():
			if eventPause.type == pygame.KEYDOWN:
				if eventPause.key == pygame.K_ESCAPE:
					pauseSurf.set_alpha(0)
					state = RUNNING
			if event.type == pygame.QUIT:
				loop = False



	pygame.display.flip()

pygame.quit()
