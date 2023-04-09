import game as gm
import random


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
    "k": 0, "K": 0
    }
    
    white_pieces = [piece for row in board for piece in row if piece is not None and piece.isupper()]
    black_pieces = [piece for row in board for piece in row if piece is not None and piece.islower()]
    
    white_value = 0
    black_value = 0

    for i in white_pieces:
        white_value += piece_values[i]

    for j in black_pieces:
        black_value += piece_values[j]
    
    return white_value, black_value


def random_move(game, board):
    """
    """
    black_piece_squares = \
    [(rc, cc) for rc, row in enumerate(board)
    for cc, piece in enumerate(row) if piece is not None and piece.islower()]
    
    while True:
        rand_new_y, rand_new_x = random.randint(0,7), random.randint(0,7)
        rand_new_pos = (rand_new_y, rand_new_x)
        rand_old_pos = random.choice(black_piece_squares)
        if game.move_piece(rand_old_pos, rand_new_pos):
            return board




def main():
    game = gm.Game()
    game.set_position()
    board = game.get_board()
    print(evaluate_position(board))

if __name__ == "__main__":
    main()
