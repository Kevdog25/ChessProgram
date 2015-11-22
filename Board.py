import pygame
import pygame.locals
from random import random, seed

class Board:
	def __init__(self,width = 640,height = 640,tile_set_file = 'TileSet.png'):
		"""Initializes the entire board"""
		self.width = width
		self.height = height
		self.squares = []
		self.initScreen()

		return
		
	def initScreen(self):
		"""Initializes the background"""
		self.screen = pygame.display.set_mode((self.width,self.height))
		xLength = self.width/8
		yLength = self.height/8
		self.background = pygame.Surface((self.width,self.height))
		for x in range(0,8):
			row_of_rects = []
			for y in range(0,8):
				row_of_rects.append(pygame.Rect(x*xLength,y*yLength,xLength,yLength))

				if (x+y) % 2 == 0:
					self.background.fill((255,255,255),(x*xLength,y*yLength,xLength,yLength))
				else:
					self.background.fill((0,0,0),(x*xLength,y*yLength,xLength,yLength))
			self.squares.append(row_of_rects)
		self.screen.blit(self.background,(0,0))
		return
	
	def rotate(self,angle = 90):
		"""Rotates and updates the display"""
		self.screen.blit(pygame.transform.rotate(self.screen,angle),(0,0))
		pygame.display.update()
	
	def display(self,rectangle = None):
		"""Displays/Updates the board"""
		if rectangle is None:
			pygame.display.flip()
		else:
			pygame.display.update(rectangle)
		return
	
	def select_rect(self,rect,sprite_list = None):
		"""Puts a boarder around a rectangle and updates any sprites inside"""
		pass
if __name__=='__main__':
	pygame.init()
	board = Board()
	board.display()
	seed()
	event = pygame.event.wait()
	while event.type != pygame.QUIT:
		event = pygame.event.wait()
		if event.type == pygame.KEYDOWN:
			board.rotate()