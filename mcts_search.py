import random

class MCTSNode:
    def __init__(self, board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = board.get_psuedo_legal_moves(board.current_player)

    def select_child(self):
        # Applying the UCB1 formula to select the best child
        from math import log, sqrt
        log_parent_visits = log(self.visits)
        best_score = -float('inf')
        best_child = None
        for child in self.children:
            # UCB1 calculation
            ucb1 = child.wins / child.visits + sqrt(2 * log_parent_visits / child.visits)
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

    def simulate(self):
        # Randomly play out the game from this state
        sim_board = self.board.copy()
        while not sim_board.is_game_over():
            possible_moves = sim_board.get_psuedo_legal_moves(sim_board.current_player)
            move = random.choice(possible_moves)
            sim_board.make_move(move)
        scores = sim_board.evaluate()
        # scores = sim_board.player_points
        # Assuming self.board.current_player gives the current root player for the node #
        return scores


    def backpropagate(self, result):
        # Update current node and propagate back to the root node
        self.visits += 1
        # Check if the root player's score is the highest
        if self.parent:  # Only non-root nodes should check their parents
            root_player = self.board.current_player
            if result[root_player] == max(result.values()):
                self.wins += 1
        if self.parent:
            self.parent.backpropagate(result)
    
    def best_move(self):
        best_win_ratio = -float('inf')
        best_node = None
        for child in self.children:
            if child.visits > 0:  # Ensure we avoid division by zero
                win_ratio = child.wins / child.visits
                if win_ratio > best_win_ratio:
                    best_win_ratio = win_ratio
                    best_node = child
        return best_node.move if best_node else None


def MCTS(root, iterations):
    for i in range(iterations):
        node = root
        # Selection
        while node.untried_moves == [] and node.children != []:
            node = node.select_child()
        # Expansion
        if node.untried_moves != []:
            node = node.expand()
        # Simulation
        result = node.simulate()
        # Backpropagation
        node.backpropagate(result)

# Usage
# initial_board = ... # Your initial board setup
# root_node = MCTSNode(initial_board)
# MCTS(root_node, 1000)
# best_move = root_node.best_move()  # Implement best_move method based on highest win ratio among root children
