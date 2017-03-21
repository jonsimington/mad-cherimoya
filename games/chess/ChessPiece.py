from games.chess.PieceType import PieceType


class ChessPiece:
    def __init__(self):
        self.id = -1
        self.type = None
        self.board_location = None
        self.rank_file = None
        self.has_moved = False
        self.captured = False
        self.color = None
        self.game_piece = None

    def __str__(self):
        if self.color == "White":
            return str(self.type) + str(self.id)
        return str(self.type).lower() + str(self.id).zfill(2)

    def __lt__(self, other):
        return str(self) < str(other)
    
    def convert_from_game_piece(self, piece):
        self.type = PieceType[piece.type.upper()]
        self.board_location = 8 - int(piece.rank), ord(piece.file) - ord("a")
        self.rank_file = piece.rank, piece.file
        self.has_moved = piece.has_moved
        self.captured = piece.captured
        self.color = piece.owner.color
        self.game_piece = piece
        self.id = piece.id
