import random
import cProfile
import time
from board import Board
from mcts_search import MCTSNode, MCTS
from utils import get_san_string, get_uci_string  

if __name__ == '__main__':
    board = Board()
    total_execution_time = 0
    num_searches = 0

    for i in range(100):
        print(f"Searching for the best move for {board.current_player}.")
        start_time = time.time()
        root_node = MCTSNode(board)
        MCTS(root_node, 10000, 5)  # Run MCTS Search for 1000 iterations
        best_move = root_node.best_move() 
        end_time = time.time()

        execution_time = end_time - start_time
        total_execution_time += execution_time
        num_searches += 1

        print("Search completed")
        print(f"Execution time for this search: {execution_time} seconds")
        
        # Calculate and print average execution time
        avg_execution_time = total_execution_time / num_searches
        print(f"Average execution time so far: {avg_execution_time} seconds")

        if best_move:
            print(f"Best move: ({best_move.from_loc.row}, {best_move.from_loc.col}) to ({best_move.to_loc.row}, {best_move.to_loc.col})")
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

    if len(board.active_players) == 1:
        print(f"Game over! Final scores: {board.player_points}")
