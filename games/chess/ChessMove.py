class ChessMove:
    def __init__(self):
        self.piece_moved_id = None
        self.piece_captured_id = None
        self.board_location_from = None
        self.board_location_to = None
        self.promote_to = ""
        self.en_passant = False
        self.castling = False

    def __str__(self):
        str = "{} {} -> {}".format(self.piece_moved_id, self.board_location_from, self.board_location_to)

        if self.en_passant:
            str += " (En Passant Capture)"
        elif self.castling:
            str += " (Castling)"

        return str
