import random
import cProfile
from enum import Enum
import time

nodes = 0

class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6
    ONE_POINT_QUEEN = 7
    #RANDO_ZOMBIE_KING = 8


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
        #self.resigned_players = []
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

    # ((0 <= r < 14 and 0 <= c < 14) and not ((r <= 2 and c <= 2) or (r <= 2 and c >= 11) or (r >= 11 and c <= 2) or (r >= 11 and c >= 11)))
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
                    match piece.piece_type:
                        case PieceType.PAWN:
                            psuedo_legal_moves.extend(self.get_pawn_moves(row, col))
                        case PieceType.KNIGHT:
                            psuedo_legal_moves.extend(self.get_knight_moves(row, col))
                        case PieceType.BISHOP:
                            psuedo_legal_moves.extend(self.get_bishop_moves(row, col))
                        case PieceType.ROOK:
                            psuedo_legal_moves.extend(self.get_rook_moves(row, col))
                        case PieceType.QUEEN | PieceType.ONE_POINT_QUEEN:
                            psuedo_legal_moves.extend(self.get_queen_moves(row, col))
                        case PieceType.KING:
                            psuedo_legal_moves.extend(self.get_king_moves(row, col))

        return psuedo_legal_moves

    def get_attacks(self, player): # attacking moves: psuedo legal moves but forward pawn moves don't count
        attacks = []

        for row in range(14):
            for col in range(14):
                piece = self.board[row][col]
                if piece and piece.player == player:
                    match piece.piece_type:
                        case PieceType.PAWN:
                            # Capture moves
                            match player:
                                case Player.RED:
                                    if row > 0 and col > 0 and self.board[row - 1][col - 1] and self.board[row - 1][col - 1].player != player:
                                        attacks.append(Move(BoardLocation(row, col), BoardLocation(row - 1, col - 1)))
                                    if row > 0 and col < 13 and self.board[row - 1][col + 1] and self.board[row - 1][col + 1].player != player:
                                        attacks.append(Move(BoardLocation(row, col), BoardLocation(row - 1, col + 1)))
                                case Player.BLUE:
                                    if row > 0 and col < 13 and self.board[row - 1][col + 1] and self.board[row - 1][col + 1].player != player:
                                        attacks.append(Move(BoardLocation(row, col), BoardLocation(row - 1, col + 1)))
                                    if row < 13 and col < 13 and self.board[row + 1][col + 1] and self.board[row + 1][col + 1].player != player:
                                        attacks.append(Move(BoardLocation(row, col), BoardLocation(row + 1, col + 1)))
                                case Player.YELLOW:
                                    if row < 13 and col > 0 and self.board[row + 1][col - 1] and self.board[row + 1][col - 1].player != player:
                                        attacks.append(Move(BoardLocation(row, col), BoardLocation(row + 1, col - 1)))
                                    if row < 13 and col < 13 and self.board[row + 1][col + 1] and self.board[row + 1][col + 1].player != player:
                                        attacks.append(Move(BoardLocation(row, col), BoardLocation(row + 1, col + 1)))
                                case Player.GREEN:
                                    if row > 0 and col > 0 and self.board[row - 1][col - 1] and self.board[row - 1][col - 1].player != player:
                                        attacks.append(Move(BoardLocation(row, col), BoardLocation(row - 1, col - 1)))
                                    if row < 13 and col > 0 and self.board[row + 1][col - 1] and self.board[row + 1][col - 1].player != player:
                                        attacks.append(Move(BoardLocation(row, col), BoardLocation(row + 1, col - 1)))
                        case PieceType.KNIGHT:
                            attacks.extend(self.get_knight_moves(row, col))
                        case PieceType.BISHOP:
                            attacks.extend(self.get_bishop_moves(row, col))
                        case PieceType.ROOK:
                            attacks.extend(self.get_rook_moves(row, col))
                        case PieceType.QUEEN | PieceType.ONE_POINT_QUEEN:
                            attacks.extend(self.get_queen_moves(row, col))
                        case PieceType.KING:
                            attacks.extend(self.get_king_moves(row, col))

        return attacks

    def get_legal_moves(self, player):
        if player not in self.active_players:
            return None # change to empty list?
        legal_moves = []

        psuedo_legal_moves = self.get_psuedo_legal_moves(player)

        for move in psuedo_legal_moves:
            captured_piece = self.make_psuedo_legal_move(move) # might have some bugs since we're making a psuedo legal move ##################################################################################################################
            if not self.is_in_check(player):
                legal_moves.append(move)
            self.undo_pseudo_legal_move(move, captured_piece)
        return legal_moves

    def get_pawn_moves(self, row, col):
        moves = []
        player = self.board[row][col].player

        match player:
            case Player.RED:
                if row > 0 and self.board[row - 1][col] is None:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row - 1, col)))
                    if row == 12 and self.board[row - 2][col] is None:
                        moves.append(Move(BoardLocation(row, col), BoardLocation(row - 2, col)))
            case Player.BLUE:
                if col < 13 and self.board[row][col + 1] is None:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row, col + 1)))
                    if col == 1 and self.board[row][col + 2] is None:
                        moves.append(Move(BoardLocation(row, col), BoardLocation(row, col + 2)))
            case Player.YELLOW:
                if row < 13 and self.board[row + 1][col] is None:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row + 1, col)))
                    if row == 1 and self.board[row + 2][col] is None:
                        moves.append(Move(BoardLocation(row, col), BoardLocation(row + 2, col)))
            case Player.GREEN:
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
            if ((0 <= r < 14 and 0 <= c < 14) and not ((r <= 2 and c <= 2) or (r <= 2 and c >= 11) or (r >= 11 and c <= 2) or (r >= 11 and c >= 11))) and (self.board[r][c] is None or self.board[r][c].player != player):
                moves.append(Move(BoardLocation(row, col), BoardLocation(r, c)))
        return moves

    def get_bishop_moves(self, row, col):
        moves = []
        player = self.board[row][col].player
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            r, c = row + dr, col + dc
            while ((0 <= r < 14 and 0 <= c < 14) and not ((r <= 2 and c <= 2) or (r <= 2 and c >= 11) or (r >= 11 and c <= 2) or (r >= 11 and c >= 11))):
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
            while ((0 <= r < 14 and 0 <= c < 14) and not ((r <= 2 and c <= 2) or (r <= 2 and c >= 11) or (r >= 11 and c <= 2) or (r >= 11 and c >= 11))):
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
                if ((0 <= r < 14 and 0 <= c < 14) and not ((r <= 2 and c <= 2) or (r <= 2 and c >= 11) or (r >= 11 and c <= 2) or (r >= 11 and c >= 11))) and (self.board[r][c] is None or self.board[r][c].player != player):
                    moves.append(Move(BoardLocation(row, col), BoardLocation(r, c)))
        # TODO: Add castling moves
        return moves

    def make_move(self, move):
        # print(f"Do move: ({move.from_loc.row}, {move.from_loc.col}) to ({move.to_loc.row}, {move.to_loc.col})")
        eliminated_players = []

        piece = self.board[move.from_loc.row][move.from_loc.col]
        # print(f"Which piece is moving: {piece}")
        # print(f"Which piece is moving: {piece.player} {piece.piece_type}")
        self.board[move.from_loc.row][move.from_loc.col] = None ###################################
        captured_piece = self.board[move.to_loc.row][move.to_loc.col]
        # print(f"Which piece got captured: ", end ="")
        # if captured_piece is not None:
        #     print(f"{captured_piece}")
        # else:
        #     print("None.")
        # print(f"Which piece got captured: ", end = "")
        # if captured_piece is not None:
        #     print(f"{captured_piece.player} {captured_piece.piece_type}")
        # else:
        #     print("None.")
        captured_player = captured_piece.player if captured_piece else None

        if captured_piece and not captured_piece.is_dead: # and not captured piece is dead - points are only given when the piece did not belong to a dead player
            captured_player = captured_piece.player
            # print(f"Giving points to {piece.player} for capturing piece: {self.get_piece_capture_value(captured_piece)} points")
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
                # print(f"{player} got checkmated by this move")
                # print(f"Giving points to {piece.player} for checkmatng them: 20 points")

                self.player_points[piece.player] += 20  # Checkmate points
                self.eliminate_player(player)
                eliminated_players.append(player)

                break # added break to fix bug
            elif self.is_stalemate(player):
                #print(str(player) + " stalemated")
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
                self.eliminate_player(player) # TODO: Split eliminate_player method into two - one for checkmate and one for stalemate?
                eliminated_players.append(player)
                break

                # will have to add double and triple checkmate support later
        # print("Updating current player......")
        # print("Current player: " + str(self.current_player) + "value: " + str(self.current_player.value))
        self.current_player = Player((self.current_player.value + 1) % 4)
        # print("Current player: " + str(self.current_player) + "value: " + str(self.current_player.value))
        while (self.current_player not in self.active_players):
            self.current_player = Player((self.current_player.value + 1) % 4)
            # print("Current player: " + str(self.current_player) + "value: " + str(self.current_player.value))
        # print("Current player: " + str(self.current_player) + "value: " + str(self.current_player.value))
        # print("Done updating current player.....")
        # print("Current player after making move: " + str(self.current_player))
        # self.current_player = self.get_next_player()
        # print(f"Finished doing move. Captured piece: {captured_piece}. Eliminated players {eliminated_players}")
        return captured_piece, eliminated_players

    def make_psuedo_legal_move(self, move): # might need work ################################################################################
        # check where it's being used
        piece = self.board[move.from_loc.row][move.from_loc.col]
        self.board[move.from_loc.row][move.from_loc.col] = None
        captured_piece = self.board[move.to_loc.row][move.to_loc.col]

        self.board[move.to_loc.row][move.to_loc.col] = piece
        if move.promotion_piece_type:
            self.board[move.to_loc.row][move.to_loc.col].piece_type = move.promotion_piece_type

        return captured_piece

    def undo_pseudo_legal_move(self, move, captured_piece): # might need work ######################################################
        # check where it's being used
        piece = self.board[move.to_loc.row][move.to_loc.col]
        self.board[move.from_loc.row][move.from_loc.col] = piece
        self.board[move.to_loc.row][move.to_loc.col] = captured_piece

    def undo_move(self, move, captured_piece, eliminated_players): # take points change parameter?
        # print("Current player: " + str(self.current_player))
        # print(f"Undo move: ({move.from_loc.row}, {move.from_loc.col}) to ({move.to_loc.row}, {move.to_loc.col})")
        # print(f"Info received from aruments: captured piece {captured_piece}, eliminated players: {eliminated_players}")
        piece = self.board[move.to_loc.row][move.to_loc.col]
        # print(f"Piece {piece} moved to ({move.to_loc.row}, {move.to_loc.col}). Going to undo this.")
        self.board[move.from_loc.row][move.from_loc.col] = self.board[move.to_loc.row][move.to_loc.col]
        # print(f"Piece {piece} moved back to ({move.from_loc.row}, {move.from_loc.col}).")
        self.board[move.to_loc.row][move.to_loc.col] = captured_piece
        # print(f"Captured piece {captured_piece} put back at ({move.to_loc.row}, {move.to_loc.col})")
        if captured_piece and ((not captured_piece.is_dead) or captured_piece.player in eliminated_players): # points are deducted regardless of whether the piece was dead or not
            # print("undo piece capture")
            # print points?
            # print(f"Deducting points from {piece.player}: {self.get_piece_capture_value(captured_piece)} points. ")
            self.player_points[piece.player] -= self.get_piece_capture_value(captured_piece) #
            # print points?

        #print(f"SIDE TO MOVE BEFORE UNDOING MOVE: {self.current_player}") # RED
        #print #### active players
        self.current_player = Player((self.current_player.value - 1) % 4)
        while (self.current_player not in self.active_players):
            self.current_player = Player((self.current_player.value - 1) % 4)
        #print(f"SIDE TO MOVE BEFORE UNDOING MOVE: {self.current_player}") # GREEN # BUG

        for player in eliminated_players:
            self.active_players.add(player)
            self.player_points[player] += 9999 ### should work but needs testing # BUG: Needs different behaviour for undoing stalemate (probably -20 points instead of +9999 ?)
            for row in range(14):
                for col in range(14):
                    piece1 = self.board[row][col]
                    if piece1 and piece1.player == player:
                        piece1.is_dead = False
            # print(f"Deducting points from {piece.player}: 20 points")
            self.player_points[piece.player] -= 20  # Undo checkmate points ##########--------------------------------------------

        # print("Move undone successfully\n")
        # print("Active players: " + str(board.active_players))
        # print("Current player after undoing move: " + str(self.current_player))

    def get_piece_value(self, piece):
        match piece.piece_type:
            case PieceType.PAWN:
                return 1
            case PieceType.KNIGHT:
                return 3
            case PieceType.BISHOP:
                return 5
            case PieceType.ROOK:
                return 5
            case PieceType.QUEEN:
                return 9
            case PieceType.ONE_POINT_QUEEN:
                return 11
            case PieceType.KING:
                return 20

    def get_piece_capture_value(self, piece):
        match piece.piece_type:
            case PieceType.PAWN:
                return 1
            case PieceType.KNIGHT:
                return 3
            case PieceType.BISHOP:
                return 5
            case PieceType.ROOK:
                return 5
            case PieceType.QUEEN:
                return 9
            case PieceType.ONE_POINT_QUEEN:
                return 1
            case PieceType.KING:
                return 20
    # def evaluate(self):
    #     scores = {player: 0 for player in board.active_players}
    #     for row in range(14):
    #         for col in range(14):
    #             piece = self.board[row][col]
    #             if piece:
    #                 if not piece.is_dead and piece.player in board.active_players:
    #                   scores[piece.player] += self.get_piece_value(piece)
    #     #print("Inside evaluate method:")
    #     #print("   Material scores: ", scores)
    #     #print("   Points: ", self.player_points)
    #     for player in board.active_players:
    #         scores[player] += self.player_points[player]
    #         scores[player] -= 63

    #     return scores

    def evaluate(self):
        # scores = {player: 0 for player in board.active_players}
        scores = {player: 0 for player in Player}
        for row in range(14):
            for col in range(14):
                piece = self.board[row][col]
                if piece:
                    if not piece.is_dead and piece.player in board.active_players:
                      scores[piece.player] += self.get_piece_value(piece)
        
        #print("Inside evaluate method:")
        #print("   Material scores: ", scores)
        #print("   Points: ", self.player_points)

        # for player in board.active_players:
        for player in Player:
            scores[player] += self.player_points[player]
            scores[player] -= 63
            # if self.is_checkmate(player):
            #     scores[player] = float('-inf')
            # no need for this^ .. already handled .. checkmated player gets -9999 points

        return scores

    def get_next_player(self):
        next_player = Player((self.current_player.value + 1) % 4)
        while (next_player not in self.active_players):
            next_player = Player((next_player.value + 1) % 4)

    def is_game_over(self):
        # return len(self.active_players) == 1 or all(self.is_checkmate(player) or self.is_stalemate(player) for player in self.active_players)
        return len(self.active_players) == 1

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
                    for opponent_move in self.get_attacks(opponent):
                        if opponent_move.to_loc.row == king_loc.row and opponent_move.to_loc.col == king_loc.col:
                              return True
            return False

    def is_checkmate(self, player):
        # print("Inside is_checkmate method")
        # print(self.is_in_check(player))
        # print(len(self.get_legal_moves(player)))
        # return self.is_in_check(player) and len(self.get_legal_moves(player)) == 0
        return self.is_in_check(player) and (self.get_legal_moves(player) == None or len(self.get_legal_moves(player)) == 0 )

    def is_stalemate(self, player):
        return not self.is_in_check(player) and len(self.get_legal_moves(player)) == 0

    def eliminate_player(self, player):
        for row in range(14):
            for col in range(14):
                piece = self.board[row][col]
                if piece and piece.player == player:
                    piece.is_dead = True
        self.active_players.remove(player)
        self.player_points[player] -= 9999 # subtracting 9999 instead of setting it as -9999 so that we can easily undo this by adding 9999 points
        # BUG: This will deduct -9999 points in case of stalemate as well? In that case I think we should add 20 points instead of deducting 9999

    # def resign(self, player): # PROBABLY NEEDS MORE WORK
    #     if self.current_player == player: # can only resign when it's their turn
    #         self.resigned_players.append(player)
    #         self.active_players.remove(player)
    #         for row in range(14):
    #             for col in range(14):
    #                 piece = self.board[row][col]
    #                 if piece:
    #                     if not piece.is_dead and piece.player == player:
    #                       if piece.piece_type != PieceType.KING:
    #                           piece.is_dead = True
    #                       else:
    #                           piece.piece_type = PieceType.RANDO_ZOMBIE_KING
    def print_board(self):
        print("      a      b      c      d      e      f      g      h      i      j      k      l      m      n")
        print("      0      1      2      3      4      5      6      7      8      9      10     11     12     13")
        print("  +" + "------+" * 14)
        for row in range(14):
            print(f"{row:2d}|", end="")
            for col in range(14):
                if self.board[row][col] is None:
                    if self.is_valid_square(row, col):
                        print("      |", end="")
                    else:
                        print("      |", end="")
                else:
                    piece = self.board[row][col]
                    player = piece.player
                    piece_type = piece.piece_type
                    if player == Player.RED:
                        color = "r"
                    elif player == Player.BLUE:
                        color = "b"
                    elif player == Player.YELLOW:
                        color = "y"
                    else:  # Player.GREEN
                        color = "g"
                    if piece_type == PieceType.PAWN:
                        symbol = "p"
                    elif piece_type == PieceType.KNIGHT:
                        symbol = "N"
                    elif piece_type == PieceType.BISHOP:
                        symbol = "B"
                    elif piece_type == PieceType.ROOK:
                        symbol = "R"
                    elif piece_type == PieceType.QUEEN:
                        symbol = "Q"
                    elif piece_type == PieceType.KING:
                        symbol = "K"
                    else:  # PieceType.ONE_POINT_QUEEN
                        symbol = "1"
                    print(f"  {color}{symbol}  |", end="")
            print(f" {row:2d}")
            print("  +" + "------+" * 14)
        print("      a      b      c      d      e      f      g      h      i      j      k      l      m      n")
        print("      0      1      2      3      4      5      6      7      8      9      10     11     12     13")
        print("Side to mode: ", board.current_player)

    def print_board_2(self):
        # Red pieces
        red_king = "\033[31m♔\033[0m"
        red_queen = "\033[31m♕\033[0m"
        red_rook = "\033[31m♖\033[0m"
        red_bishop = "\033[31m♗\033[0m"
        red_knight = "\033[31m♘\033[0m"
        red_pawn = "\033[31m♙\033[0m"

        # Yellow pieces
        yellow_king = "\033[33m♔\033[0m"
        yellow_queen = "\033[33m♕\033[0m"
        yellow_rook = "\033[33m♖\033[0m"
        yellow_bishop = "\033[33m♗\033[0m"
        yellow_knight = "\033[33m♘\033[0m"
        yellow_pawn = "\033[33m♙\033[0m"

        # Blue pieces
        blue_king = "\033[34m♔\033[0m"
        blue_queen = "\033[34m♕\033[0m"
        blue_rook = "\033[34m♖\033[0m"
        blue_bishop = "\033[34m♗\033[0m"
        blue_knight = "\033[34m♘\033[0m"
        blue_pawn = "\033[34m♙\033[0m"

        # Green pieces
        green_king = "\033[32m♔\033[0m"
        green_queen = "\033[32m♕\033[0m"
        green_rook = "\033[32m♖\033[0m"
        green_bishop = "\033[32m♗\033[0m"
        green_knight = "\033[32m♘\033[0m"
        green_pawn = "\033[32m♙\033[0m"
        
        print("+---+---+"+ "---+" * 15 + "---+")
        # print("+   +   +"+ "---+" * 14 + "   +   +")

        print("|   |   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13" + "|   |   |")
        # print("        | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13" + "|        ")

        print("|---+---+" + "---+" * 15 + "---|")
        # print("+   +   +" + "---+" * 14 + "   +   +")

        print("|   |   | a | b | c | d | e | f | g | h | i | j | k | l | m | n " + "|   |   |")
        # print("        | a | b | c | d | e | f | g | h | i | j | k | l | m | n " + "|        ")
        
        print("|---+" + "---+" + "---+" * 15 + "---|")
        # print("+---+" + "---+" + "---+" * 15 + "---+")
        for row in range(14):
            print(f"|   | {row:2d}|", end="")
            for col in range(14):
                if self.board[row][col] is None:
                    if self.is_valid_square(row, col):
                        print("   |", end="")
                    else:
                        print("   |", end="")
                else:
                    piece = self.board[row][col]
                    player = piece.player
                    piece_type = piece.piece_type
                    if player == Player.RED:
                        if piece_type == PieceType.PAWN:
                            symbol = red_pawn
                        elif piece_type == PieceType.KNIGHT:
                            symbol = red_knight
                        elif piece_type == PieceType.BISHOP:
                            symbol = red_bishop
                        elif piece_type == PieceType.ROOK:
                            symbol = red_rook
                        elif piece_type == PieceType.QUEEN:
                            symbol = red_queen
                        elif piece_type == PieceType.KING:
                            symbol = red_king
                        else:  # PieceType.ONE_POINT_QUEEN
                            symbol = red_queen
                    elif player == Player.BLUE:
                        if piece_type == PieceType.PAWN:
                            symbol = blue_pawn
                        elif piece_type == PieceType.KNIGHT:
                            symbol = blue_knight
                        elif piece_type == PieceType.BISHOP:
                            symbol = blue_bishop
                        elif piece_type == PieceType.ROOK:
                            symbol = blue_rook
                        elif piece_type == PieceType.QUEEN:
                            symbol = blue_queen
                        elif piece_type == PieceType.KING:
                            symbol = blue_king
                        else:  # PieceType.ONE_POINT_QUEEN
                            symbol = blue_queen
                    elif player == Player.YELLOW:
                        if piece_type == PieceType.PAWN:
                            symbol = yellow_pawn
                        elif piece_type == PieceType.KNIGHT:
                            symbol = yellow_knight
                        elif piece_type == PieceType.BISHOP:
                            symbol = yellow_bishop
                        elif piece_type == PieceType.ROOK:
                            symbol = yellow_rook
                        elif piece_type == PieceType.QUEEN:
                            symbol = yellow_queen
                        elif piece_type == PieceType.KING:
                            symbol = yellow_king
                        else:  # PieceType.ONE_POINT_QUEEN
                            symbol = yellow_queen
                    else:  # Player.GREEN
                        if piece_type == PieceType.PAWN:
                            symbol = green_pawn
                        elif piece_type == PieceType.KNIGHT:
                            symbol = green_knight
                        elif piece_type == PieceType.BISHOP:
                            symbol = green_bishop
                        elif piece_type == PieceType.ROOK:
                            symbol = green_rook
                        elif piece_type == PieceType.QUEEN:
                            symbol = green_queen
                        elif piece_type == PieceType.KING:
                            symbol = green_king
                        else:  # PieceType.ONE_POINT_QUEEN
                            symbol = green_queen
                    print(f" {symbol} |", end="")
            print(f" {row:2d}"+"|   |")
            print("|---+---+" + "---+" * 15 + "---|")
        print("|   |   | a | b | c | d | e | f | g | h | i | j | k | l | m | n " + "|   |   |")
        print("|---+---+" + "---+" * 15 + "---|")
        print("|   |   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13" + "|   |   |")
        print("+---+---+" + "---+" * 15 + "---+")
        print("Side to move:", board.current_player)


    def print_board_3(self):
        # Red pieces
        red_king = "\033[31m♔\033[0m"
        red_queen = "\033[31m♕\033[0m"
        red_rook = "\033[31m♖\033[0m"
        red_bishop = "\033[31m♗\033[0m"
        red_knight = "\033[31m♘\033[0m"
        red_pawn = "\033[31m♙\033[0m"

        # Yellow pieces
        yellow_king = "\033[33m♔\033[0m"
        yellow_queen = "\033[33m♕\033[0m"
        yellow_rook = "\033[33m♖\033[0m"
        yellow_bishop = "\033[33m♗\033[0m"
        yellow_knight = "\033[33m♘\033[0m"
        yellow_pawn = "\033[33m♙\033[0m"

        # Blue pieces
        blue_king = "\033[34m♔\033[0m"
        blue_queen = "\033[34m♕\033[0m"
        blue_rook = "\033[34m♖\033[0m"
        blue_bishop = "\033[34m♗\033[0m"
        blue_knight = "\033[34m♘\033[0m"
        blue_pawn = "\033[34m♙\033[0m"

        # Green pieces
        green_king = "\033[32m♔\033[0m"
        green_queen = "\033[32m♕\033[0m"
        green_rook = "\033[32m♖\033[0m"
        green_bishop = "\033[32m♗\033[0m"
        green_knight = "\033[32m♘\033[0m"
        green_pawn = "\033[32m♙\033[0m"
        
        # print("+---+---+"+ "---+" * 15 + "---+")
        # print("+   +   +"+ "---+" * 14 + "   +   +")
        print("        +"+ "---+" * 14 + "        ")

        # print("|   |   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13" + "|   |   |")
        print("        | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13" + "|        ")

        # print("|---+---+" + "---+" * 15 + "---|")
        # print("+   +   +" + "---+" * 14 + "   +   +")
        print("        +"+ "---+" * 14 + "        ")

        # print("|   |   | a | b | c | d | e | f | g | h | i | j | k | l | m | n " + "|   |   |")
        print("        | a | b | c | d | e | f | g | h | i | j | k | l | m | n " + "|        ")
        
        # print("|---+" + "---+" + "---+" * 15 + "---|")
        print("+---+" + "---+" + "---+" * 15 + "---+")
        for row in range(14):
            print(f"|   | {row:2d}|", end="")
            for col in range(14):
                if row in [0, 1, 2, 11, 12, 13]:
                    # if col in [0, 1, 2, 11, 12, 13]:
                    #     print("    ", end="")
                    if col == 0 or col == 1 or col == 11 or col == 12:
                        print("    ", end="")
                    elif col == 2 or col == 13:
                        print("   |", end="")
                    else:
                        if self.board[row][col] is None:
                            if self.is_valid_square(row, col):
                                print("   |", end="")
                            else:
                                print("   |", end="")
                        else:
                            piece = self.board[row][col]
                            player = piece.player
                            piece_type = piece.piece_type
                            if player == Player.RED:
                                if piece_type == PieceType.PAWN:
                                    symbol = red_pawn
                                elif piece_type == PieceType.KNIGHT:
                                    symbol = red_knight
                                elif piece_type == PieceType.BISHOP:
                                    symbol = red_bishop
                                elif piece_type == PieceType.ROOK:
                                    symbol = red_rook
                                elif piece_type == PieceType.QUEEN:
                                    symbol = red_queen
                                elif piece_type == PieceType.KING:
                                    symbol = red_king
                                else:  # PieceType.ONE_POINT_QUEEN
                                    symbol = red_queen
                            elif player == Player.BLUE:
                                if piece_type == PieceType.PAWN:
                                    symbol = blue_pawn
                                elif piece_type == PieceType.KNIGHT:
                                    symbol = blue_knight
                                elif piece_type == PieceType.BISHOP:
                                    symbol = blue_bishop
                                elif piece_type == PieceType.ROOK:
                                    symbol = blue_rook
                                elif piece_type == PieceType.QUEEN:
                                    symbol = blue_queen
                                elif piece_type == PieceType.KING:
                                    symbol = blue_king
                                else:  # PieceType.ONE_POINT_QUEEN
                                    symbol = blue_queen
                            elif player == Player.YELLOW:
                                if piece_type == PieceType.PAWN:
                                    symbol = yellow_pawn
                                elif piece_type == PieceType.KNIGHT:
                                    symbol = yellow_knight
                                elif piece_type == PieceType.BISHOP:
                                    symbol = yellow_bishop
                                elif piece_type == PieceType.ROOK:
                                    symbol = yellow_rook
                                elif piece_type == PieceType.QUEEN:
                                    symbol = yellow_queen
                                elif piece_type == PieceType.KING:
                                    symbol = yellow_king
                                else:  # PieceType.ONE_POINT_QUEEN
                                    symbol = yellow_queen
                            else:  # Player.GREEN
                                if piece_type == PieceType.PAWN:
                                    symbol = green_pawn
                                elif piece_type == PieceType.KNIGHT:
                                    symbol = green_knight
                                elif piece_type == PieceType.BISHOP:
                                    symbol = green_bishop
                                elif piece_type == PieceType.ROOK:
                                    symbol = green_rook
                                elif piece_type == PieceType.QUEEN:
                                    symbol = green_queen
                                elif piece_type == PieceType.KING:
                                    symbol = green_king
                                else:  # PieceType.ONE_POINT_QUEEN
                                    symbol = green_queen
                            print(f" {symbol} |", end="")
                else:         
                    if self.board[row][col] is None:
                        if self.is_valid_square(row, col):
                            print("   |", end="")
                        else:
                            print("   |", end="")
                    else:
                        piece = self.board[row][col]
                        player = piece.player
                        piece_type = piece.piece_type
                        if player == Player.RED:
                            if piece_type == PieceType.PAWN:
                                symbol = red_pawn
                            elif piece_type == PieceType.KNIGHT:
                                symbol = red_knight
                            elif piece_type == PieceType.BISHOP:
                                symbol = red_bishop
                            elif piece_type == PieceType.ROOK:
                                symbol = red_rook
                            elif piece_type == PieceType.QUEEN:
                                symbol = red_queen
                            elif piece_type == PieceType.KING:
                                symbol = red_king
                            else:  # PieceType.ONE_POINT_QUEEN
                                symbol = red_queen
                        elif player == Player.BLUE:
                            if piece_type == PieceType.PAWN:
                                symbol = blue_pawn
                            elif piece_type == PieceType.KNIGHT:
                                symbol = blue_knight
                            elif piece_type == PieceType.BISHOP:
                                symbol = blue_bishop
                            elif piece_type == PieceType.ROOK:
                                symbol = blue_rook
                            elif piece_type == PieceType.QUEEN:
                                symbol = blue_queen
                            elif piece_type == PieceType.KING:
                                symbol = blue_king
                            else:  # PieceType.ONE_POINT_QUEEN
                                symbol = blue_queen
                        elif player == Player.YELLOW:
                            if piece_type == PieceType.PAWN:
                                symbol = yellow_pawn
                            elif piece_type == PieceType.KNIGHT:
                                symbol = yellow_knight
                            elif piece_type == PieceType.BISHOP:
                                symbol = yellow_bishop
                            elif piece_type == PieceType.ROOK:
                                symbol = yellow_rook
                            elif piece_type == PieceType.QUEEN:
                                symbol = yellow_queen
                            elif piece_type == PieceType.KING:
                                symbol = yellow_king
                            else:  # PieceType.ONE_POINT_QUEEN
                                symbol = yellow_queen
                        else:  # Player.GREEN
                            if piece_type == PieceType.PAWN:
                                symbol = green_pawn
                            elif piece_type == PieceType.KNIGHT:
                                symbol = green_knight
                            elif piece_type == PieceType.BISHOP:
                                symbol = green_bishop
                            elif piece_type == PieceType.ROOK:
                                symbol = green_rook
                            elif piece_type == PieceType.QUEEN:
                                symbol = green_queen
                            elif piece_type == PieceType.KING:
                                symbol = green_king
                            else:  # PieceType.ONE_POINT_QUEEN
                                symbol = green_queen
                        print(f" {symbol} |", end="")
            print(f" {row:2d}"+"|   |")
            if row in [0, 1, 11, 12]:
                print("|---+---+"+"           " +"+---+" +"---+" * 6 +"---+" + "           " +"+---+---|")
            else:
                print("+---+---+" + "---+" * 15 + "---+")
        # print("|   |   | a | b | c | d | e | f | g | h | i | j | k | l | m | n " + "|   |   |")
        print("        | a | b | c | d | e | f | g | h | i | j | k | l | m | n " + "|        ")

        # print("+---+---+"+ "---+" * 15 + "---+")
        # print("+   +   +"+ "---+" * 14 + "   +   +")
        print("        +"+ "---+" * 14 + "        ")

        # print("|   |   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13" + "|   |   |")
        print("        | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13" + "|        ")
        
        # print("+---+---+"+ "---+" * 15 + "---+")
        # print("+   +   +"+ "---+" * 14 + "   +   +")
        print("        +"+ "---+" * 14 + "        ")
        print("Side to move:", board.current_player)

    def print_board_4(self):
        # Note: Make sure to run "chcp 65001" in the terminal if the unicode characters are not being displayed properly

        # Red pieces
        red_king = "\033[31m♔\033[0m"
        red_queen = "\033[31m♕\033[0m"
        red_rook = "\033[31m♖\033[0m"
        red_bishop = "\033[31m♗\033[0m"
        red_knight = "\033[31m♘\033[0m"
        red_pawn = "\033[31m♙\033[0m"

        # Yellow pieces
        yellow_king = "\033[33m♔\033[0m"
        yellow_queen = "\033[33m♕\033[0m"
        yellow_rook = "\033[33m♖\033[0m"
        yellow_bishop = "\033[33m♗\033[0m"
        yellow_knight = "\033[33m♘\033[0m"
        yellow_pawn = "\033[33m♙\033[0m"

        # Blue pieces
        blue_king = "\033[34m♔\033[0m"
        blue_queen = "\033[34m♕\033[0m"
        blue_rook = "\033[34m♖\033[0m"
        blue_bishop = "\033[34m♗\033[0m"
        blue_knight = "\033[34m♘\033[0m"
        blue_pawn = "\033[34m♙\033[0m"

        # Green pieces
        green_king = "\033[32m♔\033[0m"
        green_queen = "\033[32m♕\033[0m"
        green_rook = "\033[32m♖\033[0m"
        green_bishop = "\033[32m♗\033[0m"
        green_knight = "\033[32m♘\033[0m"
        green_pawn = "\033[32m♙\033[0m"
        
        # Dead pieces
        dead_king = "♔"
        dead_queen = "♕"
        dead_rook = "♖"
        dead_bishop = "♗"
        dead_knight = "♘"
        dead_pawn = "♙"
        # print("+---+---+"+ "---+" * 15 + "---+")
        # print("+   +   +"+ "---+" * 14 + "   +   +")

        # print("|   |   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13" + "|   |   |")
        # print("        | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13" + "|        ")

        # print("|---+---+" + "---+" * 15 + "---|")
        # print("+   +   +" + "---+" * 14 + "   +   +")

        print("          a   b   c   d   e   f   g   h   i   j   k   l   m   n " + "         ")
        # print("        | a | b | c | d | e | f | g | h | i | j | k | l | m | n " + "|        ")
        
        # print("|---+" + "---+" + "---+" * 15 + "---|")
        # print("+---+" + "---+" + "---+" * 15 + "---+")
        print("     " + "   +" + "---+" * 14 + "        ")
        for row in range(14):
            print(f"      {row:2d}|", end="")
            for col in range(14):
                if self.board[row][col] is None:
                    if self.is_valid_square(row, col):
                        print("   |", end="")
                    else:
                        print("   |", end="")
                else:
                    piece = self.board[row][col]
                    player = piece.player
                    piece_type = piece.piece_type
                    is_dead = piece.is_dead
                    if not is_dead:
                        if player == Player.RED:
                            if piece_type == PieceType.PAWN:
                                symbol = red_pawn
                            elif piece_type == PieceType.KNIGHT:
                                symbol = red_knight
                            elif piece_type == PieceType.BISHOP:
                                symbol = red_bishop
                            elif piece_type == PieceType.ROOK:
                                symbol = red_rook
                            elif piece_type == PieceType.QUEEN:
                                symbol = red_queen
                            elif piece_type == PieceType.KING:
                                symbol = red_king
                            else:  # PieceType.ONE_POINT_QUEEN
                                symbol = red_queen
                        elif player == Player.BLUE:
                            if piece_type == PieceType.PAWN:
                                symbol = blue_pawn
                            elif piece_type == PieceType.KNIGHT:
                                symbol = blue_knight
                            elif piece_type == PieceType.BISHOP:
                                symbol = blue_bishop
                            elif piece_type == PieceType.ROOK:
                                symbol = blue_rook
                            elif piece_type == PieceType.QUEEN:
                                symbol = blue_queen
                            elif piece_type == PieceType.KING:
                                symbol = blue_king
                            else:  # PieceType.ONE_POINT_QUEEN
                                symbol = blue_queen
                        elif player == Player.YELLOW:
                            if piece_type == PieceType.PAWN:
                                symbol = yellow_pawn
                            elif piece_type == PieceType.KNIGHT:
                                symbol = yellow_knight
                            elif piece_type == PieceType.BISHOP:
                                symbol = yellow_bishop
                            elif piece_type == PieceType.ROOK:
                                symbol = yellow_rook
                            elif piece_type == PieceType.QUEEN:
                                symbol = yellow_queen
                            elif piece_type == PieceType.KING:
                                symbol = yellow_king
                            else:  # PieceType.ONE_POINT_QUEEN
                                symbol = yellow_queen
                        else:  # Player.GREEN
                            if piece_type == PieceType.PAWN:
                                symbol = green_pawn
                            elif piece_type == PieceType.KNIGHT:
                                symbol = green_knight
                            elif piece_type == PieceType.BISHOP:
                                symbol = green_bishop
                            elif piece_type == PieceType.ROOK:
                                symbol = green_rook
                            elif piece_type == PieceType.QUEEN:
                                symbol = green_queen
                            elif piece_type == PieceType.KING:
                                symbol = green_king
                            else:  # PieceType.ONE_POINT_QUEEN
                                symbol = green_queen
                    else:
                        if piece_type == PieceType.PAWN:
                                symbol = dead_pawn
                        elif piece_type == PieceType.KNIGHT:
                            symbol = dead_knight
                        elif piece_type == PieceType.BISHOP:
                            symbol = dead_bishop
                        elif piece_type == PieceType.ROOK:
                            symbol = dead_rook
                        elif piece_type == PieceType.QUEEN:
                            symbol = dead_queen
                        elif piece_type == PieceType.KING:
                            symbol = dead_king
                        else:  # PieceType.ONE_POINT_QUEEN
                            symbol = dead_queen
                    print(f" {symbol} |", end="")
            print(f" {row:2d}"+"     ")
            # print("|---+---+" + "---+" * 15 + "---|")
            print("        +" + "---+" * 14 + "        ")
        print("          a   b   c   d   e   f   g   h   i   j   k   l   m   n " + "         ")
        # print("|---+---+" + "---+" * 15 + "---|")
        # print("|   |   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13" + "|   |   |")
        # print("+---+---+" + "---+" * 15 + "---+")
        print("Side to move:", board.current_player)


