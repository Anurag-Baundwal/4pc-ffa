# Derived from engine.py

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
    DEAD_KING = 9


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
        self.board = [[None] * 8 for _ in range(8)]
        self.active_players = set(Player)
        self.player_points = {player: 0 for player in Player}
        self.current_player = Player.RED
        #self.resigned_players = []
        self.setup_initial_board()

    def setup_initial_board(self):
        # Red pieces
        self.board[7][0] = Piece(Player.RED, PieceType.ROOK)
        self.board[7][1] = Piece(Player.RED, PieceType.KNIGHT)
        self.board[7][2] = Piece(Player.RED, PieceType.BISHOP)
        self.board[7][3] = Piece(Player.RED, PieceType.KING)
        for col in range(0, 4):
            self.board[6][col] = Piece(Player.RED, PieceType.PAWN)

        # Blue pieces
        self.board[0][0] = Piece(Player.BLUE, PieceType.ROOK)
        self.board[1][0] = Piece(Player.BLUE, PieceType.KNIGHT)
        self.board[2][0] = Piece(Player.BLUE, PieceType.BISHOP)
        self.board[3][0] = Piece(Player.BLUE, PieceType.KING)
        for row in range(0, 4):
            self.board[row][1] = Piece(Player.BLUE, PieceType.PAWN)

        # Yellow pieces
        self.board[0][7] = Piece(Player.YELLOW, PieceType.ROOK)
        self.board[0][6] = Piece(Player.YELLOW, PieceType.KNIGHT)
        self.board[0][5] = Piece(Player.YELLOW, PieceType.BISHOP)
        self.board[0][4] = Piece(Player.YELLOW, PieceType.KING)
        for col in range(4, 8):
            self.board[1][col] = Piece(Player.YELLOW, PieceType.PAWN)

        # Green pieces
        self.board[4][7] = Piece(Player.GREEN, PieceType.KING)
        self.board[5][7] = Piece(Player.GREEN, PieceType.BISHOP)
        self.board[6][7] = Piece(Player.GREEN, PieceType.KNIGHT)
        self.board[7][7] = Piece(Player.GREEN, PieceType.ROOK)
        for row in range(4, 8):
            self.board[row][6] = Piece(Player.GREEN, PieceType.PAWN)

    def is_valid_square(self, row, col):
        if not (0 <= row < 8 and 0 <= col < 8):
            return False
        return True

    def get_psuedo_legal_moves(self, player): # TODO: check if the player is dead?
        psuedo_legal_moves = []

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                # if piece and piece.player == player:
                if piece and piece.player == player and piece.is_dead == False:
                    match piece.piece_type:
                        case PieceType.PAWN:
                            psuedo_legal_moves.extend(self.get_pawn_moves(row, col))
                        case PieceType.KNIGHT:
                            psuedo_legal_moves.extend(self.get_knight_moves(row, col))
                        case PieceType.BISHOP:
                            psuedo_legal_moves.extend(self.get_bishop_moves(row, col))
                        case PieceType.ROOK:
                            psuedo_legal_moves.extend(self.get_rook_moves(row, col))
                        case PieceType.KING:
                            # psuedo_legal_moves.extend(self.get_king_moves(row, col))
                            psuedo_legal_moves = self.get_king_moves(row, col) + psuedo_legal_moves


        return psuedo_legal_moves

    def get_pawn_moves(self, row, col):
        moves = []
        player = self.board[row][col].player

        match player:
            case Player.RED:
                if row > 0 and self.board[row - 1][col] is None:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row - 1, col)))
            case Player.BLUE:
                if col < 7 and self.board[row][col + 1] is None:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row, col + 1)))
            case Player.YELLOW:
                if row < 7 and self.board[row + 1][col] is None:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row + 1, col)))
            case Player.GREEN:
                if col > 0 and self.board[row][col - 1] is None:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row, col - 1)))
                    
        # Capture moves
        match player:
            case Player.RED:
                if row > 0 and col > 0 and self.board[row - 1][col - 1] and self.board[row - 1][col - 1].player != player:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row - 1, col - 1)))
                if row > 0 and col < 7 and self.board[row - 1][col + 1] and self.board[row - 1][col + 1].player != player:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row - 1, col + 1)))
            case Player.BLUE:
                if row > 0 and col < 7 and self.board[row - 1][col + 1] and self.board[row - 1][col + 1].player != player:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row - 1, col + 1)))
                if row < 7 and col < 7 and self.board[row + 1][col + 1] and self.board[row + 1][col + 1].player != player:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row + 1, col + 1)))
            case Player.YELLOW:
                if row < 7 and col > 0 and self.board[row + 1][col - 1] and self.board[row + 1][col - 1].player != player:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row + 1, col - 1)))
                if row < 7 and col < 7 and self.board[row + 1][col + 1] and self.board[row + 1][col + 1].player != player:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row + 1, col + 1)))
            case Player.GREEN:
                if row > 0 and col > 0 and self.board[row - 1][col - 1] and self.board[row - 1][col - 1].player != player:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row - 1, col - 1)))
                if row < 7 and col > 0 and self.board[row + 1][col - 1] and self.board[row + 1][col - 1].player != player:
                    moves.append(Move(BoardLocation(row, col), BoardLocation(row + 1, col - 1)))

        # Promotion moves
        promotion_row = 7 if player == Player.RED else 7 if player == Player.BLUE else 0 if player == Player.YELLOW else 0
        if (player == Player.RED and row == promotion_row) or (player == Player.BLUE and col == promotion_row) or (player == Player.YELLOW and row == promotion_row) or (player == Player.GREEN and col == promotion_row):
            promotion_moves = []
            for move in moves:
                for piece_type in [PieceType.ROOK]:
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
                else: 
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
        return moves

    def make_move(self, move):
        eliminated_players = []

        piece = self.board[move.from_loc.row][move.from_loc.col]
        self.board[move.from_loc.row][move.from_loc.col] = None 
        captured_piece = self.board[move.to_loc.row][move.to_loc.col]
        captured_player = captured_piece.player if captured_piece else None

        # if captured_piece and (captured_piece.is_dead == False or captured_piece.piece_type == PieceType.DEAD_KING): ##### THIS IS NOT GIVING POINTS FOR CAPTURING DEAD KINGS BECAUSE is_dead is True # FIXED 
        if captured_piece and captured_piece.is_dead == False:
            captured_player = captured_piece.player
            self.player_points[piece.player] += self.get_piece_capture_value(captured_piece)

            if captured_piece.piece_type == PieceType.KING:
              # print(f"Inside make_move. {captured_player}'s king got captured. Captured by piece {piece.player} {piece.piece_type}. Board state: ")
              # self.print_board()
              self.eliminate_player(captured_player)
              eliminated_players.append(captured_player)
              
        self.board[move.to_loc.row][move.to_loc.col] = piece
        if move.promotion_piece_type:
            self.board[move.to_loc.row][move.to_loc.col].piece_type = move.promotion_piece_type

        # if len(self.active_players) != 1: ################ FIX it in undo move too? 
        #     self.current_player = Player((self.current_player.value + 1) % 4)
        #     while (self.current_player not in self.active_players):
        #         self.current_player = Player((self.current_player.value + 1) % 4)
        #     return captured_piece, eliminated_players
        # else: # BUG: In this case it returns none when it's supposed to return two things (captured piece, eliminated_players)
        #     print("Only one active player left")
        #     print(self.active_players)

        self.current_player = Player((self.current_player.value + 1) % 4)
        while (self.current_player not in self.active_players):
            self.current_player = Player((self.current_player.value + 1) % 4)
        return captured_piece, eliminated_players

    def undo_move(self, move, captured_piece, eliminated_players):
        piece = self.board[move.to_loc.row][move.to_loc.col]
        self.board[move.from_loc.row][move.from_loc.col] = self.board[move.to_loc.row][move.to_loc.col]
        self.board[move.to_loc.row][move.to_loc.col] = captured_piece
        # if captured_piece and ((not captured_piece.is_dead) or captured_piece.player in eliminated_players): 
        if captured_piece and (not captured_piece.is_dead):
            self.player_points[piece.player] -= self.get_piece_capture_value(captured_piece)

        # Adjusting turns needs to happen before adding back the eliminated players
        self.current_player = Player((self.current_player.value - 1) % 4)
        while (self.current_player not in self.active_players):
            self.current_player = Player((self.current_player.value - 1) % 4)

        # add revive player method? 
        # also adjust turn after reviving - or pass turn from make_move to undo_move
        for player in eliminated_players:
            self.active_players.add(player)

            for row in range(8):
                for col in range(8):
                    piece1 = self.board[row][col]
                    if piece1 and piece1.player == player:
                        piece1.is_dead = False
                        # self.board[row][col].is_dead = False
                        if piece1.piece_type == PieceType.DEAD_KING:
                            piece1.piece_type = PieceType.KING # new addition - handle the king as well - make it undead

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
                return 3
            case PieceType.DEAD_KING:
                return 0

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
                return 3
            case PieceType.DEAD_KING:
                return 3
    # eval ideas
    # for king -> +10 cp for every friendly piece adjancent to king and -10 for every enemy piece
    # for pawns -> bonus for moving forward towards promotion | blocked pawn penalty
    # for pieces -> small penalty for being on back rank
    def evaluate(self):
        scores = {player: 0 for player in Player}

        king_coords = {player: None for player in Player}
        coord_sums = {player: [0, 0] for player in Player}
        piece_counts = {player: 0 for player in Player}
        king_present = {player: False for player in Player}

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    coord_sums[piece.player][0] += row
                    coord_sums[piece.player][1] += col
                    piece_counts[piece.player] += 1
                    if not piece.is_dead and piece.player in self.active_players:
                      # scores[piece.player] += self.get_piece_value(piece) * 1.25 
                      scores[piece.player] += self.get_piece_value(piece)

                      if piece.piece_type == PieceType.KNIGHT or piece.piece_type == PieceType.BISHOP:
                          if ((piece.player == Player.RED and row == 7) # on back rank
                          or (piece.player == Player.YELLOW and row == 0)
                          or (piece.player == Player.GREEN and col == 7)
                          or (piece.player == Player.BLUE and col == 0)):
                              scores[piece.player] -= 0.4 # penalty for undeveloped pieces

                      
                      if piece.piece_type == PieceType.KING:
                          for dr in [-1, 0, 1]:
                              for dc in [-1, 0, 1]:
                                  if dr == 0 and dc == 0:
                                      continue
                                  r, c = row + dr, col + dc
                                  if self.is_valid_square(r, c) and (self.board[r][c] is not None):
                                      if self.board[r][c].player == piece.player:
                                          if self.board[r][c].piece_type == PieceType.PAWN:
                                              scores[piece.player] += 0.2 # king near friendly pawn
                                          else:
                                              scores[piece.player] += 0.05 # king near friendly piece
                                      else:
                                          if self.board[r][c].player not in self.active_players:
                                              scores[piece.player] += 0.15 # shelter from dead pieces
                                          else:
                                              scores[piece.player] -= 0.15 # king near enemy piece
                          # Store the coordinates of the king for each color
                          king_coords[piece.player] = [row, col]
                          
                          king_present[piece.player] = True
                          # if piece.player == Player.RED:
                          #     red_king_present = True
                          # elif piece.player == Player.BLUE:
                          #     blue_king_present = True
                          # elif piece.player == Player.YELLOW:
                          #     yellow_king_present = True
                          # elif piece.player == Player.GREEN:
                          #     green_king_present = True
                      if piece.piece_type == PieceType.PAWN:
                          if piece.player == Player.RED:
                              scores[piece.player] += 0.2*(6-row)
                              if self.board[row-1][col] != None and self.board[row-1][col].player != piece.player:
                                  scores[piece.player] -= 0.2 # blocked pawn
                              for dr in [-1]:
                                  for dc in [-1, 1]:
                                      r, c = row + dr, col + dc
                                      if self.is_valid_square(r, c):
                                          if self.board[row-1][col] != None:
                                              target = self.board[row-1][col]
                                              if target.player == piece.player:
                                                  if target.piece_type == PieceType.BISHOP or target.piece_type == PieceType.KNIGHT:
                                                      scores[piece.player] += 0.2 # piece on outpost
                                              else:
                                                  scores[piece.player] += 0.2 # attacking enemy piece
                                                  if target.piece_type == PieceType.KING:
                                                      scores[piece.player] += 0.1 # attacking enemy king
                                                      scores[target.player] -= 0.5 # king in danger - avoid getting attacked by enemy pawns
                          elif piece.player == Player.BLUE:
                              scores[piece.player] += 0.2*(col-1)
                              if self.board[row][col+1] != None and self.board[row][col+1].player != piece.player:
                                  scores[piece.player] -= 0.2
                              for dr in [-1, 1]:
                                  for dc in [1]:
                                      r, c = row + dr, col + dc
                                      if self.is_valid_square(r, c):
                                          if self.board[row-1][col] != None:
                                              target = self.board[row-1][col]
                                              if target.player == piece.player:
                                                  if target.piece_type == PieceType.BISHOP or target.piece_type == PieceType.KNIGHT:
                                                      scores[piece.player] += 0.2 # piece on outpost
                                              else:
                                                  scores[piece.player] += 0.2 # attacking enemy piece
                                                  if target.piece_type == PieceType.KING:
                                                      scores[piece.player] += 0.1 # attacking enemy king
                                                      scores[target.player] -= 0.5 # king in danger - avoid getting attacked by enemy pawns
                          elif piece.player == Player.YELLOW:
                              scores[piece.player] += 0.2*(row-1)
                              if self.board[row+1][col] != None and self.board[row+1][col].player != piece.player:
                                  scores[piece.player] -= 0.2
                              for dr in [-1, 1]:
                                  for dc in [-1]:
                                      r, c = row + dr, col + dc
                                      if self.is_valid_square(r, c):
                                          if self.board[row-1][col] != None:
                                              target = self.board[row-1][col]
                                              if target.player == piece.player:
                                                  if target.piece_type == PieceType.BISHOP or target.piece_type == PieceType.KNIGHT:
                                                      scores[piece.player] += 0.2 # piece on outpost
                                              else:
                                                  scores[piece.player] += 0.2 # attacking enemy piece
                                                  if target.piece_type == PieceType.KING:
                                                      scores[piece.player] += 0.1 # attacking enemy king
                                                      scores[target.player] -= 0.5 # king in danger - avoid getting attacked by enemy pawns
                          elif piece.player == Player.GREEN:
                              scores[piece.player] += 0.2*(6-col)
                              if self.board[row][col-1] != None and self.board[row][col-1].player != piece.player:
                                  scores[piece.player] -= 0.2
                              for dr in [-1]:
                                  for dc in [-1, 1]:
                                      r, c = row + dr, col + dc
                                      if self.is_valid_square(r, c):
                                          if self.board[row-1][col] != None:
                                              target = self.board[row-1][col]
                                              if target.player == piece.player:
                                                  if target.piece_type == PieceType.BISHOP or target.piece_type == PieceType.KNIGHT:
                                                      scores[piece.player] += 0.2 # piece on outpost
                                              else:
                                                  scores[piece.player] += 0.2 # attacking enemy piece
                                                  if target.piece_type == PieceType.KING:
                                                      scores[piece.player] += 0.1 # attacking enemy king
                                                      scores[target.player] -= 0.5 # king in danger - avoid getting attacked by enemy pawns
        
        # print(f"Piece counts: {piece_counts}")
        # Calculate the average coordinates for each color
        # avg_coords = {player: [coord_sums[player][0] / piece_counts[player], coord_sums[player][1] / piece_counts[player]] for player in Player}

        # WE DO THIS BELOW
        # avg_coords = {}
        # for player in Player:
        #     try:
        #         avg_x = coord_sums[player][0] / piece_counts[player]
        #         avg_y = coord_sums[player][1] / piece_counts[player]
        #         avg_coords[player] = [avg_x, avg_y]
        #     except ZeroDivisionError:
        #         print("Zero division error")
        #         print(f"Piece counts for {player}: {piece_counts[player]}")
        #         print("Board:")
        #         self.print_board()

        # Calculate the distance of each king from the average coordinates of their army
        for player in Player:
            if king_present[player] == True:
                avg_row = coord_sums[player][0] / piece_counts[player]
                avg_col = coord_sums[player][1] / piece_counts[player]

                king_row, king_col = king_coords[player]
                
                distance = ((abs(king_row - avg_row))**2 + (abs(king_col - avg_col))**2)**0.5
                scores[player] -= 0.25 * distance
            else:
                scores[player] = -999    
        for player in Player:
            scores[player] += self.player_points[player]
            # scores[player] -= 20*1.25
            scores[player] -= 20

        # Final rounding of scores to 2 decimal places
        for player in Player:
            scores[player] = round(scores[player], 2)
        return scores

    # def evaluate(self):
    #     red_king_present = False
    #     blue_king_present = False
    #     yellow_king_present = False
    #     green_king_present = False
    #     scores = {player: 0 for player in Player}
    #     for row in range(8):
    #         for col in range(8):
    #             piece = self.board[row][col]
    #             if piece:
    #                 if not piece.is_dead and piece.player in self.active_players:
    #                   # scores[piece.player] += self.get_piece_value(piece) * 1.25 
    #                   scores[piece.player] += self.get_piece_value(piece)
                      
    #                   if piece.piece_type == PieceType.KING:
    #                       if piece.player == Player.RED:
    #                           red_king_present = True
    #                       elif piece.player == Player.BLUE:
    #                           blue_king_present = True
    #                       elif piece.player == Player.YELLOW:
    #                           yellow_king_present = True
    #                       elif piece.player == Player.GREEN:
    #                           green_king_present = True
        
    #     for player in Player:
    #         scores[player] += self.player_points[player]
    #         # scores[player] -= 20*1.25
    #         scores[player] -= 20
    #     if not red_king_present:
    #         scores[Player.RED] = -999
    #     if not blue_king_present:
    #         scores[Player.BLUE] = -999
    #     if not yellow_king_present:
    #         scores[Player.YELLOW] = -999
    #     if not green_king_present:
    #         scores[Player.GREEN] = -999

    #     # Final rounding of scores to 2 decimal places
    #     for player in Player:
    #         scores[player] = round(scores[player], 2)
    #     return scores

    def is_game_over(self):
        return len(self.active_players) == 1

    def eliminate_player(self, player):
        # print(f"{player} eliminated!")
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    if not piece.is_dead and piece.player == player:
                      if piece.piece_type != PieceType.KING:
                          piece.is_dead = True
                      else:
                          piece.piece_type = PieceType.DEAD_KING 
        self.active_players.remove(player)

    def print_board(self):
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
        print("   0  1  2  3  4  5  6  7")
        for row in range(8):
            print(row, end=" ")
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    if piece.is_dead: # or piece.piece_type == PieceType.DEAD_KING:
                        match piece.piece_type:
                            case PieceType.PAWN:
                                symbol = dead_pawn
                            case PieceType.KNIGHT:
                                symbol = dead_knight
                            case PieceType.BISHOP:
                                symbol = dead_bishop
                            case PieceType.ROOK:
                                symbol = dead_rook
                            case PieceType.QUEEN:
                                symbol = dead_queen
                            case PieceType.KING:
                                symbol = dead_king
                            case PieceType.ONE_POINT_QUEEN:
                                symbol = dead_queen
                    else:
                        match piece.player:
                            case Player.RED:
                                match piece.piece_type:
                                    case PieceType.PAWN:
                                        symbol = red_pawn
                                    case PieceType.KNIGHT:
                                        symbol = red_knight
                                    case PieceType.BISHOP:
                                        symbol = red_bishop
                                    case PieceType.ROOK:
                                        symbol = red_rook
                                    case PieceType.QUEEN:
                                        symbol = red_queen
                                    case PieceType.KING:
                                        symbol = red_king
                                    case PieceType.ONE_POINT_QUEEN:
                                        symbol = red_queen
                                    case PieceType.DEAD_KING:
                                        symbol = red_king
                            case Player.BLUE:
                                match piece.piece_type:
                                    case PieceType.PAWN:
                                        symbol = blue_pawn
                                    case PieceType.KNIGHT:
                                        symbol = blue_knight
                                    case PieceType.BISHOP:
                                        symbol = blue_bishop
                                    case PieceType.ROOK:
                                        symbol = blue_rook
                                    case PieceType.QUEEN:
                                        symbol = blue_queen
                                    case PieceType.KING:
                                        symbol = blue_king
                                    case PieceType.ONE_POINT_QUEEN:
                                        symbol = blue_queen
                                    case PieceType.DEAD_KING:
                                        symbol = blue_king
                            case Player.YELLOW:
                                match piece.piece_type:
                                    case PieceType.PAWN:
                                        symbol = yellow_pawn
                                    case PieceType.KNIGHT:
                                        symbol = yellow_knight
                                    case PieceType.BISHOP:
                                        symbol = yellow_bishop
                                    case PieceType.ROOK:
                                        symbol = yellow_rook
                                    case PieceType.QUEEN:
                                        symbol = yellow_queen
                                    case PieceType.KING:
                                        symbol = yellow_king
                                    case PieceType.ONE_POINT_QUEEN:
                                        symbol = yellow_queen
                                    case PieceType.DEAD_KING:
                                        symbol = yellow_king
                            case Player.GREEN:
                                match piece.piece_type:
                                    case PieceType.PAWN:
                                        symbol = green_pawn
                                    case PieceType.KNIGHT:
                                        symbol = green_knight
                                    case PieceType.BISHOP:
                                        symbol = green_bishop
                                    case PieceType.ROOK:
                                        symbol = green_rook
                                    case PieceType.QUEEN:
                                        symbol = green_queen
                                    case PieceType.KING:
                                        symbol = green_king
                                    case PieceType.ONE_POINT_QUEEN:
                                        symbol = green_queen
                                    case PieceType.DEAD_KING:
                                        symbol = green_king
                    print(f"[{symbol}]", end="")
                else:
                    print("[ ]", end="")
            print()

    # RESIGNATION / FLAGGING: 
    # Eliminate the player and adjust turn
    
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
    def resign(self): # PROBABLY NEEDS MORE WORK
        player = self.current_player
        # self.resigned_players.append(player)
        # self.active_players.remove(player)
        # for row in range(8):
        #     for col in range(8):
        #         piece = self.board[row][col]
        #         if piece:
        #             if not piece.is_dead and piece.player == player:
        #               if piece.piece_type != PieceType.KING:
        #                   piece.is_dead = True
        #               else:
        #                   piece.piece_type = PieceType.DEAD_KING
        self.eliminate_player(player) 
        if len(self.active_players) != 1:
            self.current_player = Player((self.current_player.value + 1) % 4)
            while (self.current_player not in self.active_players):
                self.current_player = Player((self.current_player.value + 1) % 4)



