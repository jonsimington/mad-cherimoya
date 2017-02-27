from enum import Enum, unique


@unique
class MoveType(Enum):
    VERTICAL = ([(-1, 0), (1, 0)])
    HORIZONTAL = ([(0, -1), (0, 1)])
    L_SHAPED = ([(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)])
    DIAGONAL = ([(-1, -1), (-1, 1), (1, -1), (1, 1)])

    def __init__(self, movement_tuples):
        self.movement_tuples = movement_tuples
