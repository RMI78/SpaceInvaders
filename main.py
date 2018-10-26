import pygame
from classes import *
from functions import *




#ignite the window with title, size and icon
pygame.init()
manager = Manager("setting.conf")

#set the flags
LEAVE = 0
SOLO = 1
MENU = 2
SETTINGS = 3
MULTI = 4

pygame.event.pump()
state = MENU
while state != LEAVE:
	if state == MENU:
		state = manager.menu()
	if state == SOLO:
		state = manager.solo()
	if state == SETTINGS:
		state = manager.settings()
pygame.quit()
