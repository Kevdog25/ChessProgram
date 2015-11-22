import numpy
import pygame
import pygame.locals
from copy import copy

class ChessEngine:
	"""A class for analysing and validating chess moves/positions"""
	def __init__(self):
		self.turn_number = 1
		self.colors = ['black','white']
		self.current_position = []
		self.previous_position = []
		return
	
	def test_move(self,moving_piece,movement,white,black,all_pieces):
		"""Tests if a move is legal and returns the update position or None if illegal"""
		self.list_of_pieces = all_pieces
		self.previous_position = copy(self.current_position)
		self.current_position = self.get_game_position()
		
		if movement in moving_piece.get_moveSet(all_pieces):
			if not self.try_move_piece(moving_piece,movement):
				return False
			self.turn_number+=1
			return True
			
		return False
	
	def get_game_position(self):
		"""Returns a matrix of all the pieces on the board for game analysis"""
		matrix = [[[] for i in range(8)] for j in range(8)]
		
		for piece in self.list_of_pieces:
			x = piece.rect.x/piece.rect.width
			y = piece.rect.y/piece.rect.height
			matrix[y][x] = piece

		return copy(matrix)
		
	def in_check(self):
		"""Checks if the 'color' king is being attacked"""
		color = self.colors[self.turn_number % 2]
		print color
		opposing_pieces = []
		for y in range(len(self.current_position)):
			for x in range(len(self.current_position[y])):
				if self.current_position[y][x] == []:
					continue
				if self.current_position[y][x].type == 'K' and self.current_position[y][x].color == color:
					king_pos = (x,y)
				if self.current_position[y][x].color != color:
					opposing_pieces.append(self.current_position[y][x])
					
		for piece in opposing_pieces:
			piece_pos_x = piece.rect.x/piece.rect.width
			piece_pos_y = piece.rect.y/piece.rect.height
			for move in piece.get_moveSet(self.list_of_pieces):
				if (piece_pos_x+move[0],piece_pos_y+move[1]) == king_pos:
					return True
		return False
		
	def try_move_piece(self,piece,move):
		"""Tries a move and reverts if it fails"""
		revert_x = piece.rect.x
		revert_y = piece.rect.y
		
		revert_position = copy(self.current_position)
		
		piece.rect.x+=move[0]*piece.rect.width
		piece.rect.y+=move[1]*piece.rect.height
		
		self.current_position = self.get_game_position()
		if self.in_check():
			self.current_position = copy(revert_position)
			piece.rect.x = revert_x
			piece.rect.y = revert_y
			return False
		else:
			return True
		
		