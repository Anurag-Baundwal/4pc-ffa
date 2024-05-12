from pieces import Player

nodes = 0

def get_nodes():
    return nodes

def max_4(board, root_player, depth, alpha, beta):
    global nodes
    nodes += 1
    
    if depth == 0 or board.is_game_over():
        return board.evaluate()

    if board.current_player == root_player:
        max_scores = {p: float('-inf') if p != root_player else float('-inf') for p in set(Player)}
    else:
        max_scores = {p: float('-inf') if p != root_player else float('inf') for p in set(Player)}

    player = board.current_player

    for move in board.get_psuedo_legal_moves(player):
        captured_piece, eliminated_players = board.make_move(move)
        scores = max_4(board, root_player, depth - 1, alpha, beta)
        board.undo_move(move, captured_piece, eliminated_players)
        if player == root_player:
            if scores[player] >= max_scores[player]:
                for p in Player:
                    max_scores[p] = scores[p]
                alpha = max(alpha, max_scores[root_player])
            if alpha >= beta:
                break
        else:
            if scores[root_player] <= max_scores[root_player]:
                for p in Player:
                    max_scores[p] = scores[p]
                beta = min(beta, max_scores[root_player])
            if beta <= alpha: 
                break
    return max_scores

def get_best_move(board, depth):
    best_move = None
    max_score = float('-inf')
    best_scores = None

    global nodes
    nodes = 0

    root_player = board.current_player
    print(root_player)

    for move in board.get_psuedo_legal_moves(board.current_player):
        captured_piece, eliminated_players = board.make_move(move)
        alpha = float('-inf')
        beta = float('inf')
        scores = max_4(board, root_player, depth - 1, alpha, beta)

        if scores[root_player] > max_score:
            max_score = scores[root_player]
            best_move = move
            best_scores = scores

        board.undo_move(move, captured_piece, eliminated_players)

    return best_move, best_scores