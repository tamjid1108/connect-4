import numpy as np

class Evaluation:
	def __init__(self, piece):
		self.bot_piece = piece
		if self.bot_piece == 1:
			self.opp_piece = 2
		else:
			self.opp_piece = 1
	
	def score_position(self, board):

		# Constants for the evaluation function
		a = 100  # weight for num_blocking_sequences
		b = 5   # weight for center_control
		c = 2   # weight for edge_control
		d = 1   # weight for mobility
		e = 1   # weight for positional_advantage
		
		# Initialize scores to 0
		max_score = 0
		min_score = 0
		
		state = board.get_state()
		
		# Check for vertical blocking sequences
		for col in range(7):
			for row in range(3):
				if state[row][col] == state[row+1][col] == state[row+2][col] == self.opp_piece and state[row+3][col] == 0:
					min_score += a
						
		# Check for horizontal blocking sequences
		for row in range(6):
			for col in range(4):
				if state[row][col] == state[row][col+1] == state[row][col+2] == self.opp_piece and state[row][col+3] == 0:
					min_score += a
						
		# Check for diagonal blocking sequences (top-left to bottom-right)
		for row in range(3):
			for col in range(4):
				if state[row][col] == state[row+1][col+1] == state[row+2][col+2] == self.opp_piece and state[row+3][col+3] == 0:
					min_score += a
                    
		# Check for diagonal blocking sequences (top-right to bottom-left)
		for row in range(3):
			for col in range(3, 7):
				if state[row][col] == state[row+1][col-1] == state[row+2][col-2] == self.opp_piece and state[row+3][col-3] == 0:
					min_score += a
						
		# Check for center control
		center_col = 3
		center_rows = [0, 2, 3]
		for row in center_rows:
			if state[row][center_col] == self.bot_piece:
				max_score += b
			elif state[row][center_col] == self.opp_piece:
				min_score += b
		
		# Check for edge control
		edge_cols = [0, 6]
		edge_rows = [1, 2, 3, 4]
		for col in edge_cols:
			for row in edge_rows:
				if state[row][col] == self.bot_piece:
					max_score += c
				elif state[row][col] == self.opp_piece:
					min_score += c
						
		# Check for mobility
		moves = board.get_valid_locations()
		max_score += d * len(moves)
		min_score += d * len(moves)
						
		# Check for positional advantage
		max_score += e * np.sum(state == self.bot_piece)
		min_score += e * np.sum(state == self.opp_piece)
						
		return max_score - min_score

	def is_terminal_node(self, board):
		return board.winning_move(self.bot_piece) or board.winning_move(self.opp_piece) or len(board.get_valid_locations()) == 0
