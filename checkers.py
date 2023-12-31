import pygame, sys
from pygame.locals import *
from time import sleep
import pygame_gui

pygame.init()

##색상##
#             R    G    B
WHITE    = (255, 255, 255)
BLUE     = (  0,   0, 255)
RED      = (255,   0,   0)
BLACK    = (  0,   0,   0)
GOLD     = (255, 215,   0)
HIGH     = (160, 190, 255)

##방향##
NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"

manager = pygame_gui.UIManager((600, 600))

class Game:
	def __init__(self, loop_mode):
		self.graphics = Graphics()
		self.board = Board()
		self.endit = False
		self.turn = BLUE
		self.selected_piece = None
		self.hop = False
		self.loop_mode = loop_mode
		self.selected_legal_moves = []
		self.graphics.paused = False
		self.clock = pygame.time.Clock()
		self.fps = 60
		self.graphics.confirm = None
		self.yes = False

	def setup(self):
		# Draw the window and board at the beginning of the game
		self.graphics.setup_window()

	def player_turn(self):
		mouse_pos = tuple(map(int, pygame.mouse.get_pos()))
		self.mouse_pos = tuple(map(int, self.graphics.board_coords(mouse_pos[0], mouse_pos[1]))) # what square is the mouse in?
		if self.selected_piece != None:
			self.selected_legal_moves = self.board.legal_moves(self.selected_piece[0], self.selected_piece[1], self.hop)

		for event in pygame.event.get():
			if event.type == QUIT:
				self.terminate_game()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE and self.graphics.exit != True:
					self.graphics.paused = not self.graphics.paused
					self.graphics.message = not self.graphics.message
				elif event.key == pygame.K_q and self.graphics.paused != True:
					self.graphics.exit = not self.graphics.exit

					if self.graphics.exit:
						self.graphics.confirm = pygame_gui.windows.UIConfirmationDialog(rect=pygame.Rect((250, 200), (300, 200)),
                                                                    manager=manager,
                                                                    window_title='Quit Confirmation',
                                                                    action_long_desc='Are you sure you want to quit?',
                                                                    action_short_name='Yes',
                                                                    blocking=True) # 다른 곳 클릭 금지시키기

			if event.type == pygame.USEREVENT:
				if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
					if event.ui_element == self.graphics.confirm:
						if self.yes:
							self.graphics.exit = not self.graphics.exit
						else:
							self.terminate_game()
				elif event.user_type == pygame_gui.UI_WINDOW_CLOSE:
					if event.ui_element == self.graphics.confirm:
						self.graphics.exit = False
						print("그냥닫힘")

			if event.type == MOUSEBUTTONDOWN:
				if self.hop == False:
					if self.board.location(self.mouse_pos[0], self.mouse_pos[1]).occupant != None and self.board.location(self.mouse_pos[0], self.mouse_pos[1]).occupant.color == self.turn:
						self.selected_piece = self.mouse_pos

					elif self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece[0], self.selected_piece[1]):

						self.board.move_piece(self.selected_piece[0], self.selected_piece[1], self.mouse_pos[0], self.mouse_pos[1])

						if self.mouse_pos not in self.board.adjacent(self.selected_piece[0], self.selected_piece[1]):
							self.board.remove_piece(self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) // 2, self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) // 2)

							self.hop = True
							self.selected_piece = self.mouse_pos
						else:
							self.end_turn()

				if self.hop == True:
					if self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece[0], self.selected_piece[1], self.hop):
						self.board.move_piece(self.selected_piece[0], self.selected_piece[1], self.mouse_pos[0], self.mouse_pos[1])
						self.board.remove_piece(self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) // 2, self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) // 2)

					if self.board.legal_moves(self.mouse_pos[0], self.mouse_pos[1], self.hop) == []:
							self.end_turn()

					else:
						self.selected_piece = self.mouse_pos
			
			manager.process_events(event)


	def update(self):
		self.graphics.update_display(self.board, self.selected_legal_moves, self.selected_piece)
		pygame.display.update()

	def terminate_game(self):
		pygame.quit()
		sys.exit()

	def main(self):
		self.setup()

		while True: # main game loop
			self.player_turn()
			self.update()

	def end_turn(self):
		if self.turn == BLUE:
			self.turn = RED
		else:
			self.turn = BLUE

		self.selected_piece = None
		self.selected_legal_moves = []
		self.hop = False

		if self.check_for_endgame():
			if self.turn == BLUE:
				print('RED WINS!')
				self.graphics.draw_message("RED WINS!")
			else:
				print('BLUE WINS!')
				self.graphics.draw_message("BLUE WINS!")
			print(self.turn)
			if(self.loop_mode):
				self.endit = True
			else:
				self.terminate_game()


	def check_for_endgame(self):
		for x in range(8):
			for y in range(8):
				if self.board.location(x, y).color == BLACK and self.board.location(x, y).occupant != None and self.board.location(x, y).occupant.color == self.turn:
					if self.board.legal_moves(x, y) != []:
						return False

		return True

