import os
import random
import time
from board import Board
from bots import *
import matplotlib.pyplot as plt

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

board = None

game_over = False
winner = 0
turn = random.randint(Board.PLAYER1_PIECE, Board.PLAYER2_PIECE)

def next_turn():
    global turn
    if turn == board.PLAYER1_PIECE:
        turn = board.PLAYER2_PIECE
    else:
        turn = board.PLAYER1_PIECE

def check_win(piece):
    if board.winning_move(piece):
        return [True, piece]
    if board.check_draw():
        return [True, 0]
    return [False]

def player_move(p, piece):
    global game_over, winner
    start = time.perf_counter()
    if turn == piece and not game_over:
        col = p.get_move(board)
        if board.is_valid_location(col):
            board.drop_piece(col, piece)
            next_turn()
            game_over = check_win(piece)[0]
            if game_over:
                winner = check_win(piece)[1]
    end = time.perf_counter()
    return end - start

def connect4(p1, p2):
    global game_over, board, winner

    board = Board(turn)
    time_p1 = time_p2 = 0
    moves_count_p1 = moves_count_p2 = 0

    while not game_over:
        time_p1 += player_move(p1, board.PLAYER1_PIECE)
        moves_count_p1 += 1
        time_p2 += player_move(p2, board.PLAYER2_PIECE)
        moves_count_p2 += 1
        if game_over:
            game_over = False
            return [winner, round(time_p1/moves_count_p1, 4)]

if __name__ == "__main__":
    # Minimax
    total_wins = []
    avg_time = []

    for d in range(1, 7):
        wins = 0
        a_time = 0.0
        for _ in range(20):
            winner, p1_time = connect4(MiniMaxBot(
                Board.PLAYER1_PIECE, d), OneStepLookAheadBot(Board.PLAYER2_PIECE))
            if winner == Board.PLAYER1_PIECE:
                wins += 1
                a_time += p1_time
        total_wins.append(wins)
        avg_time.append(a_time/20)

    plt.figure(figsize=(16, 7))

    plt.subplot(1, 2, 1)
    plt.plot(range(1, 7), total_wins)
    plt.xlabel("Depth")
    plt.ylabel("Wins")
    plt.ylim(0, 25)
    plt.title("Minimax Depth vs Wins")

    plt.subplot(1, 2, 2)
    plt.plot(range(1, 7), avg_time)
    plt.xlabel("Depth")
    plt.ylabel("Avg Time (s)")
    plt.title("Minimax Depth vs Avg Time")
    
    plt.savefig("./plots/Minimax.png")
    plt.show()


    # Expectimax 
    total_wins = []
    avg_time = []

    for d in range(1, 7):
        wins = 0
        a_time = 0.0
        for _ in range(20):
            winner, p1_time = connect4(ExpectiMaxBot(
                Board.PLAYER1_PIECE, d), OneStepLookAheadBot(Board.PLAYER2_PIECE))
            if winner == Board.PLAYER1_PIECE:
                wins += 1
                a_time += p1_time
        total_wins.append(wins)
        avg_time.append(a_time/20)

    plt.figure(figsize=(16, 7))

    plt.subplot(1, 2, 1)
    plt.plot(range(1, 7), total_wins)
    plt.xlabel("Depth")
    plt.ylabel("Wins")
    plt.ylim(0, 25)
    plt.title("Expectimax Depth vs Wins")

    plt.subplot(1, 2, 2)
    plt.plot(range(1, 7), avg_time)
    plt.xlabel("Depth")
    plt.ylabel("Avg Time (s)")
    plt.title("Expectimax Depth vs Avg Time")
    
    plt.savefig("./plots/Expectimax.png")
    plt.show()


    # Monte Carlo Tree Search
    total_wins = []
    avg_time = []

    for t in range(1, 4):
        wins = 0
        a_time = 0.0
        for _ in range(20):
            winner, p1_time = connect4(MonteCarloBot(
                Board.PLAYER1_PIECE, timeout=t), OneStepLookAheadBot(Board.PLAYER2_PIECE))
            if winner == Board.PLAYER1_PIECE:
                wins += 1
                a_time += p1_time
        total_wins.append(wins)
        avg_time.append(a_time/20)
        print("Timeout: ", t, "Wins: ", wins, "Avg Time: ", a_time/20)

    plt.figure(figsize=(16, 7))

    plt.subplot(1, 2, 1)
    plt.plot(range(1, 4), total_wins)
    plt.xlabel("Timeout")
    plt.ylabel("Wins")
    plt.ylim(0, 25)
    plt.title("Monte Carlo Timeout vs Wins")

    plt.subplot(1, 2, 2)
    plt.plot(range(1, 4), avg_time)
    plt.xlabel("Timeout")
    plt.ylabel("Avg Time (s)")
    plt.title("Monte Carlo Timeout vs Avg Time")
    
    plt.savefig("./plots/MonteCarlo.png")
    plt.show()
