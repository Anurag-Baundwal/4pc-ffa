import random
import cProfile
from enum import Enum

class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6
    ONE_POINT_QUEEN = 7


class Player(Enum):
    RED = 0
    BLUE = 1
    YELLOW = 2
    GREEN = 3

class Piece:
    def __init__(self, player, piece_type):
        self.player = player
        self.piece_type = piece_type
        self.is_dead = False


class BoardLocation:
    def __init__(self, row, col):
        self.row = row
        self.col = col

class Move:
    def __init__(self, from_loc, to_loc, promotion_piece_type=None):
        self.from_loc = from_loc
        self.to_loc = to_loc
        self.promotion_piece_type = promotion_piece_type

class Board:
    def __init__(self):
        self.board = [[None] * 14 for _ in range(14)]
        self.active_players = set(Player)
        self.player_points = {player: 0 for player in Player}
        self.current_player = Player.RED
        self.setup_initial_board()

    def setup_initial_board(self):
        # Red pieces
        self.board[13][3] = Piece(Player.RED, PieceType.ROOK)
        self.board[13][4] = Piece(Player.RED, PieceType.KNIGHT)
        self.board[13][5] = Piece(Player.RED, PieceType.BISHOP)
        self.board[13][6] = Piece(Player.RED, PieceType.QUEEN)
        self.board[13][7] = Piece(Player.RED, PieceType.KING)
        self.board[13][8] = Piece(Player.RED, PieceType.BISHOP)
        self.board[13][9] = Piece(Player.RED, PieceType.KNIGHT)
        self.board[13][10] = Piece(Player.RED, PieceType.ROOK)
        for col in range(3, 11):
            self.board[12][col] = Piece(Player.RED, PieceType.PAWN)

        # Blue pieces
        self.board[3][0] = Piece(Player.BLUE, PieceType.ROOK)
        self.board[4][0] = Piece(Player.BLUE, PieceType.KNIGHT)
        self.board[5][0] = Piece(Player.BLUE, PieceType.BISHOP)
        self.board[6][0] = Piece(Player.BLUE, PieceType.QUEEN)
        self.board[7][0] = Piece(Player.BLUE, PieceType.KING)
        self.board[8][0] = Piece(Player.BLUE, PieceType.BISHOP)
        self.board[9][0] = Piece(Player.BLUE, PieceType.KNIGHT)
        self.board[10][0] = Piece(Player.BLUE, PieceType.ROOK)
        for row in range(3, 11):
            self.board[row][1] = Piece(Player.BLUE, PieceType.PAWN)

        # Yellow pieces
        self.board[0][10] = Piece(Player.YELLOW, PieceType.ROOK)
        self.board[0][9] = Piece(Player.YELLOW, PieceType.KNIGHT)
        self.board[0][8] = Piece(Player.YELLOW, PieceType.BISHOP)
        self.board[0][7] = Piece(Player.YELLOW, PieceType.QUEEN)
        self.board[0][6] = Piece(Player.YELLOW, PieceType.KING)
        self.board[0][5] = Piece(Player.YELLOW, PieceType.BISHOP)
        self.board[0][4] = Piece(Player.YELLOW, PieceType.KNIGHT)
        self.board[0][3] = Piece(Player.YELLOW, PieceType.ROOK)
        for col in range(3, 11):
            self.board[1][col] = Piece(Player.YELLOW, PieceType.PAWN)

        # Green pieces
        self.board[10][13] = Piece(Player.GREEN, PieceType.ROOK)
        self.board[9][13] = Piece(Player.GREEN, PieceType.KNIGHT)
        self.board[8][13] = Piece(Player.GREEN, PieceType.BISHOP)
        self.board[7][13] = Piece(Player.GREEN, PieceType.QUEEN)
        self.board[6][13] = Piece(Player.GREEN, PieceType.KING)
        self.board[5][13] = Piece(Player.GREEN, PieceType.BISHOP)
        self.board[4][13] = Piece(Player.GREEN, PieceType.KNIGHT)
        self.board[3][13] = Piece(Player.GREEN, PieceType.ROOK)
        for row in range(3, 11):
            self.board[row][12] = Piece(Player.GREEN, PieceType.PAWN)

    def is_valid_square(self, row, col):
        if not (0 <= row < 14 and 0 <= col < 14):
            return False
        if (row <= 2 and col <= 2) or (row <= 2 and col >= 11) or (row >= 11 and col <= 2) or (row >= 11 and col >= 11):
            return False
        return True
    # def get_legal_moves(self, player):
    #     legal_moves = []
    #     for row in range(14):
    #         for col in range(14):
    #             piece = self.board[row][col]
    #             if piece and piece.player == player:
    #                 if piece.piece_type == PieceType.PAWN:
    #                     legal_moves.extend(self.get_pawn_moves(row, col))
    #                 elif piece.piece_type == PieceType.KNIGHT:
    #                     legal_moves.extend(self.get_knight_moves(row, col))
    #                 elif piece.piece_type == PieceType.BISHOP:
    #                     legal_moves.extend(self.get_bishop_moves(row, col))
    #                 elif piece.piece_type == PieceType.ROOK:
    #                     legal_moves.extend(self.get_rook_moves(row, col))
    #                 elif piece.piece_type == PieceType.QUEEN or piece.piece_type == PieceType.ONE_POINT_QUEEN:
    #                     legal_moves.extend(self.get_queen_moves(row, col))
    #                 elif piece.piece_type == PieceType.KING:
    #                     legal_moves.extend(self.get_king_moves(row, col))

    #     # Filter out moves that would put the current player in check
    #     legal_moves = [move for move in legal_moves if not self.is_in_check(player, move)] ############ --------- problematic line
        
    #     return legal_moves
    
    def get_psuedo_legal_moves(self, player):
        psuedo_legal_moves = []
        for row in range(14):
            for col in range(14):
                piece = self.board[row][col]
                if piece and piece.player == player:
                    if piece.piece_type == PieceType.PAWN:
                        psuedo_legal_moves.extend(self.get_pawn_moves(row, col))
                    elif piece.piece_type == PieceType.KNIGHT:
                        psuedo_legal_moves.extend(self.get_knight_moves(row, col))
                    elif piece.piece_type == PieceType.BISHOP:
                        psuedo_legal_moves.extend(self.get_bishop_moves(row, col))
                    elif piece.piece_type == PieceType.ROOK:
                        psuedo_legal_moves.extend(self.get_rook_moves(row, col))
                    elif piece.piece_type == PieceType.QUEEN or piece.piece_type == PieceType.ONE_POINT_QUEEN:
                        psuedo_legal_moves.extend(self.get_queen_moves(row, col))
                    elif piece.piece_type == PieceType.KING:
                        psuedo_legal_moves.extend(self.get_king_moves(row, col))

        return psuedo_legal_moves
    
    def get_legal_moves(self, player):
        if player not in self.active_players:
            return None
        legal_moves = []

        psuedo_legal_moves = self.get_psuedo_legal_moves(player)
        
        for move in psuedo_legal_moves:
            captured_piece = self.make_psuedo_legal_move(move)
            if not self.is_in_check(player):
                legal_moves.append(move)
            self.undo_pseudo_legal_move(move, captured_piece)
        return legal_moves

    def get_pawn_moves(self, row, col):
        moves = []
        player = self.board[row][col].player

        # Forward moves
        if player == Player.RED:
            if row > 0 and self.board[row - 1][col] is None:
                moves.append(Move(BoardLocation(row, col), BoardLocation(row - 1, col)))
                if row == 12 and self.board[row - 2][col] is None:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row - 2, col)))
        elif player == Player.BLUE:
            if col < 13 and self.board[row][col + 1] is None:
                moves.append(Move(BoardLocation(row, col), BoardLocation(row, col + 1)))
                if col == 1 and self.board[row][col + 2] is None:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row, col + 2)))
        elif player == Player.YELLOW:
            if row < 13 and self.board[row + 1][col] is None:
                moves.append(Move(BoardLocation(row, col), BoardLocation(row + 1, col)))
                if row == 1 and self.board[row + 2][col] is None:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row + 2, col)))
        elif player == Player.GREEN:
            if col > 0 and self.board[row][col - 1] is None:
                moves.append(Move(BoardLocation(row, col), BoardLocation(row, col - 1)))
                if col == 12 and self.board[row][col - 2] is None:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row, col - 2)))

        # Capture moves
        match player:
            case Player.RED:
                if row > 0 and col > 0 and self.board[row - 1][col - 1] and self.board[row - 1][col - 1].player != player:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row - 1, col - 1)))
                if row > 0 and col < 13 and self.board[row - 1][col + 1] and self.board[row - 1][col + 1].player != player:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row - 1, col + 1)))
            case Player.BLUE:
                if row > 0 and col < 13 and self.board[row - 1][col + 1] and self.board[row - 1][col + 1].player != player:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row - 1, col + 1)))
                if row < 13 and col < 13 and self.board[row + 1][col + 1] and self.board[row + 1][col + 1].player != player:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row + 1, col + 1)))
            case Player.YELLOW:
                if row < 13 and col > 0 and self.board[row + 1][col - 1] and self.board[row + 1][col - 1].player != player:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row + 1, col - 1)))
                if row < 13 and col < 13 and self.board[row + 1][col + 1] and self.board[row + 1][col + 1].player != player:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row + 1, col + 1)))
            case Player.GREEN:
                if row > 0 and col > 0 and self.board[row - 1][col - 1] and self.board[row - 1][col - 1].player != player:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row - 1, col - 1)))
                if row < 13 and col > 0 and self.board[row + 1][col - 1] and self.board[row + 1][col - 1].player != player:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row + 1, col - 1)))

        # Promotion moves
        promotion_row = 5 if player == Player.RED else 8 if player == Player.BLUE else 8 if player == Player.YELLOW else 5
        if (player == Player.RED and row == promotion_row) or (player == Player.BLUE and col == promotion_row) or (player == Player.YELLOW and row == promotion_row) or (player == Player.GREEN and col == promotion_row):
            promotion_moves = []
            for move in moves:
                for piece_type in [PieceType.KNIGHT, PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN, PieceType.ONE_POINT_QUEEN]:
                    promotion_moves.append(Move(BoardLocation(move.from_loc.row, move.from_loc.col), BoardLocation(move.to_loc.row, move.to_loc.col), piece_type))
            moves.extend(promotion_moves)

        return moves

    def get_knight_moves(self, row, col):
        moves = []
        player = self.board[row][col].player
        for r, c in [(row-2, col-1), (row-2, col+1), (row-1, col-2), (row-1, col+2), (row+1, col-2), (row+1, col+2), (row+2, col-1), (row+2, col+1)]:
            # if 0 <= r < 14 and 0 <= c < 14 and (self.board[r][c] is None or self.board[r][c].player != player):
            if self.is_valid_square(r, c) and (self.board[r][c] is None or self.board[r][c].player != player):
                moves.append(Move(BoardLocation(row, col), BoardLocation(r, c)))
        return moves

    def get_bishop_moves(self, row, col):
        moves = []
        player = self.board[row][col].player
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            r, c = row + dr, col + dc
            while self.is_valid_square(r, c):
                if self.board[r][c] is None:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(r, c)))
                elif self.board[r][c].player != player:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(r, c)))
                    break
                else: #blocked by friendly piece
                    break
                r, c = r + dr, c + dc
        return moves

    def get_rook_moves(self, row, col):
        moves = []
        player = self.board[row][col].player
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            while self.is_valid_square(r, c):
                if self.board[r][c] is None:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(r, c)))
                elif self.board[r][c].player != player:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(r, c)))
                    break
                else:
                    break
                r, c = r + dr, c + dc
        return moves

    def get_queen_moves(self, row, col):
        return self.get_bishop_moves(row, col) + self.get_rook_moves(row, col)

    def get_king_moves(self, row, col):
        moves = []
        player = self.board[row][col].player
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if self.is_valid_square(r, c) and (self.board[r][c] is None or self.board[r][c].player != player):
                    moves.append(Move(BoardLocation(row, col), BoardLocation(r, c)))
        # TODO: Add castling moves
        return moves

    def make_move(self, move):
        #print(move)
        eliminated_players = []

        piece = self.board[move.from_loc.row][move.from_loc.col]
        self.board[move.from_loc.row][move.from_loc.col] = None ###################################
        captured_piece = self.board[move.to_loc.row][move.to_loc.col]
        captured_player = captured_piece.player if captured_piece else None

        if captured_piece and not captured_piece.is_dead:
            captured_player = captured_piece.player
            self.player_points[piece.player] += self.get_piece_capture_value(captured_piece)
        self.board[move.to_loc.row][move.to_loc.col] = piece
        if move.promotion_piece_type:
            self.board[move.to_loc.row][move.to_loc.col].piece_type = move.promotion_piece_type

        # Check for checkmate and stalemate
        #print("Checking if anyone is checkmated or stalemated")
        #print(self.active_players)
        for player in self.active_players:
            #print(player)
            if self.is_checkmate(player):
                self.player_points[piece.player] += 20  # Checkmate points
                self.eliminate_player(player)
                eliminated_players.append(player)

                break # added break to fix bug 
            elif self.is_stalemate(player):
                if player == self.current_player:
                    self.player_points[player] += 20  # Stalemate points for current player
                else:
                    # Distribute stalemate points among remaining players
                    active_players = [p for p in self.active_players if p != player]
                    # stalemate_points = 20 // len(active_players)
                    if len(active_players) == 2: 
                        stalemate_points == 20
                    elif len(active_players) == 3: # 2 will be left -> 20/2 = 10
                        stalemate_points = 10
                    elif len(active_players) == 4: 
                        stalemate_points == 7
                    for p in active_players:
                        self.player_points[p] += stalemate_points
                self.eliminate_player(player)
                eliminated_players.append(player)
                break
            
                # will have to add double and triple checkmate support later
        # print("Current player: " + str(self.current_player))
        self.current_player = Player((self.current_player.value + 1) % 4)
        while (self.current_player not in self.active_players):
            self.current_player = Player((self.current_player.value + 1) % 4)
        # print("Current player after making move: " + str(self.current_player))
        # self.current_player = self.get_next_player()
        return captured_piece, eliminated_players
    
    def make_psuedo_legal_move(self, move):
        piece = self.board[move.from_loc.row][move.from_loc.col]
        self.board[move.from_loc.row][move.from_loc.col] = None
        captured_piece = self.board[move.to_loc.row][move.to_loc.col]
        
        self.board[move.to_loc.row][move.to_loc.col] = piece
        if move.promotion_piece_type:
            self.board[move.to_loc.row][move.to_loc.col].piece_type = move.promotion_piece_type

        return captured_piece

    def undo_pseudo_legal_move(self, move, captured_piece):
        piece = self.board[move.to_loc.row][move.to_loc.col]
        self.board[move.from_loc.row][move.from_loc.col] = piece
        self.board[move.to_loc.row][move.to_loc.col] = captured_piece
    
    def undo_move(self, move, captured_piece, eliminated_players):
        # print("Current player: " + str(self.current_player))
        piece = self.board[move.to_loc.row][move.to_loc.col]
        self.board[move.from_loc.row][move.from_loc.col] = self.board[move.to_loc.row][move.to_loc.col]
        self.board[move.to_loc.row][move.to_loc.col] = captured_piece
        if captured_piece:
            self.player_points[piece.player] -= self.get_piece_capture_value(captured_piece) #

        for player in eliminated_players:
            self.active_players.add(player)
            for row in range(14):
                for col in range(14):
                    piece1 = self.board[row][col]
                    if piece1 and piece1.player == player:
                        piece1.is_dead = False
            self.player_points[piece.player] -= 20  # Undo checkmate points
        
        self.current_player = Player((self.current_player.value - 1) % 4)
        while (self.current_player not in self.active_players):
            self.current_player = Player((self.current_player.value + 1) % 4)
        # print("Active players: " + str(board.active_players))
        # print("Current player after undoing move: " + str(self.current_player))

    def get_piece_value(self, piece):
        if piece.piece_type == PieceType.PAWN:
            return 1
        elif piece.piece_type == PieceType.KNIGHT:
            return 3
        elif piece.piece_type == PieceType.BISHOP:
            return 5
        elif piece.piece_type == PieceType.ROOK:
            return 5
        elif piece.piece_type == PieceType.QUEEN:
            return 9
        elif piece.piece_type == PieceType.ONE_POINT_QUEEN:
            return 11
        elif piece.piece_type == PieceType.KING:
            return 20
          
    def get_piece_capture_value(self, piece):
        if piece.piece_type == PieceType.PAWN:
            return 1
        elif piece.piece_type == PieceType.KNIGHT:
            return 3
        elif piece.piece_type == PieceType.BISHOP:
            return 5
        elif piece.piece_type == PieceType.ROOK:
            return 5
        elif piece.piece_type == PieceType.QUEEN:
            return 9
        elif piece.piece_type == PieceType.ONE_POINT_QUEEN:
              return 1
        elif piece.piece_type == PieceType.KING:
            return 20

    def evaluate(self):
        scores = {player: 0 for player in board.active_players}
        for row in range(14):
            for col in range(14):
                piece = self.board[row][col]
                if piece:
                    if not piece.is_dead and piece.player in board.active_players:
                      scores[piece.player] += self.get_piece_value(piece)
        for player in board.active_players:
            scores[player] += self.player_points[player]
            scores[player] -= 63
        
        return scores
    
    def get_next_player(self):
        next_player = Player((self.current_player.value + 1) % 4)
        while (next_player not in self.active_players):
            next_player = Player((next_player.value + 1) % 4)

    def is_game_over(self):
        return len(self.active_players) == 1 or all(self.is_checkmate(player) or self.is_stalemate(player) for player in self.active_players)
    
    # def is_in_check(self, player, move=None): # rename this?
    #     captured_piece = None

    #     # Make the move temporarily if provided 
    #     if move:
    #         captured_piece, eliminated_players = self.make_move(move) # PROBLEM HERE

    #     king_loc = None
    #     for row in range(14):
    #         for col in range(14):
    #             piece = self.board[row][col]
    #             if piece and piece.player == player and piece.piece_type == PieceType.KING:
    #                 king_loc = BoardLocation(row, col)
    #                 break
    #         if king_loc:
    #             break

    #     if king_loc:
    #         for opponent in Player:
    #             if opponent != player:
    #                 for opponent_move in self.get_psuedo_legal_moves(opponent):
    #                     if opponent_move.to_loc.row == king_loc.row and opponent_move.to_loc.col == king_loc.col:
    #                         # Undo the temporary move if provided
    #                         if move:
    #                             self.undo_move(move, captured_piece, eliminated_players)
    #                         return True

    #     # Undo the temporary move if provided
    #     if move:
    #         self.undo_move(move, captured_piece, eliminated_players)
    #     return False

    def is_in_check(self, player):
        king_loc = None
        for row in range(14):
            for col in range(14):
                piece = self.board[row][col]
                if piece and piece.player == player and piece.piece_type == PieceType.KING:
                    king_loc = BoardLocation(row, col)
                    break
            if king_loc:
                break

        if king_loc:
            for opponent in Player:
                if opponent != player:
                    for opponent_move in self.get_psuedo_legal_moves(opponent):
                        if opponent_move.to_loc.row == king_loc.row and opponent_move.to_loc.col == king_loc.col:
                              return True
            return False

    def is_checkmate(self, player):
        # print("Inside is_checkmate method")
        # print(self.is_in_check(player))
        # print(len(self.get_legal_moves(player)))
        return self.is_in_check(player) and len(self.get_legal_moves(player)) == 0

    def is_stalemate(self, player):
        return not self.is_in_check(player) and len(self.get_legal_moves(player)) == 0

    def eliminate_player(self, player):
        for row in range(14):
            for col in range(14):
                piece = self.board[row][col]
                if piece and piece.player == player:
                    piece.is_dead = True
        self.active_players.remove(player)

