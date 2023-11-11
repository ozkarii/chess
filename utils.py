import copy
    
def transpose(matrix):
        """Returns the transpose of the chessboard

        :param matrix: list, matrix-like list[list[]] data-structure
        :return: list, input matrix's transpose
        """

        num_rows = len(matrix)
        num_cols = len(matrix[0])
        transposed_board = [[None] * num_rows for _ in range(num_cols)]
        for i in range(num_rows):
            for j in range(num_cols):
                transposed_board[j][i] = matrix[i][j]
        
        return transposed_board
    
def flip_board(board):
    """Flips
    """

    new_board = copy.deepcopy(board)

    for row in new_board:
        row.reverse()
    
    new_board.reverse()

    return new_board

def flip_coordinate(coord):
    """Mirrors the coordinate in the number line [0,7].
    For example: 0 -> 7,  2 -> 5,  4 -> 3

    :param coord: coordinate to be flipped
    :return: int, the new coordinate
    """
    
    if coord <= 3:
        return 7 - coord
    else:
        return abs(coord - 7)