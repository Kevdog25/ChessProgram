from Game import *
import pygame
from pygame.locals import *
if __name__=="__main__":
	pygame.init()
	game = Game(1)
	clock = pygame.time.Clock()
	event = pygame.event.wait()
	while event.type != pygame.QUIT:
		clock.tick(60)
		if event.type == pygame.MOUSEBUTTONDOWN:
			game.click(pygame.mouse.get_pos())
		if event.type == pygame.KEYDOWN:
			if pygame.key.get_pressed()[pygame.K_f]:
				game.toggle_fps()
			
		game.update(clock)
		event = pygame.event.wait()