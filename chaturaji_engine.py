import random
import cProfile
from enum import Enum
import time
from search import get_best_move, get_nodes
from utils import *
from board import Board
from pieces import *

if __name__ == '__main__':
    board = Board()
    total_execution_time = 0
    num_searches = 0

    for i in range(100):
        print(f"Searching for the best move for {board.current_player}.")
        start_time = time.time()
        best_move, scores = get_best_move(board, 5) # fixed depth search
        end_time = time.time()
        nodes = get_nodes()
        execution_time = end_time - start_time
        total_execution_time += execution_time
        num_searches += 1

        print("Search completed")
        print(f"Number of nodes visited: {nodes + 1}")
        print(f"Execution time for this search: {execution_time} seconds")
        
        # Calculate and print average execution time
        avg_execution_time = total_execution_time / num_searches
        print(f"Average execution time so far: {avg_execution_time} seconds")

        nps = (nodes + 1) / (execution_time+0.001)
        print(f"Nodes per second (NPS): {nps}")
        if best_move:
            print(f"Best move: ({best_move.from_loc.row}, {best_move.from_loc.col}) to ({best_move.to_loc.row}, {best_move.to_loc.col}), Scores: {scores} ")
            print(f"san string of best_move: {get_san_string(best_move, board)}")
            print(f"uci string of best_move: {get_uci_string(best_move, board)}")
            # What happens if we play the best move
            board.make_move(best_move)
            print("Board state after playing best move: ")
            board.print_board()
            print("Turn: ", board.current_player)
            print("Active players: ", board.active_players)
            print("board.evaluate() output: ", board.evaluate(), "\n")
            print(f"Points: {board.player_points}")
            print(f"Total moves played in this game so far: {i}")
        else:
            print("No valid moves found or game is over. ")

    if (len(board.active_players) == 1):
        print(f"Game over! Final scores: {board.player_points}")