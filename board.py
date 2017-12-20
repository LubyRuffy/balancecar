import pygame,sys 
from pygame.locals import * 
pygame.init()

while True:
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			print "down"
