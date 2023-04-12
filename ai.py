"""
COMP.CS.100
Author: Oskari Heinonen

Basic chess ai
"""


import game as gm
import random
import copy


def evaluate_position(board):
    """Returns a tuple which contains the sum of the piece's values
    for white and black respectively.

    :param board: list, board data structure
    :return: tuple, material value of the position (white, black)
    """
    
    piece_values = {
    "p": 1, "P": 1,
    "n": 3, "N": 3,
    "b": 3, "B": 3,
    "r": 5, "R": 5,
    "q": 9, "Q": 9,
    "k": 100, "K": 100
    }
    
    white_pieces = [piece for row in board 
                    for piece in row if piece is not None and piece.isupper()]
    black_pieces = [piece for row in board 
                    for piece in row if piece is not None and piece.islower()]
    
    white_value = 0
    black_value = 0

    for i in white_pieces:
        white_value += piece_values[i]

    for j in black_pieces:
        black_value += piece_values[j]
    

    return white_value, black_value


def piece_squares(board, color):
    """Returns the squares' coordinates in which there are pieces of the
    specified color.

    :param board: list, board data structure to be iterated
    :param color: str, color of the pieces to be checked for
    :return: list, list of pieces' coordinates
    """

    if color == "white":
        piece_squares = \
        [(rc, cc) for rc, row in enumerate(board)
        for cc, piece in enumerate(row) if piece is not None and piece.isupper()]
        return piece_squares

    elif color == "black":
        piece_squares = \
        [(rc, cc) for rc, row in enumerate(board)
        for cc, piece in enumerate(row) if piece is not None and piece.islower()]
        return piece_squares

    else:
        raise ValueError("Invalid color")    


def random_move(game, board, color):
    """Makes a random legal move.
    
    :param game: Game, game-object
    :param board: list, board before the move
    :param color: str, color of the piece to be moved
    """
    
    while True:
        rand_new_y, rand_new_x = random.randint(0,7), random.randint(0,7)
        rand_new_pos = (rand_new_y, rand_new_x)
        rand_old_pos = random.choice(piece_squares(board, color))
        # If the move is legal, make it, and break
        if game.move_is_legal(rand_old_pos, rand_new_pos, test=True):
            game.move_piece(rand_old_pos, rand_new_pos, test=False)
            break


def calculated_move(game, board, color):
    """Calculates the best legal move (currently only for black).
    Calculations are based on trying to make a move that allows
    the enemy to capure the least amount of material on the next move.
    If there are multiple "best moves", return a random one among them.
    Returns (None, None) if it's checkmate.

    :param game: Game, game-object
    :param board: list, board before the move
    :param color: str, color of the piece to be moved
    :return: tuple, (moved piece's coordinates, target square's coordinates)
                    or (None, None) if checkmate
    """

    old_board = copy.deepcopy(board)
    
    if color == "white":
        return None
    
    elif color == "black":
        
        # Will contain moves (old_pos, new_pos) as keys and lowest 
        # black's position's evaluation after trying all
        # white's moves on that position
        move_eval = {}

        # Loop trough all legal black moves
        black_squares = piece_squares(old_board, "black")
        for old_pos in black_squares:
            for i in range(8):
                for j in range(8):
                    new_pos = (i, j)
                    # TODO: fix old_board updating here
                    if game.move_is_legal(old_pos, new_pos, test=True):
                        piece = old_board[old_pos[0]][old_pos[1]]
                        new_board = copy.deepcopy(old_board)
                        new_board[old_pos[0]][old_pos[1]] = None
                        new_board[new_pos[0]][new_pos[1]] = piece

                        # old_board = board before any moves
                        # new_board = board after black's
                        # random move (first move)

                        # Loop through white's all possible moves 
                        # and get black's position evaluation for each
                        while True:
                            # Positions of white pieces after
                            # black's random move
                            squares = piece_squares(new_board, "white")
                            # Black evaluation values list
                            black_evaluations = []
                            # Set the board after black's move as
                            # the board to the game object
                            game.set_position_list(new_board)
                            tmp_board = copy.deepcopy(new_board)
                            # For each white piece
                            for white_pos in squares:
                                # Loop throug all squares on the board
                                for i in range(8):
                                    for j in range(8):
                                        # Move the white piece to that square
                                        # if the move is legal
                                        if game.move_piece(white_pos, (i, j), test=True):
                                            # Evaluate black's material after
                                            # white's move and add the value
                                            # to the list
                                            black_evaluations.append(
                                            evaluate_position(
                                                game.get_board())[1])
                                            new_board = copy.deepcopy(
                                                tmp_board)
                                            # Set the position back to
                                            # how it was before white's move
                                            game.set_position_list(new_board)
                                        else:
                                            continue
                            move_eval[(old_pos, new_pos)] = \
                            min(black_evaluations)

                            game.set_position_list(old_board)
                            break

        # Find the maximum value in the dictionary
        max_value = max(move_eval.values())
        if max_value < 100:
            return None, None

        # Create a list of positions that have the maximum value
        max_keys = [key for key, value in move_eval.items() 
                    if value == max_value]

        # Choose a random position from the list of
        # positions with the maximum value
        best_move = random.choice(max_keys)
        return best_move
