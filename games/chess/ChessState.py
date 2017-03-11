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
        self.move_made = None
        self.heuristic_value = None

    def __str__(self):
        string = str(self.move_made)

        if self.heuristic_value is not None:
            string += ": " + str(self.heuristic_value)

        return string
