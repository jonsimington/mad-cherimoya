from enum import Enum, unique
from games.chess.MoveType import MoveType


@unique
class PieceType(Enum):
    PAWN = ([MoveType.VERTICAL, MoveType.DIAGONAL], 1)
    ROOK = ([MoveType.VERTICAL, MoveType.HORIZONTAL], 8)
    KNIGHT = ([MoveType.L_SHAPED], 1)
    BISHOP = ([MoveType.DIAGONAL], 8)
    QUEEN = ([MoveType.VERTICAL, MoveType.HORIZONTAL, MoveType.DIAGONAL], 8)
    KING = ([MoveType.VERTICAL, MoveType.HORIZONTAL, MoveType.DIAGONAL], 1)

    def __init__(self, valid_moves, num_spaces):
        self.valid_moves = valid_moves
        self.num_spaces = num_spaces

    def __str__(self):
        # To stay with SIG-Game convention, represent Knights with 'N'
        if self == PieceType.KNIGHT:
            return "N"
        return self.name[0]