# def max_4(board, root_player, depth): # add root player parameter? -> def negamax4(board, depth, root_player):
#     global nodes
#     nodes += 1
#     if depth == 0 or board.is_game_over():
#         #print("Running board.evaluate()")
#         return board.evaluate()

#     max_scores = {p: float('-inf') if p != root_player else float('inf') for p in board.active_players}
#     player = board.current_player

#     for move in board.get_psuedo_legal_moves(player):
#         captured_piece, eliminated_players = board.make_move(move)

#         scores = max_4(board, root_player, depth - 1)
        
#         if scores[player] > max_scores[player]:
#             for p in Player: 
#                 max_scores[p] = scores[p]

#         board.undo_move(move, captured_piece, eliminated_players)

#     return max_scores

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

def parse_board_from_fen(fen_string):
    print(f"Fen string:\n{fen_string}")
    parts = fen_string.split('-')
    print(f"Parts: {parts}")
    print(f"len(parts): {len(parts)}")
    # Create a new Board instance
    board = Board()
    board.board = [[None] * 8 for _ in range(8)]
    
    # Part 1: Handle eliminated players
    eliminated_players = parts[1].split(',')
    for i, eliminated in enumerate(eliminated_players):
        if eliminated == '1':
            player = Player(i)
            board.current_player = player
            board.resign()

    # Part 4: Set player points
    points = parts[4].split(',')
    for i, point in enumerate(points):
        board.player_points[Player(i)] = int(point)

    # Part 7: Piece placement
    rows = parts[7].split('/')
    for row in range(3, 11):  # Throw away the first three and last three rows
        pieces = rows[row].split(',')[3:-3]  # Throw away the first three and last three values
        col = 0
        for piece_info in pieces:
            if piece_info.isdigit():
                # Empty squares
                col += int(piece_info)
            elif piece_info == 'x':
                # Empty square
                col += 1
            else:
                player = None
                piece_type = None
                is_dead = False

                if len(piece_info) == 3:
                    # Dead piece
                    if piece_info[0] == 'd':
                        is_dead = True
                        piece_info = piece_info[1:]
                    else:
                        raise ValueError(f"Invalid piece format: {piece_info}")

                if len(piece_info) == 2:
                    # Normal piece
                    if piece_info[0] == 'r':
                        player = Player.RED
                    elif piece_info[0] == 'b':
                        player = Player.BLUE
                    elif piece_info[0] == 'y':
                        player = Player.YELLOW
                    elif piece_info[0] == 'g':
                        player = Player.GREEN

                    if piece_info[1] == 'P':
                        piece_type = PieceType.PAWN
                    elif piece_info[1] == 'N':
                        piece_type = PieceType.KNIGHT
                    elif piece_info[1] == 'B':
                        piece_type = PieceType.BISHOP
                    elif piece_info[1] == 'R':
                        piece_type = PieceType.ROOK
                    elif piece_info[1] == 'K':
                        piece_type = PieceType.KING

                if player is not None and piece_type is not None:
                    piece = Piece(player, piece_type)
                    piece.is_dead = is_dead
                    board.board[row - 3][col] = piece
                col += 1
    # Part 0: Set current player
    player_char = parts[0][0]
    if player_char == 'R':
        board.current_player = Player.RED
    elif player_char == 'B':
        board.current_player = Player.BLUE
    elif player_char == 'Y':
        board.current_player = Player.YELLOW
    elif player_char == 'G':
        board.current_player = Player.GREEN
    return board

