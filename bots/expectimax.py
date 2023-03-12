import random
import math
from bots.evaluation import Evaluation

class ExpectiMaxBot(Evaluation):
	def __init__(self, piece, depth=5):
		super().__init__(piece)
		self.depth = depth

	def expectimax(self, board, depth, maximizingPlayer):
		valid_locations = board.get_valid_locations()
		is_terminal = super().is_terminal_node(board)

		if depth == 0 or is_terminal:
			if is_terminal:
				if board.winning_move(self.bot_piece):
					return (None, 10000)
				elif board.winning_move(self.opp_piece):
					return (None, -10000)
				else: # Game is over, no more valid moves
					return (None, 0)
			else: # Depth is zero
				return (None, super().score_position(board))

		if maximizingPlayer: # (maximizing node)
			value = -math.inf
			column = random.choice(valid_locations)
			for col in valid_locations:
				b_copy = board.copy_board()
				b_copy.drop_piece(col, self.bot_piece)
				new_score = self.expectimax(b_copy, depth-1, False)[1]

				if new_score > value:
					value = new_score
					column = col

			return column, value
		
		else: # Expecting player (chance node)
			value = 0
			column = random.choice(valid_locations)
			for col in valid_locations:
				b_copy = board.copy_board()
				b_copy.drop_piece(col, self.opp_piece)
				new_score = self.expectimax(b_copy, depth-1, True)[1]

				value += new_score

			value = math.floor(value/len(valid_locations))

			return column, value

	def get_move(self, board):
		col, expectimax_score = self.expectimax(board, self.depth, True)
		return col