def negamax4(board, depth, player, alpha, beta):
    if depth == 0 or board.is_game_over():
        scores = board.evaluate()
        # print(scores)
        return scores

    max_scores = {p: float('-inf') for p in board.active_players}

    for move in board.get_legal_moves(board.current_player):
        captured_piece, eliminated_players = board.make_move(move)
        scores = negamax4(board, depth - 1, board.get_next_player(), alpha, beta)
        

        for p in board.active_players:
            max_scores[p] = max(max_scores[p], scores[p])

        if max_scores[board.current_player] >= beta:
            break

        alpha = max(alpha, max_scores[board.current_player])
        board.undo_move(move, captured_piece, eliminated_players)
    return max_scores

def get_best_move(board, depth):
    best_move = None
    max_score = float('-inf')
    best_scores = None
    alpha = float('-inf')
    beta = float('inf')

    for move in board.get_legal_moves(board.current_player):
        captured_piece, eliminated_players = board.make_move(move)
        scores = negamax4(board, depth - 1, board.get_next_player(), alpha, beta)
        

        # print("In get_best_move:")
        # print("Current player: "+ str(board.current_player))
        # print("Active players: " + str(board.active_players))
        # print(scores)
        if scores[board.current_player] > max_score:
            max_score = scores[board.current_player]
            best_move = move
            best_scores = scores

        alpha = max(alpha, max_score)
        board.undo_move(move, captured_piece, eliminated_players)
    return best_move, best_scores