def negamax4(board, depth): # add root player parameter? -> def negamax4(board, depth, root_player):
    global nodes
    nodes += 1
    if depth == 0 or board.is_game_over():
        #print("Running board.evaluate()")
        return board.evaluate()

    max_scores = {p: float('-inf') for p in board.active_players}
    player = board.current_player

    for move in board.get_legal_moves(player):
        captured_piece, eliminated_players = board.make_move(move)

        scores = negamax4(board, depth - 1)
        # Original implementation
        # for p in board.active_players:
        #     max_scores[p] = max(max_scores[p], scores[p])
        
        # New implementation
        if scores[player] > max_scores[player]:
            # for p in board.active_players: # BUG
            for p in Player: # fix
                max_scores[p] = scores[p] ## makes sense? or update something else instead of max_scores?

        board.undo_move(move, captured_piece, eliminated_players)

    return max_scores

def get_best_move(board, depth):
    best_move = None
    max_score = float('-inf')
    best_scores = None

    global nodes
    nodes = 0
    root_player = board.current_player
    for move in board.get_legal_moves(board.current_player):
        captured_piece, eliminated_players = board.make_move(move)
        scores = negamax4(board, depth - 1)
        # print("In get_best_move:")
        # print("Current player: "+ str(board.current_player))
        # print("Active players: " + str(board.active_players))
        # print(scores)

        # if scores[board.current_player] > max_score:
        #     max_score = scores[board.current_player]
        #     best_move = move
        #     best_scores = scores
        if scores[root_player] > max_score:
            max_score = scores[root_player]
            best_move = move
            best_scores = scores

        board.undo_move(move, captured_piece, eliminated_players)
    return best_move, best_scores

