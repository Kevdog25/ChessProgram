import pygame
import pygame.locals
from Pieces import *
from Board import *
from ChessEngine import *

class Game:
	def __init__(self,game_mode):
		"""Initializes the game in the desired game_mode"""
		self.moved_pieces = pygame.sprite.LayeredDirty()
		self.taken_pieces = pygame.sprite.LayeredDirty()
		self.white_pieces = pygame.sprite.LayeredDirty()
		self.black_pieces = pygame.sprite.LayeredDirty()

		self.board = Board()
		self.board.display()

		self.load_piece_dict('TileSet.png')
		self.init_pieces()
		
		self.chess_engine = ChessEngine()

		self.dirty_rects = []
		self.selected_piece = None
		self.selected_square = None
		self.white_to_move = True
		
		self.display_fps = False
		#self.font = pygame.font.Font(None,12)
		#self.dirty_fps = (0,0,0,0)
			
			
	def toggle_fps(self):
		self.display_fps = not self.display_fps
		

	def load_piece_dict(self,filename):
			"""Load the table of chess pieces"""
			self.tile_set = pygame.image.load(filename).convert()
			image_width, image_height = self.tile_set.get_size()
			self.pieces_list = ['K','Q','N','B','R','P']
			self.piece_dict = {}
			for color,y in [('black',1),('white',3)]:
				tempdict = {}
				x = 0
				for piece in self.pieces_list:
					rect = (x*image_width/6,y*image_height/4,image_width/6,image_height/4)
					image = self.tile_set.subsurface(rect)
					image = pygame.transform.scale(image,(self.board.width/8,self.board.height/8))
					image.set_colorkey((255,0,0))
					tempdict[piece] = image
					x +=1
				self.piece_dict[color] = tempdict
			return
			
	def init_pieces(self): #Piece(self.piece_dict['black'][placement[y][x]],x*self.board.width/8,y*self.board.height/8)
		"""Places all of the pieces in an array"""
		backRank = ['R','N','B','Q','K','B','N','R']
		pawns = ['P','P','P','P','P','P','P','P']
		placement = [backRank,pawns]
		
		self.all_pieces = pygame.sprite.LayeredDirty()

		y = 0
		for row in placement:
			x = 0
			for key in row:
				piece = Piece(self.piece_dict['black'][key],x*self.board.width/8,y*self.board.height/8,key,'black')
				self.black_pieces.add(piece)
				self.all_pieces.add(piece)
				x+=1
			y+=1

		placement.reverse()
		y = 6
		for row in placement:
			x = 0
			for key in row:
				piece = Piece(self.piece_dict['white'][key],x*self.board.width/8,y*self.board.height/8,key,'white')		
				self.white_pieces.add(piece)
				self.all_pieces.add(piece)
				x+=1
			y+=1
		
		self.all_pieces.draw(self.board.screen)
		self.board.display()
		
	def update(self,clock):
		"""Updates the gamestate"""
		self.all_pieces.clear(self.board.screen,self.board.background)
		self.dirty_rects = self.all_pieces.draw(self.board.screen)
		
		if self.display_fps:
			print clock.get_fps()
		#	fps = clock.get_fps()
		#	fps_surface = self.font.render(str(fps),1,(255,255,20))
		#	self.dirty_fps = self.board.screen.blit(fps_surface,(7*self.board.width/8,7*self.board.height/8))
		#self.dirty_rects.append(self.dirty_fps)
			
		pygame.display.update(self.dirty_rects)
	
	def click(self,pos):
		"""Processes in game clicking"""
		if self.white_to_move:
			movable_pieces = self.white_pieces
		else:
			movable_pieces = self.black_pieces

		if self.selected_piece is not None:
			for row in self.board.squares:
				for rect in row:
					if rect.collidepoint(pos):
						self.selected_square = rect
						break

		for sprite in movable_pieces:
			if sprite.rect.collidepoint(pos):
				if sprite is not self.selected_piece:
					self.selected_piece = sprite
					break

		if self.selected_piece is not None and self.selected_square is not None:
			if self.selected_piece.rect != self.selected_square:
				print self.selected_piece.rect,self.selected_square,'\n'
				if self.get_test_move():
					self.move_piece()
					self.white_to_move = not self.white_to_move
					print 'moved'
				else:
					pass
					
					
				self.selected_piece = None
				self.selected_square = None
					

	def take_piece(self):
		"""Removes pieces that have been taken"""
		if self.selected_piece in self.white_pieces:
			taken = pygame.sprite.spritecollide(self.selected_piece,self.black_pieces,True)
		else:
			taken = pygame.sprite.spritecollide(self.selected_piece,self.white_pieces,True)
		if len(taken) !=0:
			self.taken_pieces.add(taken[0])
		return
		
	def move_piece(self):
		"""Moves the piece and updates the pieces moveSet if necessary"""
		self.selected_piece.dirty = 1
		self.selected_piece.update_move()
		self.selected_piece.rect = self.selected_square
		self.take_piece()
		
		
		
	def get_test_move(self):
		w = self.board.width/8
		h = self.board.height/8
		
		movement_x = (self.selected_square.x - self.selected_piece.rect.x)/w
		movement_y = (self.selected_square.y - self.selected_piece.rect.y)/h
		
		start_x = self.selected_piece.rect.x/w
		start_y = self.selected_piece.rect.y/h
		
		
		return self.chess_engine.test_move(self.selected_piece,(movement_x,movement_y),self.white_pieces,self.black_pieces,self.all_pieces)
	
	def remove_piece(self,sprite):
		"""Removes a piece from the board, and marks that rect to be updated"""
		sprite.dirty = 1
		sprite.kill()
		self.taken_pieces.add(sprite)