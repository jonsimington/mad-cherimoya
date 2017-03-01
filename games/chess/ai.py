# This is where you build your AI for the Chess game.

from joueur.base_ai import BaseAI
from games.chess.ChessPiece import ChessPiece
from games.chess.PieceType import PieceType
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

        # Reference pieces by id
        self.pieces = {}
        self.enemy_pieces = {}

        # Reference pieces by location
        self.board = {}

        # Load our pieces
        for piece in self.player.pieces:
            p = ChessPiece()
            p.convert_from_game_piece(piece)

            # Add to the dictionary
            self.pieces[str(p)] = p

            # Mark the board
            self.board[p.board_location] = p

        # Load enemy pieces
        for piece in self.player.opponent.pieces:
            p = ChessPiece()
            p.convert_from_game_piece(piece)

            # Add to the dictionary
            self.enemy_pieces[str(p)] = p

            # Mark the board
            self.board[p.board_location] = p

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
                del self.board[AI.rank_file_to_board_loc((m.to_rank, m.to_file))]
                del self.pieces[captured_piece_id]

            # Remove enemy piece's old position
            del self.board[AI.rank_file_to_board_loc((m.from_rank, m.from_file))]

            # Set the enemy piece's new position
            self.board[AI.rank_file_to_board_loc((m.to_rank, m.to_file))] = self.enemy_pieces[enemy_piece_id]

            # Update the enemy_pieces dict
            self.enemy_pieces[enemy_piece_id].board_location = AI.rank_file_to_board_loc((m.to_rank, m.to_file))
            self.enemy_pieces[enemy_piece_id].rank_file = m.to_rank, m.to_file
            self.enemy_pieces[enemy_piece_id].has_moved = True

        # 3) print how much time remaining this AI has to calculate moves
        print("Time Remaining: " + str(self.player.time_remaining) + " ns")

        # Generate a random, valid move
        piece_id, rank_file = self.random_valid_move()
        
        piece = self.pieces[piece_id]

        # Apply that move and see if it crashes
        piece.game_piece.move(rank_file[1], rank_file[0])

        # Apply this move to the internal state
        del self.board[piece.board_location]
        piece.board_location = AI.rank_file_to_board_loc(rank_file)
        piece.rank_file = rank_file
        self.board[piece.board_location] = piece
        piece.has_moved = True

        return True  # to signify we are done with our turn.

    def random_valid_move(self):
        # TODO: Select a piece and print all legal moves for that piece
        valid_moves = set()
        # Iterate through each piece we own
        for key, piece in self.pieces.items():
            valid_moves |= self.valid_moves_for_piece(piece)

        return random.choice(list(valid_moves))

    @staticmethod
    def board_loc_to_rank_file(board_loc):
        return 8 - board_loc[0], chr(ord("a") + board_loc[1])

    @staticmethod
    def rank_file_to_board_loc(rank_file):
        return 8 - rank_file[0], ord(rank_file[1]) - ord("a")

    def valid_moves_for_piece(self, piece):
        # TODO: Add all the weird rules like 2 space pawn movement, castling, promotion, etc...
        valid_moves = set()
        extra_moves = []
        if piece.type == PieceType.PAWN:
            r, c = piece.board_location
            # TODO: En Passant
            # TODO: Two space pawn movement
            if not piece.has_moved:
                # Move it two spaces
                extra_moves.append((r + -self.player.rank_direction * 2, c))

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

                    if self.is_valid(piece, (r, c)):
                        valid_moves.add((str(piece), AI.board_loc_to_rank_file((r, c))))
        # Take care of any extra moves
        for m in extra_moves:
            if self.is_valid(piece, m):
                valid_moves.add((str(piece), AI.board_loc_to_rank_file(m)))

        return valid_moves

    def is_valid(self, piece, board_location):
        r, c = board_location

        # Common sense check; is this space even on the board?
        if not (0 <= r < 8 and 0 <= c < 8):
            return False

        elif piece.type == PieceType.PAWN:
            # Negate rank direction to fit my coordinate system
            delta_row = board_location[0] - piece.board_location[0]
            if delta_row / abs(delta_row) != -self.player.rank_direction:
                # Pawns can't move backwards
                return False

            spaces_moved = abs(board_location[0] - piece.board_location[0])
            if spaces_moved > 2:
                # Pawn can move at most 2 spaces
                return False
            elif spaces_moved == 2:
                # Special two-space rule, but pawns can only do that at the start

                if piece.has_moved:
                    return False

                # If both spaces directly in front of the pawn aren't occupied
                return (piece.board_location[0] + delta_row / abs(delta_row), piece.board_location[1]) not in \
                       self.board.keys() and board_location not in self.board.keys()

            if board_location[1] != piece.board_location[1]:
                # It's moving diagonally

                # En Passant?
                if len(self.game.moves) > 0:
                    # There was some previous move

                    # If there is an adjacent piece
                    if (piece.board_location[0], board_location[1]) in self.board.keys():
                        pawn = self.board[(piece.board_location[0], board_location[1])]
                        
                        # If it's a pawn
                        if pawn.type == PieceType.PAWN:
                            
                            # If it's an enemy
                            if pawn.color != piece.color:
                                
                                # Check previous move
                                move = self.game.moves[-1]

                                # Did this piece move last turn?
                                if str(pawn) == AI.create_id(move.piece):
                                    # Is this the first time it moved?
                                    # TODO: This
                                    return True

                if board_location in self.board.keys():
                    # Something is there
                    other_piece = self.board[board_location]

                    if other_piece.color != piece.color:
                        # Get 'em
                        return True

            else:  # It's moving forward
                # Is there something there?
                return board_location not in self.board.keys()
        # Knights don't have to move through their spaces
        elif piece.type == PieceType.KNIGHT:
            # Check if target location is empty or contains an enemy
            if board_location in self.board.keys():
                # Check to see if the space is an enemy or not
                if piece.color != self.board[board_location].color:
                    # Capture an enemy
                    return True
                else:
                    return False
            else:
                # Space is empty
                return True
        else:
            # Some other piece

            # Is the target location occupied?
            if board_location in self.board.keys():
                # Is it an ally?
                piece_on_target_loc = self.board[board_location]

                if piece_on_target_loc.color == piece.color:
                    return False

            # Check every space between it
            r1, c1 = board_location
            r2, c2 = piece.board_location
            movement_tuple = r1 - r2, c1 - c2

            r, c = movement_tuple
            # Normalize the tuple
            movement_tuple = r / abs(r) if r != 0 else 0, c / abs(c) if c != 0 else 0

            # The number of spaces we're moving
            delta = max(abs(r), abs(c))

            for i in range(1, delta + 1, 1):
                r, c = piece.board_location

                r += i * movement_tuple[0]
                c += i * movement_tuple[1]

                # If that space is occupied
                if (r, c) in self.board.keys():
                    return False

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