if __name__ == '__main__':
    board = Board()
    #board.make_move(Move(BoardLocation(6, 0), BoardLocation(11, 3)))  # Blue queen(6, 0) to (11, 3)

    # # Setting up the board such that yellow has mate in 1 on green
    board.make_move(Move(BoardLocation(12, 7), BoardLocation(11, 7))) # red pawn move ############ fix (13,7) and 12,7 to 12, 7 and 11,7
    board.make_move(Move(BoardLocation(10, 1), BoardLocation(10, 3))) # blue pawn move
    board.make_move(Move(BoardLocation(9, 1), BoardLocation(9, 2))) # blue pawn move
    board.make_move(Move(BoardLocation(1, 8), BoardLocation(2, 8))) # yellow pawn move
    board.make_move(Move(BoardLocation(13, 8), BoardLocation(11, 6))) # red bishop move
    # board.current_player = Player.YELLOW
    board.current_player = Player.GREEN

    # BUG: GREEN WON'T TRY TO STOP MATE IN 1
    # fixed with update to negamax4
    # if scores[player] > max_scores[player]:
    #         # for p in board.active_players: # BUG
    #         for p in Player: # fix
    #             max_scores[p] = scores[p] ## makes sense? or update something else instead of max_scores?

    ###################################
    # # check eval after mating green
    # board.make_move((Move(BoardLocation(0, 7), BoardLocation(5, 12)))) # yellow checkmates green
    # board.print_board_4()
    # print(board.evaluate())

    ##############################3

    # Setting up the board such that green's knight is hanging and red can take it
    # See if green will move the knight and stop red from taking it
    # board.make_move(Move(BoardLocation(12, 10), BoardLocation(11, 10))) # red pawn move
    # board.make_move(Move(BoardLocation(9, 13), BoardLocation(10, 11))) # Green knight move - hang it so that red can take it next turn
    # board.current_player = Player.GREEN

    # board.current_player = Player.GREEN
    

    # FOR TESTING MOVE GEN
    # player_to_generate_moves_for = board.current_player
    player_to_generate_moves_for = Player.GREEN ################################################## change back to board.current_player?
    board.current_player = player_to_generate_moves_for
    print ("Current state of the board: ")
    board.print_board_4()
    psuedo_legal_moves = board.get_psuedo_legal_moves(player_to_generate_moves_for)
    legal_moves = board.get_legal_moves(player_to_generate_moves_for)
    time.sleep(3)
    for i, move in enumerate(legal_moves):
        print(f"Move generated {i}: ({move.from_loc.row}, {move.from_loc.col}) to ({move.to_loc.row}, {move.to_loc.col}) ")
        print(f"Making move {i}")
        print(f"Scores: {board.evaluate}")
        print(f"Player points: {board.player_points}")
        captured_piece, eliminated_players = board.make_move(move)
        board.print_board_4()
        print(f"Turn: {board.current_player}")
        print(f"Active players: {board.active_players}\n")
        time.sleep(0.5)
        board.undo_move(move, captured_piece, eliminated_players)
        print(f"Undid move {i}")
        print(f"Scores: {board.evaluate()}")
        print(f"Player points: {board.player_points}")
        board.print_board_4()
        print(f"Turn: {board.current_player}")
        print(f"Active players: {board.active_players}")
        print(f"Player points: {board.player_points}\n")
        time.sleep(0.5)
    print(f"Total moves generated: psuedo_legal - {len(psuedo_legal_moves)}, legal - {len(legal_moves)}.")

    # PSUEDO LEGAL MOVES
    # psuedo_legal_moves =
    # for move in psuedo_legal_moves:
    #     print

    # FOR PROFILING
    # cProfile.run('get_best_move(board, 1)', 'profile_results') # Not good because we can't get the returned values

    def get_best_move_wrapper(board, depth):
        return get_best_move(board, depth)

    # Calling get_best_move and looking at the output
    # start_time = time.time() #########################################################################

    # PROFILING
    # # Profile the get_best_move_wrapper function
    # prof = cProfile.Profile()
    # globals_dict = globals().copy()
    # globals_dict['get_best_move_wrapper'] = get_best_move_wrapper
    # prof.runctx('result = get_best_move_wrapper(board, 2)', globals_dict, locals())
    # prof.dump_stats('profile_results')

    # # Retrieve the return values from the locals dictionary
    # best_move, scores = locals()['result']

    ######################################################################################################
    moves_to_play = 4 # how many moves do we want to play out
    for _ in range (moves_to_play):
        start_time = time.time()
        # best_move, scores = get_best_move(board, 2)
        best_move, scores = get_best_move(board, 4) # depth 3 search so that to see if red and yellow will mate green
        end_time = time.time()
        execution_time = end_time - start_time
        print("Search completed")
        print(f"Number of nodes visited: {nodes + 1}")
        print(f"Execution time for this search: {execution_time} seconds")
        nps = (nodes + 1) / execution_time
        print(f"Nodes per second (NPS): {nps}")
        if best_move:
            print(f"Best move: ({best_move.from_loc.row}, {best_move.from_loc.col}) to ({best_move.to_loc.row}, {best_move.to_loc.col}), Scores: {scores} ")
            # What happens if we play the best move
            board.make_move(best_move)
            print("Board state after playing best move: ")
            board.print_board_4()
            print("Turn: ", board.current_player)
            print("Active players: ", board.active_players)
            print("board.evaluate() output: ", board.evaluate(), "\n")
        else:
            print("No valid moves found or game is over. \n")
    ######################################################################################################


    ########## TEST IF CHECKMATE IS BEING DETECTED ########
    # board.make_move(Move(BoardLocation(0, 7), BoardLocation(5, 12)))
    # print(board.active_players) # confirm that this move is checkmate
    # scores = board.evaluate()
    # print(scores)
    # print(board.player_points)
    # print(board.current_player)
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
# x Add nps measurement

