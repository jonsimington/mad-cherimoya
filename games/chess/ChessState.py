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
        self.ply_since_capture_or_pawn_movement = 0

    def __str__(self):
        string = str(self.move_made)

        if self.heuristic_value is not None:
            string += ": " + str(self.heuristic_value)

        return string

    def is_draw(self):
        # TODO: Fifty-move rule
        if self.ply_since_capture_or_pawn_movement == 100:
            return True
        # TODO: Simplified threefold repetition
        # TODO: Not in check, but no legal move (stalemate)
        # TODO: Insufficient material
