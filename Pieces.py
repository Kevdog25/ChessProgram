import pygame
import pygame.locals

class Piece(pygame.sprite.DirtySprite):
	def __init__(self,surface,x,y,piece_type,color):
		pygame.sprite.DirtySprite.__init__(self)
		self.image = surface
		self.rect = self.image.get_rect()
		
		self.color = color
		
		self.has_moved = False
		self.type = piece_type
		self.rect.x = x
		self.rect.y = y
		
		
		self.set_moveSet()
		
		return
	
	def set_moveSet(self):
		self.total_moveSet = []
		
		if self.type == 'K':
			self.total_moveSet = [(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0)]
		elif self.type == 'P':
			if self.color is 'white':
				self.total_moveSet = [(0,-1),(0,-2)]
			else:
				self.total_moveSet = [(0,1),(0,2)]
		elif self.type == 'B':
			for i in range(1,8):
				self.total_moveSet.append((i,i))
				self.total_moveSet.append((-i,-i))
				self.total_moveSet.append((i,-i))
				self.total_moveSet.append((-i,i))
		elif self.type == 'N':
			self.total_moveSet = [(2,1),(1,2),(1,-2),(2,-1),(-2,1),(-2,-1),(-1,2),(-1,-2)]
		elif self.type == 'R':
			for i in range(1,8):
				self.total_moveSet.append((i,0))
				self.total_moveSet.append((0,i))
				self.total_moveSet.append((-i,0))
				self.total_moveSet.append((0,-i))
		elif self.type == 'Q':
			for i in range(1,8):
				self.total_moveSet.append((i,i))
				self.total_moveSet.append((-i,-i))
				self.total_moveSet.append((i,-i))
				self.total_moveSet.append((-i,i))
				self.total_moveSet.append((i,0))
				self.total_moveSet.append((0,i))
				self.total_moveSet.append((-i,0))
				self.total_moveSet.append((0,-i))
				
		return
	
	def update_move(self):
		if not self.has_moved:
			self.has_moved = True
			if self.type == 'P':
				try:
					self.total_moveSet.remove((0,-2))
				except ValueError:
					self.total_moveSet.remove((0,2))
					
	def get_moveSet(self,all_pieces):
		"""returns a modified list of legal moves"""
		self.current_position = self.get_current_position(all_pieces)
		return_moveSet = self.total_moveSet[:]
		
		
		x = self.rect.x/self.rect.width
		y = self.rect.y/self.rect.height
		
		for move in self.total_moveSet:
			if not(0 <= x+move[0] <8 and 0 <= y+move[1] <8):
				return_moveSet.remove(move)
			elif self.type != 'N':
				if self.is_obstructed((x,y),move):
					return_moveSet.remove(move)
		
		if self.type == 'P':
			if self.color == 'white':
				if self.current_position[y-1][x] != 0:
					return_moveSet.remove((0,-1))
				if (0 <= (x-1) < 8) and (0 <= (y-1) < 8):
					if self.current_position[y-1][x-1] == 'black':
						return_moveSet.append((-1,-1))
				if (0 <= (x+1) < 8) and (0 <= (y-1) < 8):
					if self.current_position[y-1][x+1] == 'black':
						return_moveSet.append((1,-1))
			else:
				if self.current_position[y+1][x] != 0:
					return_moveSet.remove((0,1))
				if (0 <= (x+1) < 8) and (0 <= (y+1) < 8):
					if self.current_position[y+1][x+1] == 'white':
						return_moveSet.append((1,1))
				if (0 <= (x-1) < 8) and (0 <= (y+1) < 8):
					if self.current_position[y+1][x-1] == 'white':
						return_moveSet.append((-1,1))
		
		return return_moveSet
		
	def is_obstructed(self,pos,move):
		norm_vector = (int(round(move[0]/abs((move[0])+0.0001))),int(round(move[1]/abs(move[1]+0.0001))))
	
		for r in range(1,max([abs(move[0]),abs(move[1])])):
			x = pos[0]+r*norm_vector[0]
			y = pos[1]+r*norm_vector[1]
			if self.current_position[y][x] != 0:
				return True
		
		return False
	
	def get_current_position(self,pieces_list):
		"""Returns a matrix of piece positions for legal move determination"""
		matrix = [[0 for i in range(8)] for j in range(8)]
		
		for piece in pieces_list:
			x = piece.rect.x/piece.rect.width
			y = piece.rect.y/piece.rect.height
			matrix[y][x] = piece.color
		return matrix
		