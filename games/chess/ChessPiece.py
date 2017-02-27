class ChessPiece:
    def __init__(self):
        self.type = None
        self.board_location = None
        self.rank_file = None
        self.has_moved = False
        self.captured = False
        self.color = None

    def __str__(self):
        if self.color == "White":
            return str(self.type)
        return str(self.type).lower()