class Graphics:
	def __init__(self):
		self.caption = "CLASSIC BOARD GAME : CHECKERS V1.0"

		self.window_size = 600
		self.screen = pygame.display.set_mode((self.window_size, self.window_size))
		self.background = pygame.image.load('resources/board.png')

		self.square_size = self.window_size // 8
		self.piece_size = self.square_size // 2

		self.message = False
		self.paused = False
		self.exit = False
		self.bg = pygame.image.load('bg.png')
		self.confirm = None

	def setup_window(self):
		pygame.init()
		pygame.display.set_caption(self.caption)

	def update_display(self, board, legal_moves, selected_piece):
		"""
		This updates the current display.
		"""

		manager.update(pygame.time.Clock().tick(60))

		if self.exit == False:
			pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP])
			self.screen.blit(self.background, (0,0))

			self.highlight_squares(legal_moves, selected_piece)
			self.draw_board_pieces(board)
		if self.exit and self.paused != True:
			pygame.event.set_blocked([pygame.KEYDOWN, pygame.KEYUP])
			self.screen.blit(self.bg, (0, 0))
			manager.draw_ui(self.screen)
			pygame.display.update()
		else:
			if self.paused:
				self.draw_message("Paused")  # 일시정지 메시지를 그림.
				self.screen.blit(self.bg, (0, 0))
				pygame.event.set_blocked(MOUSEBUTTONDOWN)

			else:
				pygame.event.set_allowed(MOUSEBUTTONDOWN)

			if self.message:
				self.screen.blit(self.text_surface_obj, self.text_rect_obj)

			pygame.display.update()

	def draw_board_squares(self, board):
		"""
		Takes a board object and draws all of its squares to the display
		"""
		for x in range(8):
			for y in range(8):
				pygame.draw.rect(self.screen, board[x][y].color, (x * self.square_size, y * self.square_size, self.square_size, self.square_size), )

	def draw_board_pieces(self, board):
		for x in range(8):
			for y in range(8):
				if board.matrix[x][y].occupant != None:
					pygame.draw.circle(self.screen, board.matrix[x][y].occupant.color, tuple(map(int, self.pixel_coords((x, y)))), int(self.piece_size))

					if board.location(x,y).occupant.king == True:
						pygame.draw.circle(self.screen, GOLD, self.pixel_coords((x, y)), int(self.piece_size // 1.7), self.piece_size // 4)

	def pixel_coords(self, board_coords):
		return (board_coords[0] * self.square_size + self.piece_size, board_coords[1] * self.square_size + self.piece_size)

	def board_coords(self, pixel_x, pixel_y):
		return (pixel_x // self.square_size, pixel_y // self.square_size)

	def highlight_squares(self, squares, origin):
		for square in squares:
			pygame.draw.rect(self.screen, HIGH, (square[0] * self.square_size, square[1] * self.square_size, self.square_size, self.square_size))

		if origin != None:
			pygame.draw.rect(self.screen, HIGH, (origin[0] * self.square_size, origin[1] * self.square_size, self.square_size, self.square_size))

	def draw_message(self, message): # draw message on the screen
		print("[DEBUG]: 메시지 실행중입니다.")
		self.message = True
		self.font_obj = pygame.font.Font('NanumMyeongjoExtraBold.ttf', 44)
		self.text_surface_obj = self.font_obj.render(message, True, HIGH, BLACK)
		self.text_rect_obj = self.text_surface_obj.get_rect()
		self.text_rect_obj.center = (self.window_size // 2, self.window_size // 2)

class Board:
	def __init__(self):
		self.matrix = self.new_board()

	def new_board(self):
		"""
		Create a new board matrix.
		"""

		# initialize squares and place them in matrix

		matrix = [[None] * 8 for i in range(8)]

		for x in range(8):
			for y in range(8):
				if (x % 2 != 0) and (y % 2 == 0):
					matrix[y][x] = Square(WHITE)
				elif (x % 2 != 0) and (y % 2 != 0):
					matrix[y][x] = Square(BLACK)
				elif (x % 2 == 0) and (y % 2 != 0):
					matrix[y][x] = Square(WHITE)
				elif (x % 2 == 0) and (y % 2 == 0):
					matrix[y][x] = Square(BLACK)

		# 말들 초기화 하고 위치 세밀하게 구분하여 배치

		for x in range(8):
			for y in range(3):
				if matrix[x][y].color == BLACK:
					matrix[x][y].occupant = Piece(RED)
			for y in range(5, 8):
				if matrix[x][y].color == BLACK:
					matrix[x][y].occupant = Piece(BLUE)

		return matrix

	def board_string(self, board):
		board_string = [[None] * 8] * 8

		for x in range(8):
			for y in range(8):
				if board[x][y].color == WHITE:
					board_string[x][y] = "WHITE"
				else:
					board_string[x][y] = "BLACK"


		return board_string

	def rel(self, dir, x, y):
		if dir == NORTHWEST:
			return (x - 1, y - 1)
		elif dir == NORTHEAST:
			return (x + 1, y - 1)
		elif dir == SOUTHWEST:
			return (x - 1, y + 1)
		elif dir == SOUTHEAST:
			return (x + 1, y + 1)
		else:
			return 0

	def adjacent(self, x, y):
		return [self.rel(NORTHWEST, x,y), self.rel(NORTHEAST, x,y),self.rel(SOUTHWEST, x,y),self.rel(SOUTHEAST, x,y)]

	def location(self, x, y):
		x = int(x)
		y = int(y)
		return self.matrix[x][y]

	def blind_legal_moves(self, x, y):
		if self.matrix[x][y].occupant != None:

			if self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == BLUE:
				blind_legal_moves = [self.rel(NORTHWEST, x, y), self.rel(NORTHEAST, x, y)]

			elif self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == RED:
				blind_legal_moves = [self.rel(SOUTHWEST, x, y), self.rel(SOUTHEAST, x, y)]

			else:
				blind_legal_moves = [self.rel(NORTHWEST, x, y), self.rel(NORTHEAST, x, y), self.rel(SOUTHWEST, x, y), self.rel(SOUTHEAST, x, y)]

		else:
			blind_legal_moves = []

		return blind_legal_moves

	def legal_moves(self, x, y, hop = False):
		blind_legal_moves = self.blind_legal_moves(x, y)
		# print('BLind Legal moves', blind_legal_moves)
		legal_moves = []

		if hop == False:
			for move in blind_legal_moves:
				if hop == False:
					if self.on_board(move[0], move[1]):
						if self.location(move[0], move[1]).occupant == None:
							legal_moves.append(move)

						elif self.location(move[0], move[1]).occupant.color != self.location(x, y).occupant.color and self.on_board(move[0] + (move[0] - x), move[1] + (move[1] - y)) and self.location(move[0] + (move[0] - x), move[1] + (move[1] - y)).occupant == None: # is this location filled by an enemy piece?
							legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

		else: # hop == True
			for move in blind_legal_moves:
				if self.on_board(move[0], move[1]) and self.location(move[0], move[1]).occupant != None:
					if self.location(move[0], move[1]).occupant.color != self.location(x, y).occupant.color and self.on_board(move[0] + (move[0] - x), move[1] + (move[1] - y)) and self.location(move[0] + (move[0] - x), move[1] + (move[1] - y)).occupant == None: # is this location filled by an enemy piece?
						legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

		return legal_moves

	def remove_piece(self, x, y):
		self.matrix[x][y].occupant = None

	def move_piece(self, start_x, start_y, end_x, end_y):

		self.matrix[end_x][end_y].occupant = self.matrix[start_x][start_y].occupant
		self.remove_piece(start_x, start_y)

		self.king(end_x, end_y)

	def is_end_square(self, coords):

		if coords[1] == 0 or coords[1] == 7:
			return True
		else:
			return False

	def on_board(self, x, y):

		if x < 0 or y < 0 or x > 7 or y > 7:
			return False
		else:
			return True


	def king(self, x, y):
		# 왕으로 승급
		if self.location(x, y).occupant != None:
			if (self.location(x, y).occupant.color == BLUE and y == 0) or (self.location(x, y).occupant.color == RED and y == 7):
				self.location(x, y).occupant.crown()

	def repr_matrix(self):
		for j in range(8):
			for i in range(8):
				if self.matrix[i][j].occupant is not None:
					if self.matrix[i][j].occupant.color == BLUE:
						print('B', end=" ")
					else:
						print('R', end=" ")
				else:
					print('X', end=" ")
			print('')

class Piece: # 실질적인 승급을 관리
	def __init__(self, color, king = False):
		self.color = color
		self.king = king
		self.value = 1

	def crown(self):
		self.king = True
		self.value = 2

class Square:
	def __init__(self, color, occupant = None):
		self.color = color # color is either BLACK or WHITE
		self.occupant = occupant # occupant is a Square object