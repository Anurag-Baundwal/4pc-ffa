import math
import random

def normalize_score(score):
        return 2 / (1 + math.exp(-score / 100)) - 1

class MCTSNode:
    def __init__(self, board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.children = []
        self.score = 0
        self.min_score = float('inf') # use 0 instead ?
        self.visits = 0
        self.untried_moves = board.get_psuedo_legal_moves(board.current_player)

    def select_child(self):
        # Applying the modified UCB1 formula to select the best child
        from math import log, sqrt
        log_parent_visits = log(self.visits)
        best_score = -float('inf')
        best_child = None
        for child in self.children:
            # Modified UCB1 calculation
            if child.visits == 0:
                # If a child node has not been visited yet, assign it a high priority
                ucb1 = float('inf')
            else:
                avg_score = normalize_score(child.score / child.visits)
                min_score = normalize_score(child.min_score)
                # weighted_score = 0.5 * avg_score + 0.5 * min_score
                weighted_score = 0.0 * avg_score + 1.0 * min_score  # Adjust weights
                exploration_term = 0.4 * sqrt(log_parent_visits / child.visits)
                ucb1 = weighted_score + exploration_term
            if ucb1 > best_score:
                best_score = ucb1
                best_child = child
        return best_child

    def expand(self):
        # Expand a random untried move
        move = random.choice(self.untried_moves)
        self.untried_moves.remove(move)
        new_board = self.board.copy()  
        new_board.make_move(move) 
        new_node = MCTSNode(new_board, self, move)
        self.children.append(new_node)
        return new_node

    def simulate(self, depth):
        # Randomly play out the game from this state
        sim_board = self.board.copy()
        current_depth = 0

        while current_depth < depth and not sim_board.is_game_over():
            possible_moves = sim_board.get_psuedo_legal_moves(sim_board.current_player)
            if not possible_moves:
                # Handle the case when there are no valid moves
                # You can either terminate the simulation or take an appropriate action
                # TODO: print the board and see what kind of position it is that there is a player who's in the active players and it's their turn but they have no moves, even psuedo legal moves.
                break
            move = random.choice(possible_moves)
            sim_board.make_move(move)
        scores = sim_board.evaluate()
        # scores = sim_board.player_points
        # Assuming self.board.current_player gives the current root player for the node #
        return scores


    def backpropagate(self, result):
        # Update current node and propagate back to the root node
        self.visits += 1
        root_player = self.board.current_player
        if abs(result[root_player]-(-999)) < 100:  # Handle the case when the simulation resulted in checkmate (score close to -999)
            self.score = -999
            self.min_score = -999
        else:
            self.score += result[root_player]  # Accumulate the score of the root player
            self.min_score = min(self.min_score, result[root_player])  # Update the minimum score

        if self.parent:
            self.parent.backpropagate(result)

    def best_move(self):
        best_score = -float('inf')
        best_node = None

        for child in self.children:
            if child.visits > 0:
                avg_score = child.score / child.visits  # Renamed from child.wins
                if avg_score > best_score:
                    best_score = avg_score
                    best_node = child
        return best_node.move if best_node else None


def MCTS(root, iterations, simulation_depth):
    for i in range(iterations):
        node = root

        # Selection
        while node.untried_moves == [] and node.children != []:
            node = node.select_child()

        # Expansion
        if node.untried_moves != []:
            node = node.expand()

        # Simulation
        result = node.simulate(simulation_depth)

        # Backpropagation
        node.backpropagate(result)

# Usage
# initial_board = ... # Your initial board setup
# root_node = MCTSNode(initial_board)
# MCTS(root_node, 1000)
# best_move = root_node.best_move()  # Implement best_move method based on highest win ratio among root children
