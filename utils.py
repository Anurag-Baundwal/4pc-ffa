from pieces import PieceType, Player, Piece
from board import Board 

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