if __name__ == '__main__':
    board = Board()
    #board.make_move(Move(BoardLocation(6, 0), BoardLocation(11, 3)))  # Blue queen(6, 0) to (11, 3)
    # See if it can spot mate in 1 -----------------------------------------------------------------------------------------------------
    board.make_move(Move(BoardLocation(12, 7), BoardLocation(11, 7))) # red pawn move ############ fix (13,7) and 12,7 to 12, 7 and 11,7
    board.make_move(Move(BoardLocation(10, 1), BoardLocation(10, 3))) # blue pawn move
    board.make_move(Move(BoardLocation(9, 1), BoardLocation(9, 2))) # blue pawn move
    board.make_move(Move(BoardLocation(1, 8), BoardLocation(2, 8))) # yellow pawn move
    board.make_move(Move(BoardLocation(13, 8), BoardLocation(11, 6))) # red bishop move
    board.current_player = Player.YELLOW
    # see if best move for red is to take the queen

    #cProfile.run('get_best_move(board, 1)', 'profile_results')
    
    # Calling get_best_move and looking at the output
    best_move, scores = get_best_move(board, 2) 
    if best_move:
        print(f"Best move: ({best_move.from_loc.row}, {best_move.from_loc.col}) to ({best_move.to_loc.row}, {best_move.to_loc.col}) ")
        print(f"Scores: {scores}")
    else:
        print("No valid moves found or game is over.")

    ########## TEST IF CHECKMATE IS BEING DETECTED ########
    board.make_move(Move(BoardLocation(0, 7), BoardLocation(5, 12)))
    print(board.active_players) # confirm that this move is checkmate
    # scores = board.evaluate()
    # print(scores)
    # print(board.player_points)
    ########################################################

    # print(board.active_players)
    # board.make_move(Move(BoardLocation(0, 7), BoardLocation(5, 12)))
    # print(board.active_players)
    ##  -----------------------------------------------------------------------------------------------------------------------

    # # while not board.is_game_over():
    # #print(f"Current player: {board.current_player}")
    # best_move = get_best_move(board, 4)
    # # board.make_move(best_move)
    # #print(f"Best move: ({best_move.from_loc.row}, {best_move.from_loc.col}) to ({best_move.to_loc.row}, {best_move.to_loc.col}) ")
    # #print(f"Scores: {board.evaluate()}")

    # #print(f"Game over! Final scores: {board.evaluate()}")


# TODO:
# Add FEN Parser
# Add function to convert moves to san and uci strings
# x Add check, checkmate, stalemate and resignation support
# x And support for dead pieces
# Count number of nodes visited during search and use that to calculate nps
# x Handle one point queens such that they contribute a 9 points to the score but only give one point when captured
# Modify is_checkmate -> requires modifying is_in_check and get_legal_moves -> need to generate attacks of all 4 colors and see if the other colors are attacking the square our king is on -> create get_attackers function?
# handle promotions in undo_move?
# NOTE: 
# Engine still needs a lot of testing