import numpy as np

class Evaluation:
	def __init__(self, piece):
		self.bot_piece = piece
		if self.bot_piece == 1:
			self.opp_piece = 2
		else:
			self.opp_piece = 1

	# def evaluate_window(self, board, window):
	# 	score = 0
	# 	if window.count(self.bot_piece) == 4:
	# 		score += 100
	# 	elif window.count(self.bot_piece) == 3 and window.count(board.EMPTY) == 1:
	# 		score += 5
	# 	elif window.count(self.bot_piece) == 2 and window.count(board.EMPTY) == 2:
	# 		score += 2

	# 	if window.count(self.opp_piece) == 3 and window.count(board.EMPTY) == 1:
	# 		score -= 4

	# 	return score

	# def score_position(self, board):
	# 	score = 0

		# ## Score center column
		# center_array = [int(i) for i in list(board.get_board()[:, board.COLUMN_COUNT//2])]
		# center_count = center_array.count(self.bot_piece)
		# score += center_count * 3

	# 	## Score Horizontal
	# 	for r in range(board.ROW_COUNT):
	# 		row_array = [int(i) for i in list(board.get_board()[r,:])]
	# 		for c in range(board.COLUMN_COUNT-3):
	# 			window = row_array[c:c+board.WINDOW_LENGTH]
	# 			score += self.evaluate_window(board, window)

	# 	## Score Vertical
	# 	for c in range(board.COLUMN_COUNT):
	# 		col_array = [int(i) for i in list(board.get_board()[:,c])]
	# 		for r in range(board.ROW_COUNT-3):
	# 			window = col_array[r:r+board.WINDOW_LENGTH]
	# 			score += self.evaluate_window(board, window)

	# 	## Score positive sloped diagonal
	# 	for r in range(board.ROW_COUNT-3):
	# 		for c in range(board.COLUMN_COUNT-3):
	# 			window = [board.get_board()[r+i][c+i] for i in range(board.WINDOW_LENGTH)]
	# 			score += self.evaluate_window(board, window)

	# 	## Score negative sloped diagonal
	# 	for r in range(board.ROW_COUNT-3):
	# 		for c in range(board.COLUMN_COUNT-3):
	# 			window = [board.get_board()[r+3-i][c+i] for i in range(board.WINDOW_LENGTH)]
	# 			score += self.evaluate_window(board, window)

	# 	return score
	
	def score_position(self, board):
		# Constants for the evaluation function
		b = 100  # weight for num_blocking_sequences
		c = 5   # weight for center_control
		d = 2   # weight for edge_control
		e = 1   # weight for mobility
		f = 1   # weight for positional_advantage
		
		# Initialize scores to 0
		max_score = 0
		min_score = 0
		
		state = board.get_board()
		# Check for vertical winning sequences
		# for col in range(7):
		# 	for row in range(3):
		# 		if state[row][col] == state[row+1][col] == state[row+2][col] == state[row+3][col]:
		# 			if state[row][col] == self.bot_piece:
		# 				max_score += a
		# 			elif state[row][col] == self.opp_piece:
		# 				min_score += a
						
		# # Check for horizontal winning sequences
		# for row in range(6):
		# 	for col in range(4):
		# 		if state[row][col] == state[row][col+1] == state[row][col+2] == state[row][col+3]:
		# 			if state[row][col] == self.bot_piece:
		# 				max_score += a
		# 			elif state[row][col] == self.opp_piece:
		# 				min_score += a
						
		# # Check for diagonal winning sequences (top-left to bottom-right)
		# for row in range(3):
		# 	for col in range(4):
		# 		if state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3]:
		# 			if state[row][col] == self.bot_piece:
		# 				max_score += a
		# 			elif state[row][col] == self.opp_piece:
		# 				min_score += a
						
		# # Check for diagonal winning sequences (top-right to bottom-left)
		# for row in range(3):
		# 	for col in range(3, 7):
		# 		if state[row][col] == state[row+1][col-1] == state[row+2][col-2] == state[row+3][col-3]:
		# 			if state[row][col] == self.bot_piece:
		# 				max_score += a
		# 			elif state[row][col] == self.opp_piece:
		# 				min_score += a
						
		# Check for vertical blocking sequences
		for col in range(7):
			for row in range(3):
				if state[row][col] == state[row+1][col] == state[row+2][col] == self.opp_piece and state[row+3][col] == 0:
					min_score += b
						
		# Check for horizontal blocking sequences
		for row in range(6):
			for col in range(4):
				if state[row][col] == state[row][col+1] == state[row][col+2] == self.opp_piece and state[row][col+3] == 0:
					min_score += b
						
		# Check for diagonal blocking sequences (top-left to bottom-right)
		for row in range(3):
			for col in range(4):
				if state[row][col] == state[row+1][col+1] == state[row+2][col+2] == self.opp_piece and state[row+3][col+3] == 0:
					min_score += b
                    
		# Check for diagonal blocking sequences (top-right to bottom-left)
		for row in range(3):
			for col in range(3, 7):
				if state[row][col] == state[row+1][col-1] == state[row+2][col-2] == self.opp_piece and state[row+3][col-3] == 0:
					min_score += b
						
		# Check for center control
		center_col = 3
		center_rows = [0, 2, 3]
		for row in center_rows:
			if state[row][center_col] == self.bot_piece:
				max_score += c
			elif state[row][center_col] == self.opp_piece:
				min_score += c 
		# for row in range(6):
		# 	if state[row][center_col] == self.bot_piece:
		# 		max_score += c
		# 	elif state[row][center_col] == self.opp_piece:
		# 		min_score += c 
						
		# Check for edge control
		edge_cols = [0, 6]
		edge_rows = [1, 2, 3, 4]
		for col in edge_cols:
			for row in edge_rows:
				if state[row][col] == self.bot_piece:
					max_score += d
				elif state[row][col] == self.opp_piece:
					min_score += d
						
		# Check for mobility
		moves = board.get_valid_locations()
		max_score += e * len(moves)
		min_score += e * len(moves)
						
		# Check for positional advantage
		max_score += f * np.sum(state == self.bot_piece)
		min_score += f * np.sum(state == self.opp_piece)
						
		return max_score - min_score

	def is_terminal_node(self, board):
		return board.winning_move(self.bot_piece) or board.winning_move(self.opp_piece) or len(board.get_valid_locations()) == 0
