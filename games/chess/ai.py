# This is where you build your AI for the Chess game.

from joueur.base_ai import BaseAI
from games.chess.ChessPiece import ChessPiece
from games.chess.PieceType import PieceType
from games.chess.ChessMove import ChessMove
from games.chess.MoveType import MoveType
from games.chess.ChessState import ChessState
import random
from copy import deepcopy


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
        print("start() function")

        # Appease the interpreter
        king_board_location = None
        enemy_king_board_location = None

        # Print which color we are
        print("We are the {} player".format(self.player.color))

        # If a custom (non-default) FEN has been loaded
        custom_fen = self.game.fen != "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        # Reference pieces by id
        pieces = {}
        enemy_pieces = {}

        # Reference pieces by location
        board = {}
        en_passant_enemy = None
        en_passant_ally = None

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
            elif p.type == PieceType.KING:
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
            elif p.type == PieceType.KING:
                # Set a special variable for the king
                enemy_king_board_location = p.board_location

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
                    elif char == "q":
                        # Black can castle queenside
                        board[(0, 0)].has_moved = False
                        board[(0, 4)].has_moved = False
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
                        # It's our piece
                        piece_loc = loc[0] + 1, loc[1]
                        en_passant_ally = board[piece_loc], loc
                else:
                    # It's a white piece
                    if self.player.color != "White":
                        # It's an enemy piece
                        piece_loc = loc[0] - 1, loc[1]
                        en_passant_enemy = board[piece_loc], loc
                    else:
                        # It's our piece
                        piece_loc = loc[0] + 1, loc[1]
                        en_passant_ally = board[piece_loc], loc

                if en_passant_enemy is not None:
                    print("There is an enemy or ally who may be able to be captured en passant")

        # Create our initial state
        self.current_state = ChessState()
        self.current_state.board = board
        self.current_state.pieces = pieces
        self.current_state.enemy_pieces = enemy_pieces
        self.current_state.en_passant_enemy = en_passant_enemy
        self.current_state.en_passant_ally = en_passant_ally
        self.current_state.enemy_king_board_location = enemy_king_board_location
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
        print("Turn {}".format(self.game.current_turn))
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

        if len(self.game.moves) > 0:
            """move_made = self.game.moves[-1]

            piece_moved_id = self.create_id(move_made.piece)

            if move_made.promotion != "":
                # Promotion occurred, change id to piece id before it was promoted
                if self.player.opponent.color == "White":
                    piece_moved_id = "P" + piece_moved_id[1:]
                else:
                    piece_moved_id = "p" + piece_moved_id[1:]

            # Search and find the move chosen from current neighbors
            for neighbor in self.current_state.neighbors:
                # Grab the move that brought us to that state
                m = neighbor.move_made

                # Do they agree on promotion?
                if m.promote_to == move_made.promotion:
                    # Promotion may or may not have occurred, but at least they agree

                    # Did the same piece move?
                    if m.piece_moved_id == piece_moved_id:
                        # Did they move to the same place?
                        if AI.board_loc_to_rank_file(m.board_location_to) == (move_made.to_rank, move_made.to_file):
                            # This is the move that was made
                            self.current_state = neighbor
                            break"""

            # Grab the previous move
            m = self.game.moves[-1]
            enemy_piece = m.piece

            enemy_piece_id = AI.create_id(enemy_piece)

            if m.promotion != "":
                # A promotion on the other side occurred
                if self.player.opponent.color == "White":
                    pre_promotion_id = "P" + enemy_piece_id[1:]
                else:
                    pre_promotion_id = "p" + enemy_piece_id[1:]

                p = self.current_state.enemy_pieces[pre_promotion_id]
                p.type = PieceType[m.promotion.upper()]
                del self.current_state.enemy_pieces[pre_promotion_id]
                self.current_state.enemy_pieces[enemy_piece_id] = p

                print("Opponent's Last Move: {} {} -> {}. Promoted to {}".format(
                    pre_promotion_id, m.from_file + str(m.from_rank), m.to_file + str(m.to_rank), m.promotion))

            else:
                print("Opponent's Last Move: {} {} -> {}".format(enemy_piece_id, m.from_file + str(m.from_rank),
                                                             m.to_file + str(m.to_rank)))

            # Check if the opponent castled
            if self.current_state.enemy_pieces[enemy_piece_id].type == PieceType.KING:
                # Did they castle?
                king_pos = self.current_state.enemy_pieces[enemy_piece_id].board_location
                file_delta = ord(m.from_file) - ord(m.to_file)
                if file_delta == 2:
                    # Queenside Castle, move the rook to file D
                    print("They castled Queenside!")

                    # Grab the rook, which we know is in file A
                    rook = self.current_state.board[(king_pos[0], 0)]

                    # Update its internal position
                    rook.board_location = king_pos[0], 3
                    rook.rank_file = AI.board_loc_to_rank_file(rook.board_location)

                    # Remove that board entry
                    del self.current_state.board[(king_pos[0], 0)]

                    # Move it
                    self.current_state.board[rook.board_location] = rook
                elif file_delta == -2:
                    # Kingside Castle, move the rook to file F
                    print("They castled Kingside!")

                    # Grab the rook, which we know is in file H
                    rook = self.current_state.board[(king_pos[0], 7)]

                    # Update its internal position
                    rook.board_location = king_pos[0], 5
                    rook.rank_file = AI.board_loc_to_rank_file(rook.board_location)

                    # Remove that board entry
                    del self.current_state.board[(king_pos[0], 7)]

                    # Move it
                    self.current_state.board[rook.board_location] = rook
                else:
                    # They didn't castle, continue as normal
                    pass
                # Regardless, keep track of the enemy king
                self.current_state.enemy_king_board_location = AI.rank_file_to_board_loc((m.to_rank, m.to_file))
            elif self.current_state.enemy_pieces[enemy_piece_id].type == PieceType.PAWN:
                # Check for en passant setup
                delta_rank = abs(m.from_rank - m.to_rank)

                if delta_rank == 2:
                    print("Enemy pawn moved two spaces. May be able to be captured en passant!")
                    # They made their "first" move, ie two spaces
                    passant_pawn = self.current_state.enemy_pieces[enemy_piece_id]
                    r, c = AI.rank_file_to_board_loc((m.to_rank, m.to_file))

                    # Long way, add negative of opponent rank direction. (-(-opponent.rank_direction)
                    # Same thing as (-(player.rank_direction)) -> -player.rank_direction

                    # Go one space "back" in rank
                    r += -self.player.rank_direction
                    self.current_state.en_passant_enemy = passant_pawn, (r, c)

            # Deal with capture
            captured_piece = m.captured

            if captured_piece is not None:
                # Build the id
                captured_piece_id = AI.create_id(captured_piece)

                print("Enemy {} captured our piece {}!".format(enemy_piece_id, captured_piece_id))

                captured_piece = self.current_state.pieces[captured_piece_id]

                # Removed the captured piece from the board and our pieces dict
                del self.current_state.board[captured_piece.board_location]
                del self.current_state.pieces[captured_piece_id]
                del captured_piece

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

        AI.print_board(self.current_state)
        print()

        # 3) print how much time remaining this AI has to calculate moves
        print("Time Remaining: " + str(self.player.time_remaining) + " ns")
        print()

        # Generate a random, valid move
        state = self.id_mm(self.current_state)  # random_valid_move(self.current_state)
        move = state.move_made
        print("Chosen move: {}".format(str(move)))
        rank_file = AI.board_loc_to_rank_file(move.board_location_to)
        piece = self.current_state.pieces[move.piece_moved_id]

        # Print all moves for chosen piece
        """v_m = self.valid_moves_for_piece(piece, self.current_state)
        print("All {} possible moves for {}:".format(len(v_m), str(piece)))
        for m in list(v_m):
            print(m)"""

        # Apply that move and see if it crashes
        piece.game_piece.move(rank_file[1], rank_file[0], move.promote_to)

        # We already calculated the state, just set it equal
        self.current_state = state

        if move.en_passant:
            print("En Passant capture! {} moved from {} -> {} to capture {}!".format(move.piece_moved_id,
                                                                                     move.board_location_from,
                                                                                     move.board_location_to,
                                                                                     move.piece_captured_id))
        elif move.castling:
            print("We castled!")

        print()

        return True  # to signify we are done with our turn.

    def random_valid_move(self, state):
        valid_moves = set()
        # Iterate through each piece we own
        for key, piece in state.pieces.items():
            valid_moves |= self.valid_moves_for_piece(piece, state)

        print("Generated {} possible moves".format(len(valid_moves)))

        for move in list(valid_moves):
            print(move)

        print()
        return random.choice(list(valid_moves))

    def valid_moves_in_state(self, state, me=True):
        chosen_pieces = state.pieces if me else state.enemy_pieces
        valid_moves = []
        # Iterate through each piece we own
        for key, piece in chosen_pieces.items():
            valid_moves.extend(self.valid_moves_for_piece(piece, state, me))

        return valid_moves

    def id_mm(self, state):
        print("ID-Minimax for {}".format(self.player.color))
        best_state = None
        # Defina a max depth
        # TODO: Put this somewhere else
        # TODO: Alternate who is at move
        max_depth = 2
        me = True

        # Set the initial depth, for me
        state.neighbors = self.valid_moves_in_state(state, me)

        current_level = state.neighbors

        # Iterate through the possible depths we're allowed to look at
        for depth in range(1, max_depth + 1, 1):
            # Call minimax on the current depth
            best_state = self.dl_mm(state, depth)

            # Generate the next depth worth of nodes
            # Generate moves for the OTHER player
            me = not me
            next_level = []
            for neighbor in current_level:
                neighbor.neighbors.extend(self.valid_moves_in_state(neighbor, me))

                # For easy access, add them to a new list
                next_level.extend(neighbor.neighbors)
            current_level = next_level
            next_level = None

        # Return the best state
        return best_state

    def dl_mm(self, state, max_depth):
        print("Depth-Limited MiniMax; d = {}".format(max_depth))
        if max_depth == 0:
            # Dumb, we have to go at least one ply deep
            return None
        elif len(state.neighbors) == 0:
            # Some sort of stalemante situation
            print("No available moves! Leaf node!")
            return self.chess_heuristic(state)

        max_value = 0
        best_state = None

        print("Looking at {} neighbors".format(len(state.neighbors)))
        for neighbor in state.neighbors:
            value = self.dl_mm_min_val(neighbor, max_depth - 1)

            print("{}: {}".format(str(neighbor), value))

            if best_state is None or value > max_value:
                print("{} is the new max!".format(str(neighbor)))
                best_state = neighbor
                max_value = value

        print("Returning {} with a value of {}".format(str(best_state), max_value))
        return best_state

    def dl_mm_max_val(self, state, depth):
        print("MaxV({}, {})".format(str(state), depth))
        max_value = None
        # Base case, return heuristic
        if depth == 0:
            val = self.chess_heuristic(state)
            print("\t={}".format(val))
            return val
        elif len(state.neighbors) == 0:
            # Some sort of stalemante situation
            print("No available moves! Leaf node!")
            return self.chess_heuristic(state)

        print("Looking at {} neighbors".format(len(state.neighbors)))
        for neighbor in state.neighbors:
            value = self.dl_mm_min_val(neighbor, depth - 1)

            if max_value is None or value > max_value:
                max_value = value
        
        return max_value

    def dl_mm_min_val(self, state, depth):
        print("MinV({}, {})".format(str(state), depth))
        min_value = None
        # Base case, return heuristic
        if depth == 0:
            val = self.chess_heuristic(state)
            print("\t={}".format(val))
            return val
        elif len(state.neighbors) == 0:
            print("No available moves! Leaf node!")
            return self.chess_heuristic(state)

        print("Looking at {} neighbors".format(len(state.neighbors)))
        for neighbor in state.neighbors:
            value = self.dl_mm_max_val(neighbor, depth - 1)

            if min_value is None or value < min_value:
                min_value = value

        return min_value

    def chess_heuristic(self, state):
        # TODO: Generate one level deeper than necessary to check if valid moves are available
        # If I did not make the last move, I am at move
        im_at_move = state.board[state.move_made.board_location_to].color != self.player.color

        if state.is_in_check(im_at_move):
            # Next player is in check, what about mate?
            if state.is_in_checkmate(im_at_move):
                # Am I the next player?
                if im_at_move:
                    # This is bad for me
                    return -200
                else:
                    # This is great for me
                    return 200

            # Am I the one in check?
            if im_at_move:
                # Being in check is bad
                return -100
            else:
                # Checking the opponent is great
                return 100
        elif state.is_draw():
            # A draw is a draw, and it's boring
            return 0

        piece_values = {PieceType.PAWN: 1, PieceType.KNIGHT: 3, PieceType.BISHOP: 3, PieceType.ROOK: 5,
                        PieceType.QUEEN: 9, PieceType.KING: 0}
        my_value = 0
        their_value = 0

        for key, value in state.pieces.items():
            my_value += piece_values[value.type]

        for key, value in state.enemy_pieces.items():
            their_value += piece_values[value.type]

        return my_value - their_value

    @staticmethod
    def board_loc_to_rank_file(board_loc):
        return 8 - board_loc[0], chr(ord("a") + board_loc[1])

    @staticmethod
    def rank_file_to_board_loc(rank_file):
        return 8 - rank_file[0], ord(rank_file[1]) - ord("a")

    def state_after_move(self, state, move, me=True):
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

        # Todo: Deal with this
        new_state.en_passant_enemy = state.en_passant_enemy
        new_state.en_passant_ally = state.en_passant_ally

        new_state.enemy_king_board_location = state.enemy_king_board_location
        new_state.king_board_location = state.king_board_location

        my_pieces = new_state.pieces if me else new_state.enemy_pieces
        their_pieces = new_state.enemy_pieces if me else new_state.pieces

        # Copy the ply value and add one to it (This will get reset if conditions match)
        new_state.ply_since_capture_or_pawn_movement = state.ply_since_capture_or_pawn_movement + 1

        # Copy over the previous moves
        new_state.previous_moves = deepcopy(state.previous_moves)

        # Copy the ply since promotion value and increment it
        new_state.ply_since_promotion = state.ply_since_promotion + 1

        # Apply the move
        # TODO: Make this player-agnostic
        piece = my_pieces[move.piece_moved_id]

        # Update king_board_location if necessary
        if piece.type == PieceType.KING:
            if me:
                new_state.king_board_location = move.board_location_to
            else:
                new_state.enemy_king_board_location = move.board_location_to

            delta_file = move.board_location_to[1] - move.board_location_from[1]
            rank = move.board_location_from[0]
            if delta_file == 2:
                # Kingside castle

                # Grab the rook we know is at file h
                rook = new_state.board[(rank, 7)]

                # Castle it internally
                rook.board_location = rank, 5
                rook.rank_file = AI.board_loc_to_rank_file(rook.board_location)

                # Remove it from the board
                del new_state.board[(rank, 7)]

                # Put it in its new location
                new_state.board[rook.board_location] = rook
                del rook
            elif delta_file == -2:
                # Queenside castle

                # Grab the rook we know is at file a
                rook = new_state.board[(rank, 0)]

                # Castle it internally
                rook.board_location = rank, 3
                rook.rank_file = AI.board_loc_to_rank_file(rook.board_location)

                # Remove it from the board
                del new_state.board[(rank, 0)]

                # Put it in its new location
                new_state.board[rook.board_location] = rook
                del rook

        # Apply this move to the internal state
        del new_state.board[piece.board_location]
        piece.board_location = move.board_location_to

        if piece.type == PieceType.PAWN:
            # Reset ply value
            new_state.ply_since_capture_or_pawn_movement = 0
            delta_rank = abs(move.board_location_to[0] - move.board_location_from[0])
            if delta_rank == 2:
                # Possibility of being en passant captured
                if me:
                    new_state.en_passant_ally = piece, (move.board_location_to[0] + self.player.rank_direction,
                                                        move.board_location_to[1])
                else:
                    new_state.en_passant_enemy = piece, (move.board_location_to[0] - self.player.rank_direction,
                                                         move.board_location_to[1])
            elif move.promote_to != "":
                # Promotion occurred!

                # Reset promotion flag
                new_state.ply_since_promotion = 0

                # Remove it from our piece dict
                del my_pieces[str(piece)]

                # Promote it
                piece.type = PieceType[move.promote_to.upper()]

                # Put it back
                my_pieces[str(piece)] = piece

        if move.piece_captured_id is not None:
            # Reset ply value
            new_state.ply_since_capture_or_pawn_movement = 0

            # There was something there, grab its id then remove it

            # Wipe it from the board (takes into account the en passant capture where you don't move onto the space
            # of the piece you capture
            del new_state.board[their_pieces[move.piece_captured_id].board_location]
            del their_pieces[move.piece_captured_id]

        piece.rank_file = AI.board_loc_to_rank_file(move.board_location_to)
        new_state.board[piece.board_location] = piece
        piece.has_moved = True

        # Reset the en passant enemy because regardless of whether or not we captured it, en passant no longer exists
        if me:
            new_state.en_passant_enemy = None
        else:
            new_state.en_passant_ally = None

        # Add the move that put us in this state
        new_state.move_made = move

        # Set whether each piece is in check. These calls return, but also set internal lookup
        new_state.is_in_check(True)
        new_state.is_in_check(False)

        # Add the move that generated this state to the list of moves
        new_state.previous_moves.append(move)

        # Appending this move pushed it over 8 moves
        if len(new_state.previous_moves) == 9:
            # Delete the oldest state
            del new_state.previous_moves[0]

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

    def valid_moves_for_piece(self, piece, state, me=True):
        # Set player-at-move-specific things
        rank_direction = -self.player.rank_direction if me else -self.player.opponent.rank_direction
        opponent_color = self.player.opponent.color if me else self.player.color

        valid_moves = []
        extra_moves = []
        if piece.type == PieceType.PAWN:
            r, c = piece.board_location

            # Two space pawn movement
            if not piece.has_moved:
                # Move it two spaces
                m = ChessMove()
                m.piece_moved_id = str(piece)
                m.board_location_from = r, c
                m.board_location_to = (r + rank_direction * 2, c)

                extra_moves.append(m)
        elif piece.type == PieceType.KING:
            if not piece.has_moved and len(state.is_board_location_under_attack(piece.board_location, opponent_color)) \
                    == 0:
                # King hasn't moved and we aren't in check currently, good

                # Let the move checker mess with the details
                for m_t in [(0, -2), (0, 2)]:
                    # Throw them in the extra moves list
                    r, c = piece.board_location

                    m = ChessMove()
                    m.piece_moved_id = str(piece)
                    m.board_location_from = piece.board_location
                    m.board_location_to = r, c + m_t[1]

                    extra_moves.append(m)

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

                    if self.is_valid(m, state, me):
                        # Convert it to a state
                        s = self.state_after_move(state, m, me)

                        # If i'm not in check
                        if not s.is_in_check(me):
                            if piece.type == PieceType.PAWN:
                                # Check for promotion
                                if (opponent_color == "White" and m.board_location_to[0] == 7) or \
                                   (opponent_color == "Black" and m.board_location_to[0] == 0):
                                    # White or Black pawn promoting
                                    for piece_type in ["Queen", "Rook", "Bishop", "Knight"]:
                                        new_move = ChessMove()
                                        new_move.piece_moved_id = m.piece_moved_id
                                        new_move.piece_captured_id = m.piece_captured_id
                                        new_move.board_location_from = m.board_location_from
                                        new_move.board_location_to = m.board_location_to
                                        new_move.promote_to = piece_type
                                        new_move.en_passant = m.en_passant
                                        new_move.castling = m.castling

                                        valid_moves.append(self.state_after_move(state, new_move, me))
                                else:
                                    valid_moves.append(s)
                            else:
                                valid_moves.append(s)
                    else:
                        # If it's invalid for a certain step, certainly all subsequent steps will be invalid
                        break
        # Take care of any extra moves
        for m in extra_moves:
            if self.is_valid(m, state, me):
                s = self.state_after_move(state, m, me)
                if not s.is_in_check(me):
                    valid_moves.append(s)

        return valid_moves

    def is_valid(self, move, state, me=True):
        # Player-at-move-specific things
        rank_direction = -self.player.rank_direction if me else -self.player.opponent.rank_direction
        en_passant_enemy = state.en_passant_enemy if me else state.en_passant_ally
        enemy_color = self.player.opponent.color if me else self.player.color
        pieces = state.pieces if me else state.enemy_pieces

        piece = pieces[move.piece_moved_id]
        r, c = move.board_location_to

        # Common sense check; is this space even on the board?
        if not (0 <= r < 8 and 0 <= c < 8):
            return False

        if piece.type == PieceType.PAWN:
            delta_row = move.board_location_to[0] - piece.board_location[0]

            if delta_row / abs(delta_row) != rank_direction:
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
                if en_passant_enemy is not None:
                    # Are we moving there?
                    if move.board_location_to == en_passant_enemy[1]:
                        move.piece_captured_id = str(en_passant_enemy[0])
                        move.en_passant = True
                        return True

                # Guess not
                if move.board_location_to in state.board.keys():
                    # Something is there
                    other_piece = state.board[move.board_location_to]

                    if other_piece.color == enemy_color:
                        # Get 'em
                        move.piece_captured_id = str(other_piece)
                        return True

            # It's moving forward one
            else:
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
        elif piece.type == PieceType.KING and not piece.has_moved and \
                abs(move.board_location_from[1] - move.board_location_to[1]) == 2:
            # Castling move
            delta_file = move.board_location_from[1] - move.board_location_to[1]

            # Kingside castle attempt
            if delta_file == -2:
                # Is there something at (rank, 7)?
                if (move.board_location_from[0], 7) in state.board.keys():
                    # Is it a rook?
                    if state.board[(move.board_location_from[0], 7)].type == PieceType.ROOK:
                        rook = state.board[(move.board_location_from[0], 7)]

                        # Is it ours?
                        if rook.color != enemy_color:
                            # Has it moved yet?
                            if not rook.has_moved:
                                # Castling will work in theory, just need to check intermediate squares
                                square2 = move.board_location_to

                                # Average the file values to get the middle
                                square1 = rook.board_location[0], \
                                          (move.board_location_to[1] + move.board_location_from[1]) / 2

                                # Are the intermediate squares empty?
                                if square1 not in state.board.keys() and square2 not in state.board.keys():
                                    # Is either space under attack?
                                    if not state.is_board_location_under_attack(square1, enemy_color) and \
                                            not state.is_board_location_under_attack(square2, enemy_color):
                                        move.castling = True
                                        return True
                return False
            else:
                # Queenside castle attempt

                # Is there something at (rank, 0)?
                if (move.board_location_from[0], 0) in state.board.keys():
                    # Is it a rook?
                    if state.board[(move.board_location_from[0], 0)].type == PieceType.ROOK:
                        rook = state.board[(move.board_location_from[0], 0)]

                        # Is it ours?
                        if rook.color != enemy_color:
                            # Has it moved yet?
                            if not rook.has_moved:
                                # Castling will work in theory, just need to check intermediate squares
                                square2 = move.board_location_to

                                # Average the file values to get the middle
                                square1 = rook.board_location[0], 3

                                # Queenside castles need to check 3 squares
                                square3 = rook.board_location[0], 1

                                # Are the intermediate squares empty?
                                if square1 not in state.board.keys() and square2 not in state.board.keys() and \
                                        square3 not in state.board.keys():
                                    # Is either space under attack?
                                    if not state.is_board_location_under_attack(square1, enemy_color) and \
                                            not state.is_board_location_under_attack(square2, enemy_color) and \
                                            not state.is_board_location_under_attack(square3, enemy_color):
                                        move.castling = True
                                        return True
                return False
        else:
            # Some other piece

            # Is the target location occupied?
            if move.board_location_to in state.board.keys():
                # Is it an ally?
                piece_on_target_loc = state.board[move.board_location_to]

                if piece_on_target_loc.color == piece.color:
                    # Can't capture our own pieces
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

        piece_id += str(piece.id).zfill(2)

        return piece_id

    @staticmethod
    def print_board(state):
        """Prints the current board using pretty ASCII art
        Note: you can delete this function if you wish
        """

        # iterate through the range in reverse order
        for r in range(9, -2, -1):
            output = ""
            if r == 9 or r == 0:
                # then the top or bottom of the board
                output = "   +----------------------------------------+"
            elif r == -1:
                # then show the ranks
                output = "      0    1    2    3    4    5    6    7"
            else:  # board
                output = " " + str(8 - r) + " |"
                # fill in all the files with pieces at the current rank
                for file_offset in range(0, 8):
                    # start at a, with with file offset increasing the char
                    f = file_offset
                    current_piece = None
                    if (8 - r, f) in state.board.keys():
                        current_piece = state.board[(8 - r, f)]

                    code = " . "  # default "no piece"
                    if current_piece is not None:
                        # the code will be the first character of their type
                        # e.g. 'Q' for "Queen"
                        code = str(current_piece)

                    output += " " + code + " "

                output += "|"
            print(output)
