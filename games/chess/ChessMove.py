class ChessMove:
    def __init__(self):
        self.piece_moved_id = None
        self.piece_captured_id = None
        self.board_location_from = None
        self.board_location_to = None
        self.promote_to = ""
        self.en_passant = False
        self.castling = False

    def __eq__(self, other):
        return self.board_location_from == other.board_location_from and \
               self.board_location_to == other.board_location_to

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        str = "{} {} -> {}".format(self.piece_moved_id, self.board_location_from, self.board_location_to)

        if self.en_passant:
            str += " (En Passant Capture)"
        elif self.castling:
            str += " (Castling)"
        elif self.promote_to != "":
            str += " (Promoted to {})".format(self.promote_to)

        return str