# TODO:
# Deduct points for being checkmated: -9999 points -> but add a second list of points to store their final score
#                                                   -> also add 9999 points when undoing move 
#                                                   -> update evaluate method to have scores of all players rather than just the active ones
# Add resignation support - turn king into zombie
# update methods print_board 1 2 3 to print eliminated pieces as white (already updated print_board_4)
# Be careful about dead pieces during move gen (even though checking whether the player is in the active_players already handles this)

# TODO:
# Handle points differently for stalemate case of elimination
# Fix promotion related stuff - make move, undo move - maybe points as well - might need to pass which piece we promoted to
# In negamax4 pass root player as an argument and search differently based on whether it's the root player's turn or opponent's turn - for example maybe search moves where opponents team up on the root player
# Find and fix bugs in search if any - so far: takes free stuff, moves pieces which are hanging, tries to avoid getting mated. so looking good

# TODO: Do a depth 4 search to see if green realizes that there's no way to stop red and yellow from mating him, and then see what green plays
# ^ line 1269

# TODO: 
# Iterative deepening
# pv line
# copy enhancements from sunfish

# NEW IDEA:
# A different type of search. Instead of searching turn by turn, performing three quick 2v2 searches each of depth 1 or 2 - one for root player vs each opp. Then prune moves that hang our pieces or get us mated. This helps avoid hanging our pieces without having to perform a depth 4 search. Then we can do a proper search, ie, turn by turn, to find combos against us and try and stop them.

# BUG or TODO: In search: when it's a dead player's turn, change player and add another ply to the search

# IDEA:
# Opponent models: when there an equilibrium point (many equally good *or roughly equally good moves (ie we expand the equilibrium)* for the opponents), pick the ones that deal the most damage to the root player

# TODO: Implement get_game_result() - checks if the game is over and then returns the players with the most points
# NOTE:
# Engine still needs a lot of testing