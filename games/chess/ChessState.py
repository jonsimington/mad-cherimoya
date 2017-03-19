from games.chess.MoveType import MoveType
from games.chess.PieceType import PieceType


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
        self.me_in_check = None
        self.enemy_in_check = None
        self.previous_moves = []
        self.ply_since_promotion = 0

    def __str__(self):
        string = str(self.move_made)

        if self.heuristic_value is not None:
            string += ": " + str(self.heuristic_value)

        return string

    def is_in_checkmate(self, me=True):
        my_color = self.board[self.king_board_location].color if me \
            else self.board[self.enemy_king_board_location].color

        # I'm in check
        if self.is_in_check(me):
            if self.board[self.move_made.board_location_to].color != my_color:
                # My opponent made the move that got into this state, i am at move

                # If i'm in check and have no moves, i'm in checkmate
                return len(self.neighbors) == 0
            else:
                # I made the move that got into this state. The neighbors are my opponent's move. Indeterminate
                print("Hit indeterminate case in checkmate lookup")
                return None

        # I'm not in check, so I can't be in checkmate
        return False

    def is_in_check(self, me=True):
        # Lookup stored value
        lookup_var = self.me_in_check if me else self.enemy_in_check

        if lookup_var is not None:
            return lookup_var

        # Our king if the attacking color isn't us, otherwise the enemy king
        king_loc = self.king_board_location if me else self.enemy_king_board_location
        attacking_color = self.board[self.enemy_king_board_location].color if me else \
            self.board[self.king_board_location].color

        lookup_var = len(self.is_board_location_under_attack(king_loc, attacking_color))

        if me:
            self.me_in_check = lookup_var
        else:
            self.enemy_in_check = lookup_var

        return lookup_var

    def is_board_location_under_attack(state, board_location, attacking_player_color):
        defending_player_color = "White" if attacking_player_color == "Black" else "Black"
        rank_dir = 1 if attacking_player_color == "Black" else -1
        # print("Checking if {} is under attack by {}".format(board_location, attacking_player_color))
        attacking_piece_id_location_tuples = set()
        # Sanity check - is the location on the board?
        if not (0 <= board_location[0] < 8 and 0 <= board_location[1] < 8):
            # print("Invalid board location")
            return attacking_piece_id_location_tuples

        # Radiates out from every valid direction and checks for pieces that can make it to the given location in 1 turn
        for move in MoveType:
            for movement_tuple in move.movement_tuples:
                # print("{} {}".format(move.name, movement_tuple))
                if move != MoveType.L_SHAPED:
                    for i in range(1, 8, 1):
                        # print("i = {}".format(i))
                        r, c = board_location

                        # Check each board location
                        r += i * movement_tuple[0]
                        c += i * movement_tuple[1]

                        new_loc = r, c

                        # Is it in bounds?
                        if 0 <= r < 8 and 0 <= c < 8:

                            # Is it occupied?
                            if new_loc in state.board.keys():

                                occupying_piece = state.board[new_loc]

                                # Is it an enemy piece?
                                if occupying_piece.color == attacking_player_color:
                                    # Deal with pawns not being able to attack backwards
                                    if occupying_piece.type == PieceType.PAWN:
                                        if move == MoveType.DIAGONAL:
                                            # Pawns can only move 1, so is it in range?
                                            if i == 1:
                                                # Check if our piece is "in front of" the pawn
                                                if occupying_piece.board_location[0] + rank_dir == board_location[0]:
                                                    """ print("{} is under attack by a pawn at {}".format(
                                                        board_location, occupying_piece.board_location))"""
                                                    attacking_piece_id_location_tuples.add(
                                                        (str(occupying_piece), occupying_piece.board_location))
                                                else:
                                                    # It can't hit us, but it is protecting us
                                                    """ print("{} is protected by a pawn at {}".format(
                                                        board_location, occupying_piece.board_location))"""
                                                    break
                                            else:
                                                # Out of range, still protects us
                                                """ print("{} is protected by a pawn at {}".format(
                                                    board_location, occupying_piece.board_location))"""
                                                break
                                        else:
                                            # We ran in to a pawn blocking everything else
                                            """ print("{} is protected by a pawn at {}".format(
                                                board_location, occupying_piece.board_location))"""
                                            break

                                    elif occupying_piece.type == PieceType.KNIGHT:
                                        # We know we didn't find this through an L-shaped move, so we can ignore it
                                        """ print("{} is protected by a knight at {}".format(
                                            board_location, occupying_piece.board_location))"""
                                        break
                                    else:
                                        # Rook, Bishop, Queen, King
                                        if move in occupying_piece.type.valid_moves and \
                                                        i <= occupying_piece.type.num_spaces:
                                            # The found piece can not only move in the direction we're looking,
                                            # but also make it the number of steps we've counted in one turn
                                            attacking_piece_id_location_tuples.add(
                                                (str(occupying_piece), occupying_piece.board_location))
                                            """ print("{} is under attack by a {} at {}".format(
                                                board_location, str(occupying_piece), occupying_piece.board_location))"""
                                            break
                                        else:
                                            # That piece can't get us
                                            """ print("Protected by {} at {} who can't get us".format(
                                                str(occupying_piece), occupying_piece.board_location))"""
                                            break
                                else:
                                    # We're protected by one of our pieces
                                    # print("Our piece {} is protecting {}".format(str(occupying_piece), board_location))
                                    break

                        else:
                            # If we just went OOB, don't even bother continuing to go even more OOB
                            # print("Stopped going out of bounds: {}".format(new_loc))
                            break
                else:
                    # Check each board location
                    r, c = board_location
                    r += movement_tuple[0]
                    c += movement_tuple[1]

                    new_loc = r, c

                    # Is it in bounds?
                    if 0 <= r < 8 and 0 <= c < 8:

                        # Is it occupied?
                        if new_loc in state.board.keys():

                            occupying_piece = state.board[new_loc]

                            # Is it an enemy knight?
                            if occupying_piece.color == attacking_player_color and \
                                            occupying_piece.type == PieceType.KNIGHT:
                                # There's an enemy knight in one of the L-shaped spots
                                """ print("Enemy knight at {} threatens{}".format(
                                    occupying_piece.board_location, board_location))"""
                                attacking_piece_id_location_tuples.add(
                                    (str(occupying_piece), occupying_piece.board_location))
        return attacking_piece_id_location_tuples

    def is_draw(self):
        # TODO: Fifty-move rule
        if self.ply_since_capture_or_pawn_movement == 100:
            return True
        # TODO: Simplified threefold repetition
        if self.ply_since_capture_or_pawn_movement >= 8 and self.ply_since_promotion >= 8:
            for i in range(4):
                if self.previous_moves[i] != self.previous_moves[i + 4]:
                    return False
            return True
        # TODO: Not in check, but no legal move (stalemate) - Actually i'll implement that in the heuristic itself
        # TODO: Insufficient material
        material_lists = [({PieceType.KING}, {PieceType.KING}), 
                          ({PieceType.KING}, {PieceType.KING, PieceType.BISHOP}),
                          ({PieceType.KING}, {PieceType.KING, PieceType.KNIGHT}),
                          ({PieceType.KING, PieceType.BISHOP}, {PieceType.KING, PieceType.BISHOP})]

        for material_list in material_lists:
            for piece_list in [(self.pieces, self.enemy_pieces), (self.enemy_pieces, self.pieces)]:
                piece_set = set([p.type for p in piece_list[0]]), set([p.type for p in piece_list[1]])
                if piece_set[0] == material_list[0] and piece_set[1] == material_list[1]:
                    # Materials are the same

                    # Is this the special case?
                    if len(material_list[0]) == len(material_list[1]) == 2:
                        # TODO: Figure out a way to determine space colors
                        bishop_spaces = []

                        for piece in piece_list:
                            for p in piece:
                                if p.type == PieceType.BISHOP:
                                    bishop_spaces.append(p.board_location)
                                    break

                        bishop_spaces[0] = (8 * bishop_spaces[0][0] + bishop_spaces[0][1]) % 2
                        bishop_spaces[1] = (8 * bishop_spaces[1][0] + bishop_spaces[1][1]) % 2

                        return bishop_spaces[0] == bishop_spaces[1]
                    else:
                        return True
        return False
