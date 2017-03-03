class ChessMove:
    def __init__(self):
        self.piece_moved_id = None
        self.piece_captured_id = None
        self.board_location_from = None
        self.board_location_to = None
        self.promote_to = None
        self.en_passant = False
        self.castling = False