def get_san_string(move, board):
    from_piece = board.board[move.from_loc.row][move.from_loc.col]
    to_piece = board.board[move.to_loc.row][move.to_loc.col]

    from_piece_type = from_piece.piece_type.name[0]
    if from_piece_type == 'P':
        from_piece_type = ''

    
    to_piece_type = '' if to_piece == None else to_piece.piece_type.name[0]
    if to_piece_type == 'P':
        to_piece_type = ''
    from_col = chr(move.from_loc.col + ord('a'))
    from_row = 8 - move.from_loc.row
    to_col = chr(move.to_loc.col + ord('a'))
    to_row = 8 - move.to_loc.row

    capture = 'x' if to_piece else '-'

    promotion = ''
    if move.promotion_piece_type:
        promotion = '=' + move.promotion_piece_type.name[0]

    return f"{from_piece_type}{from_col}{from_row}{capture}{to_piece_type}{to_col}{to_row}{promotion}"

def get_uci_string(move, board):
    from_col = chr(move.from_loc.col + ord('a'))
    from_row = 8 - move.from_loc.row
    to_col = chr(move.to_loc.col + ord('a'))
    to_row = 8 - move.to_loc.row

    return f"{from_col}{from_row}{to_col}{to_row}"

if __name__ == '__main__':
    board = Board()
    #board.make_move(Move(BoardLocation(6, 0), BoardLocation(11, 3)))  # Blue queen(6, 0) to (11, 3)

    # # Setting up the board such that yellow has mate in 1 on green
    # board.make_move(Move(BoardLocation(12, 7), BoardLocation(11, 7))) # red pawn move ############ fix (13,7) and 12,7 to 12, 7 and 11,7
    # board.make_move(Move(BoardLocation(10, 1), BoardLocation(10, 3))) # blue pawn move
    # board.make_move(Move(BoardLocation(9, 1), BoardLocation(9, 2))) # blue pawn move
    # board.make_move(Move(BoardLocation(1, 8), BoardLocation(2, 8))) # yellow pawn move
    # board.make_move(Move(BoardLocation(13, 8), BoardLocation(11, 6))) # red bishop move
    # # board.current_player = Player.YELLOW
    # board.current_player = Player.GREEN

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
    

    # FOR TESTING MOVE GEN ---------------------------------------------------------------------------------------------------------------------------
    # player_to_generate_moves_for = board.current_player
    # player_to_generate_moves_for = Player.RED ################################################## change back to board.current_player?
    # board.current_player = player_to_generate_moves_for
    # print ("Current state of the board: ")
    # board.print_board()
    # psuedo_legal_moves = board.get_psuedo_legal_moves(player_to_generate_moves_for)
    # # legal_moves = board.get_legal_moves(player_to_generate_moves_for)
    # time.sleep(3)
    # for i, move in enumerate(psuedo_legal_moves):
    #     print(f"Move generated {i+1}: ({move.from_loc.row}, {move.from_loc.col}) to ({move.to_loc.row}, {move.to_loc.col}) ")
    #     print(f"Making move {i+1}")
    #     print(f"Scores: {board.evaluate}")
    #     print(f"Player points: {board.player_points}")
    #     captured_piece, eliminated_players = board.make_move(move)
    #     board.print_board()
    #     print(f"Turn: {board.current_player}")
    #     print(f"Active players: {board.active_players}\n")
    #     time.sleep(0.5)
    #     board.undo_move(move, captured_piece, eliminated_players)
    #     print(f"Undid move {i+1}")
    #     print(f"Scores: {board.evaluate()}")
    #     print(f"Player points: {board.player_points}")
    #     board.print_board()
    #     print(f"Turn: {board.current_player}")
    #     print(f"Active players: {board.active_players}")
    #     print(f"Player points: {board.player_points}\n")
    #     time.sleep(0.5)
    # print(f"Total moves generated: psuedo_legal - {len(psuedo_legal_moves)}")

    # PSUEDO LEGAL MOVES
    # psuedo_legal_moves =
    # for move in psuedo_legal_moves:
    #     print
    ####################################------------------------------------------------------------------------------
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
    # moves_to_play = 4 # how many moves do we want to play out
    # for _ in range (moves_to_play):
    #     start_time = time.time()
    #     # best_move, scores = get_best_move(board, 2)
    #     best_move, scores = get_best_move(board, 5) # depth 3 search so that to see if red and yellow will mate green
    #     end_time = time.time()
    #     execution_time = end_time - start_time
    #     print("Search completed")
    #     print(f"Number of nodes visited: {nodes + 1}")
    #     print(f"Execution time for this search: {execution_time} seconds")
    #     nps = (nodes + 1) / execution_time
    #     print(f"Nodes per second (NPS): {nps}")
    #     if best_move:
    #         print(f"Best move: ({best_move.from_loc.row}, {best_move.from_loc.col}) to ({best_move.to_loc.row}, {best_move.to_loc.col}), Scores: {scores} ")
    #         # What happens if we play the best move
    #         board.make_move(best_move)
    #         print("Board state after playing best move: ")
    #         board.print_board()
    #         print("Turn: ", board.current_player)
    #         print("Active players: ", board.active_players)
    #         print("board.evaluate() output: ", board.evaluate(), "\n")
    #     else:
    #         print("No valid moves found or game is over. \n")
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
    # print("Making two players resign")
    # board.resign()
    # print(f"Resigned. Active players: {board.active_players}")
    # board.resign()
    # print("Done")
    # print(f"Resigned. Active players: {board.active_players}")
    # print("Printing the board:")
    # board.print_board()
 
    # board.make_move((Move(BoardLocation(0, 4), BoardLocation(0, 3)))) # yellow king move
    # board.make_move((Move(BoardLocation(4, 6), BoardLocation(4, 5)))) # green pawn move
    # board.make_move((Move(BoardLocation(5, 7), BoardLocation(4, 6)))) # green bishop move to threaten the 

    # board.make_move((Move(BoardLocation(2, 0), BoardLocation(5, 1)))) # blue bishop # red can take this free bishop or move the king to safety
    # board.make_move((Move(BoardLocation(0, 5), BoardLocation(3, 5)))) # yellow bishop move

    # board.current_player = Player.RED
    # # board.make_move((Move(BoardLocation(4, 6), BoardLocation(7, 3)))) # green bishop move
    # print(board.evaluate())
    # print(board.player_points)
    # # board.make_move((Move(BoardLocation(4, 6), BoardLocation(7, 4))))
    # # board.make_move((Move(BoardLocation(7, 4), BoardLocation(7, 5))))
    # board.print_board()
    #######################################
    # while not board.is_game_over():
    # while False:

    fen_string = '''B-0,0,1,1-0,0,0,0-0,0,0,0-4,3,14,0-0-{'dim':'8x8','boxOffset':1}-
x,x,x,x,x,x,x,x,x,x,x,x,x,x/
x,x,x,x,x,x,x,x,x,x,x,x,x,x/
x,x,x,x,x,x,x,x,x,x,x,x,x,x/
x,x,x,1,bP,bN,rB,1,dyB,1,dyR,x,x,x/
x,x,x,1,bK,1,bP,3,dyP,x,x,x/
x,x,x,2,bP,1,dyP,3,x,x,x/
x,x,x,8,x,x,x/
x,x,x,2,rP,5,x,x,x/
x,x,x,1,rP,1,rP,3,dgB,x,x,x/
x,x,x,rP,1,rN,3,bR,dgN,x,x,x/
x,x,x,1,rK,5,dgR,x,x,x/
x,x,x,x,x,x,x,x,x,x,x,x,x,x/
x,x,x,x,x,x,x,x,x,x,x,x,x,x/
x,x,x,x,x,x,x,x,x,x,x,x,x,x'''
    # board = parse_board_from_fen(fen_string)
    # board.print_board()

    for i in range(100):
        print(f"Searching for the best move for {board.current_player}.")
        start_time = time.time()
        best_move, scores = get_best_move(board, 5) # depth 3 search so that to see if red and yellow will mate green
        end_time = time.time()
        execution_time = end_time - start_time
        print("Search completed")
        print(f"Number of nodes visited: {nodes + 1}")
        print(f"Execution time for this search: {execution_time} seconds")
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
        else:
            print("No valid moves found or game is over. ")

    print(f"Game over! Final scores: {board.player_points}")






# Update: For king - moving near friendly pawns gives bonus 