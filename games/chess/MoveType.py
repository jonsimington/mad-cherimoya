from enum import Enum, unique


@unique
class MoveType(Enum):
    VERTICAL = 1
    HORIZONTAL = 2
    L_SHAPED = 3
    DIAGONAL = 4
