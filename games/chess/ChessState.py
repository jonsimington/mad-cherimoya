class ChessState:
    def __init__(self):
        self.board = None
        self.pieces = None
        self.enemy_pieces = None
        self.en_passant_enemy = None
        self.en_passant_ally = None
        self.enemy_king_board_location = None
        self.king_board_location = None
        self.fen_string = None
        self.neighbors = []
