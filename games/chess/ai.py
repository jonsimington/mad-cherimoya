# This is where you build your AI for the Chess game.

from joueur.base_ai import BaseAI
from games.chess.ChessPiece import ChessPiece
from games.chess.PieceType import PieceType
from games.chess.ChessMove import ChessMove
from games.chess.MoveType import MoveType
from games.chess.ChessState import ChessState
import random


class AI(BaseAI):
    """ The basic AI functions that are the same between games. """

    def get_name(self):
        """ This is the name you send to the server so your AI will control the
        player named this string.

        Returns
            str: The name of your Player.
        """

        return "Ethan and the Bradberries"  # REPLACE THIS WITH YOUR TEAM NAME

    def start(self):
        """ This is called once the game starts and your AI knows its playerID
        and game. You can initialize your AI here.
        """
        # If a custom (non-default) FEN has been loaded
        custom_fen = self.game.fen != "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        # Reference pieces by id
        pieces = {}
        enemy_pieces = {}

        # Reference pieces by location
        board = {}
        en_passant_enemy = None

        # Load our pieces
        for piece in self.player.pieces:
            p = ChessPiece()
            p.convert_from_game_piece(piece)

            p.has_moved = custom_fen
            # Special pawn case for determining 2 space move
            if p.type == PieceType.PAWN:
                if p.color == "White":
                    # If the pawn is on rank 2
                    p.has_moved = p.board_location[0] != 6
                else:
                    # If the pawn is on rank 7
                    p.has_moved = p.board_location[0] != 1
            if p.type == PieceType.KING:
                # Set a special variable for the king
                king_board_location = p.board_location

            # Add to the dictionary
            pieces[str(p)] = p

            # Mark the board
            board[p.board_location] = p

        # Load enemy pieces
        for piece in self.player.opponent.pieces:
            p = ChessPiece()
            p.convert_from_game_piece(piece)

            p.has_moved = custom_fen
            # Special pawn case for determining 2 space move
            if p.type == PieceType.PAWN:
                if p.color == "White":
                    # If the pawn is on rank 2
                    p.has_moved = p.board_location[0] != 6
                else:
                    # If the pawn is on rank 7
                    p.has_moved = p.board_location[0] != 1

            # Add to the dictionary
            enemy_pieces[str(p)] = p

            # Mark the board
            board[p.board_location] = p

        if custom_fen:
            print("Using custom FEN!")
            # Load FEN stuff
            fen = tuple(self.game.fen.split(" "))

            # Check castling
            if fen[2] != "-":
                # Castling is available
                print("Castling available!")

                # Figure out who can castle where
                for char in fen[2]:
                    if char == "K":
                        # White can castle kingside
                        board[(7, 7)].has_moved = False
                        board[(7, 4)].has_moved = False
                    elif char == "Q":
                        # White can castle queenside
                        board[(7, 0)].has_moved = False
                        board[(7, 4)].has_moved = False
                    elif char == "k":
                        # Black can castle kingside
                        board[(0, 7)].has_moved = False
                        board[(0, 4)].has_moved = False
                        pass
                    elif char == "q":
                        # Black can castle queenside
                        board[(0, 0)].has_moved = False
                        board[(0, 4)].has_moved = False
                        pass
                    else:
                        print("FEN part 3 Error! {}".format(fen[2]))
                        exit(1)
            # Check en passant
            if fen[3] != "-":
                # A piece can move en passant
                print("En Passant available!")

                loc = AI.rank_file_to_board_loc((int(fen[3][1]), fen[3][0]))

                if loc[0] % 2 == 0:
                    # It's a black piece

                    if self.player.color != "Black":
                        # It's an enemy piece
                        piece_loc = loc[0] + 1, loc[1]
                        en_passant_enemy = board[piece_loc], loc
                else:
                    # It's a white piece
                    if self.player.color != "White":
                        # It's an enemy piece
                        piece_loc = loc[0] - 1, loc[1]
                        en_passant_enemy = board[piece_loc], loc

                if en_passant_enemy is not None:
                    print("There is an enemy who may be able to be captured en passant")

        # Create our initial state
        self.current_state = ChessState()
        self.current_state.board = board
        self.current_state.pieces = pieces
        self.current_state.enemy_pieces = enemy_pieces
        self.current_state.en_passant_enemy = en_passant_enemy
        self.current_state.king_board_location = king_board_location
        self.current_state.fen_string = self.game.fen

        print("Initialization done")

    def game_updated(self):
        """ This is called every time the game's state updates, so if you are
        tracking anything you can update it here.
        """

        # replace with your game updated logic

    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and
        dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why you won or
                          lost.
        """

        # replace with your end logic

    def run_turn(self):
        """ This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your
                  turn, False means to keep your turn going and re-call this
                  function.
        """

        # Here is where you'll want to code your AI.

        # We've provided sample code that:
        #    1) prints the board to the console
        #    2) prints the opponent's last move to the console
        #    3) prints how much time remaining this AI has to calculate moves
        #    4) makes a random (and probably invalid) move.

        # 1) print the board to the console
        self.print_current_board()

        if len(self.game.moves) > 0:
            # TODO: Set the en passant enemy variable
            # TODO: Handle piece promotion
            # Grab the previous move
            m = self.game.moves[-1]
            enemy_piece = m.piece

            enemy_piece_id = AI.create_id(enemy_piece)

            print("Opponent's Last Move: {} {} -> {}".format(enemy_piece_id, m.from_file + str(m.from_rank),
                                                             m.to_file + str(m.to_rank)))

            # Deal with capture
            captured_piece = m.captured

            if captured_piece is not None:
                # Build the id
                captured_piece_id = AI.create_id(captured_piece)

                print("Enemy {} captured our piece {}!".format(enemy_piece_id, captured_piece_id))

                # Removed the captured piece from the board and our pieces dict
                del self.current_state.board[AI.rank_file_to_board_loc((m.to_rank, m.to_file))]
                del self.current_state.pieces[captured_piece_id]

            # Remove enemy piece's old position
            del self.current_state.board[AI.rank_file_to_board_loc((m.from_rank, m.from_file))]

            # Set the enemy piece's new position
            self.current_state.board[AI.rank_file_to_board_loc((m.to_rank, m.to_file))] = \
                self.current_state.enemy_pieces[enemy_piece_id]

            # Update the enemy_pieces dict
            self.current_state.enemy_pieces[enemy_piece_id].board_location = \
                AI.rank_file_to_board_loc((m.to_rank, m.to_file))
            self.current_state.enemy_pieces[enemy_piece_id].rank_file = m.to_rank, m.to_file
            self.current_state.enemy_pieces[enemy_piece_id].has_moved = True

        # 3) print how much time remaining this AI has to calculate moves
        print("Time Remaining: " + str(self.player.time_remaining) + " ns")

        # Generate a random, valid move
        move = self.random_valid_move(self.current_state)
        rank_file = AI.board_loc_to_rank_file(move.board_location_to)
        piece = self.current_state.pieces[move.piece_moved_id]

        # Apply that move and see if it crashes
        piece.game_piece.move(rank_file[1], rank_file[0])

        # Update king_board_location if necessary
        if piece.type == PieceType.KING:
            self.current_state.king_board_location = move.board_location_to

        # Apply this move to the internal state
        # TODO: Fix KeyError where an en passant capture happens but the captured pawn stays on the board internally
        # TODO: Remove the captured piece (if there is one) from the opponent dictionary
        del self.current_state.board[piece.board_location]
        piece.board_location = move.board_location_to

        if move.piece_captured_id is not None:
            # There was something there, grab its id then remove it
            del self.current_state.enemy_pieces[move.piece_captured_id]

        piece.rank_file = rank_file
        self.current_state.board[piece.board_location] = piece
        piece.has_moved = True

        # Reset the en passant enemy because regardless of whether or not we captured it, en passant no longer exists
        self.current_state.en_passant_enemy = None

        if move.en_passant:
            print("En Passant capture! {} moved from {} -> {} to capture {}!".format(move.piece_moved_id,
                                                                                     move.board_location_from,
                                                                                     move.board_location_to,
                                                                                     move.piece_captured_id))

        return True  # to signify we are done with our turn.

    def random_valid_move(self, state):
        # TODO: Select a piece and print all legal moves for that piece
        valid_moves = set()
        # Iterate through each piece we own
        for key, piece in state.pieces.items():
            valid_moves |= self.valid_moves_for_piece(piece, state)

        return random.choice(list(valid_moves))

    @staticmethod
    def board_loc_to_rank_file(board_loc):
        return 8 - board_loc[0], chr(ord("a") + board_loc[1])

    @staticmethod
    def rank_file_to_board_loc(rank_file):
        return 8 - rank_file[0], ord(rank_file[1]) - ord("a")

    def is_board_location_under_attack(self, state, board_location, attacking_player_color):
        # Sanity check - is the location on the board?
        if not (0 <= board_location[0] < 8 and 0 <= board_location[1] < 8):
            return False

        # Radiates out from every valid direction and checks for pieces that can make it to the given location in 1 turn
        for move in MoveType:
            for movement_tuple in move.movement_tuples:
                if move != MoveType.L_SHAPED:
                    for i in range(1, 8, 1):
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
                                                # Grab the rank direction
                                                if self.player.color == attacking_player_color:
                                                    rank_dir = -self.player.rank_direction
                                                else:
                                                    rank_dir = -self.player.opponent.rank_direction

                                                # Check if our piece is "in front of" the pawn
                                                if occupying_piece.board_location[0] + rank_dir == board_location[0]:
                                                    return True
                                                else:
                                                    # It can't hit us, but it is protecting us
                                                    break
                                            else:
                                                # Out of range, still protects us
                                                break
                                        else:
                                            # We ran in to a pawn blocking everything else
                                            break

                                    elif occupying_piece.type == PieceType.KNIGHT:
                                        # We know we didn't find this through an L-shaped move, so we can ignore it
                                        pass
                                    else:
                                        # Rook, Bishop, Queen, King
                                        if move in occupying_piece.type.valid_moves and \
                                                        i <= occupying_piece.type.num_spaces:
                                            # The found piece can not only move in the direction we're looking,
                                            # but also make it the number of steps we've counted in one turn
                                            # TODO: Perhaps return which piece is threatening this location?
                                            return True
                                else:
                                    # We're protected by one of our pieces
                                    break

                        else:
                            # If we just went OOB, don't even bother continuing to go even more OOB
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
                                return True
        return False

    def is_in_check_after_move(self, move, state):
        new_state = AI.state_after_move(state, move)

        in_check = self.is_board_location_under_attack(new_state, move.board_location_to, self.player.opponent.color)

        print("If {} moves from {} -> {}, is the King ({}) in check? {}".format(move.piece_moved_id,
                                                                                move.board_location_from,
                                                                                move.board_location_to,
                                                                                state.king_board_location,
                                                                                in_check))

        return in_check

    @staticmethod
    def state_after_move(state, move):
        # Copy the state
        # TODO: Maybe only copy the piece that moves?
        new_board = {}
        new_pieces = {}
        new_enemy_pieces = {}
        new_state = ChessState()

        for key, value in state.pieces.items():
            new_pieces[key] = AI.copy_piece(value)

        for key, value in state.enemy_pieces.items():
            new_enemy_pieces[key] = AI.copy_piece(value)

        for p in new_pieces.values():
            new_board[p.board_location] = p

        for p in new_enemy_pieces.values():
            new_board[p.board_location] = p

        new_state.board = new_board
        new_state.pieces = new_pieces
        new_state.enemy_pieces = new_enemy_pieces

        if state.en_passant_enemy is not None:
            new_state.en_passant_enemy = new_state.enemy_pieces[str(state.en_passant_enemy)]

        new_state.king_board_location = state.king_board_location

        # Apply the move
        piece = new_state.pieces[move.piece_moved_id]

        # Update king_board_location if necessary
        if piece.type == PieceType.KING:
            new_state.king_board_location = move.board_location_to

        # Apply this move to the internal state
        # TODO: Fix KeyError where an en passant capture happens but the captured pawn stays on the board internally
        # TODO: Remove the captured piece (if there is one) from the opponent dictionary
        del new_state.board[piece.board_location]
        piece.board_location = move.board_location_to

        if move.piece_captured_id is not None:
            # There was something there, grab its id then remove it
            del new_state.enemy_pieces[move.piece_captured_id]

        piece.rank_file = AI.board_loc_to_rank_file(move.board_location_to)
        new_state.board[piece.board_location] = piece
        piece.has_moved = True

        # Reset the en passant enemy because regardless of whether or not we captured it, en passant no longer exists
        new_state.en_passant_enemy = None

        return new_state

    @staticmethod
    def copy_piece(piece):
        new_piece = ChessPiece()
        new_piece.id = piece.id
        new_piece.type = piece.type
        new_piece.board_location = piece.board_location
        new_piece.rank_file = piece.rank_file
        new_piece.has_moved = piece.has_moved
        new_piece.captured = piece.captured
        new_piece.color = piece.color
        new_piece.game_piece = piece.game_piece

        return new_piece

    def valid_moves_for_piece(self, piece, state):
        # TODO: Add all the weird rules like 2 space pawn movement, castling, promotion, etc...
        # TODO: Do a check to see if this new state is in check
        valid_moves = set()
        extra_moves = []
        if piece.type == PieceType.PAWN:
            r, c = piece.board_location

            # Two space pawn movement
            if not piece.has_moved:
                # Move it two spaces
                m = ChessMove()
                m.piece_moved_id = str(piece)
                m.board_location_from = r, c
                m.board_location_to = (r + -self.player.rank_direction * 2, c)

                extra_moves.append(m)

            # TODO: Promotion
            pass
        elif piece == PieceType.KING:
            # TODO: Castling
            pass

        # Iterate through possible move types
        for move_type in piece.type.valid_moves:
            # Iterate over the directions this move type has (up and down for vertical, etc...)
            for movement_tuple in move_type.movement_tuples:
                # Iterate through possible lengths (IE Bishop moving 1 space or 5)
                for length in range(1, piece.type.num_spaces + 1, 1):
                    # Grab current position on the board
                    r, c = piece.board_location

                    r += length * movement_tuple[0]
                    c += length * movement_tuple[1]

                    m = ChessMove()
                    m.piece_moved_id = str(piece)
                    m.board_location_from = piece.board_location
                    m.board_location_to = r, c

                    if self.is_valid(m, state):
                        if not self.is_in_check_after_move(m, state):
                            valid_moves.add(m)
                    else:
                        # If it's invalid for a certain step, certainly all subsequent steps will be invalid
                        break
        # Take care of any extra moves
        for m in extra_moves:
            if self.is_valid(m, state):
                if not self.is_in_check_after_move(m, state):
                    valid_moves.add(m)

        return valid_moves

    def is_valid(self, move, state):
        piece = state.pieces[move.piece_moved_id]
        r, c = move.board_location_to

        # Common sense check; is this space even on the board?
        if not (0 <= r < 8 and 0 <= c < 8):
            return False

        print("Seeing if we can move {} from {} -> {}".format(
            move.piece_moved_id, move.board_location_from, move.board_location_to))
        print("Is the space we're trying to move to under attack from {}? {}".format(
            self.player.opponent.color, self.is_board_location_under_attack(state, move.board_location_to,
                                                                            self.player.opponent.color)))

        if piece.type == PieceType.PAWN:
            # Negate rank direction to fit my coordinate system
            delta_row = move.board_location_to[0] - piece.board_location[0]
            if delta_row / abs(delta_row) != -self.player.rank_direction:
                # Pawns can't move backwards
                return False

            spaces_moved = abs(move.board_location_to[0] - piece.board_location[0])
            if spaces_moved > 2:
                # Pawn can move at most 2 spaces
                return False
            elif spaces_moved == 2:
                # Special two-space rule, but pawns can only do that at the start

                if piece.has_moved:
                    return False

                # If both spaces directly in front of the pawn aren't occupied
                return (piece.board_location[0] + delta_row / abs(delta_row), piece.board_location[1]) not in \
                       state.board.keys() and move.board_location_to not in state.board.keys()

            if move.board_location_to[1] != piece.board_location[1]:
                # It's moving diagonally

                # En Passant?
                if state.en_passant_enemy is not None:
                    # Are we moving there?
                    if move.board_location_to == state.en_passant_enemy[1]:
                        move.piece_captured_id = str(state.en_passant_enemy[0])
                        move.en_passant = True
                        return True

                if move.board_location_to in state.board.keys():
                    # Something is there
                    other_piece = state.board[move.board_location_to]

                    if other_piece.color != piece.color:
                        # Get 'em
                        move.piece_captured_id = str(other_piece)
                        return True

            else:  # It's moving forward
                # Is there something there?
                return move.board_location_to not in state.board.keys()
        # Knights don't have to move through their spaces
        elif piece.type == PieceType.KNIGHT:
            # Check if target location is empty or contains an enemy
            if move.board_location_to in state.board.keys():
                # Check to see if the space is an enemy or not
                if piece.color != state.board[move.board_location_to].color:
                    # Capture an enemy
                    move.piece_captured_id = str(state.board[move.board_location_to])
                    return True
                else:
                    return False
            else:
                # Space is empty
                return True
        else:
            # Some other piece

            # Is the target location occupied?
            if move.board_location_to in state.board.keys():
                # Is it an ally?
                piece_on_target_loc = state.board[move.board_location_to]

                if piece_on_target_loc.color == piece.color:
                    move.piece_captured_id = str(piece_on_target_loc)
                    return False

            # Check every space between it
            r1, c1 = move.board_location_to
            r2, c2 = piece.board_location
            movement_tuple = r1 - r2, c1 - c2

            r, c = movement_tuple
            # Normalize the tuple
            movement_tuple = r / abs(r) if r != 0 else 0, c / abs(c) if c != 0 else 0

            # The number of spaces we're moving
            delta = max(abs(r), abs(c))

            for i in range(1, delta, 1):
                r, c = piece.board_location

                r += i * movement_tuple[0]
                c += i * movement_tuple[1]

                # If that space is occupied
                if (r, c) in state.board.keys():
                    return False

            # If there's something to capture at the end of this journey
            if move.board_location_to in state.board.keys():
                move.piece_captured_id = str(state.board[move.board_location_to])

            return True

    @staticmethod
    def create_id(piece):
        if piece.type == "Knight":
            piece_id = "N"
        else:
            piece_id = piece.type[0]

        if piece.owner.color != "White":
            piece_id = piece_id.lower()

        piece_id += piece.id

        return piece_id

    def print_current_board(self):
        """Prints the current board using pretty ASCII art
        Note: you can delete this function if you wish
        """

        # iterate through the range in reverse order
        for r in range(9, -2, -1):
            output = ""
            if r == 9 or r == 0:
                # then the top or bottom of the board
                output = "   +------------------------+"
            elif r == -1:
                # then show the ranks
                output = "     a  b  c  d  e  f  g  h"
            else:  # board
                output = " " + str(r) + " |"
                # fill in all the files with pieces at the current rank
                for file_offset in range(0, 8):
                    # start at a, with with file offset increasing the char
                    f = chr(ord("a") + file_offset)
                    current_piece = None
                    for piece in self.game.pieces:
                        if piece.file == f and piece.rank == r:
                            # then we found the piece at (file, rank)
                            current_piece = piece
                            break

                    code = "."  # default "no piece"
                    if current_piece:
                        # the code will be the first character of their type
                        # e.g. 'Q' for "Queen"
                        code = current_piece.type[0]

                        if current_piece.type == "Knight":
                            # 'K' is for "King", we use 'N' for "Knights"
                            code = "N"

                        if current_piece.owner.id == "1":
                            # the second player (black) is lower case.
                            # Otherwise it's uppercase already
                            code = code.lower()

                    output += " " + code + " "

                output += "|"
            print(output)
