"""
COMP.CS.100 
Tekijä: Oskari Heinonen

Chess game logic
"""

# TODO: checking for check could be implemented by checking if capturing
# the king is a legal move
# TODO: make capturing own pieces illegal
# TODO: moving one square diagonally is not allowed for bishop and queen

class Game:
    """This class handles the game logic (moves, captures, turns etc.)
    """

    START_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

    def __init__(self):
        """Initializes necessary things for the game
        """
        # Data structure which holds the positional information of the pieces
        self.__board = [
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None]
        ]

        # Data structure which records moves
        self.__moves = []


    def get_board(self):
        """Returns the current board
        
        :return: list, board data structure
        """
        return self.__board
    
    
    def set_position(self, fen_string = START_POSITION):
        """Interprates position information in Forsyth-Edwards Notation
        given in <fen_string> and places the pieces to the right places
        in <self.__board>.

        :param fen_string: str, position information in Forsyth-Edwards
                        Notation (FEN)
        :return: bool, True if <fen_string> was valid, False if not
        """
        row = 0
        column = 0

        if fen_string == "":
            return False
        else:
            try:
                while row < 8:
                    for char in fen_string:
                        if char == "/":
                            column = 0
                            row += 1
                        elif column == 8:
                            column = 0
                            row += 1
                        elif row == 8:
                            break
                        elif char.isnumeric():
                            for i in range(column, column + int(char)):
                                self.__board[row][i] = None
                            column += int(char)
                        else:
                            self.__board[row][column] = char
                            column += 1
                return True

            except (KeyError, ValueError, IndexError,):
                print("invalid")


    def list_to_fen(self, board):
        """Coverts the position information in <self.__board> 
        into a FEN-string.
        :param board: list, data structure for holding positional information
        :return: str, position as FEN-string
        """
        
        output_fen = ""
        empty_square_count = 0
        column_count = 0
        row_count = 0
        for row in board:
            for square in row:
                if column_count == 7:
                    output_fen += str(empty_square_count + 1)
                    if row_count != 7:
                        output_fen += "/"
                    column_count = 0
                    empty_square_count = 0
                elif isinstance(square, str):
                    if empty_square_count != 0:
                        output_fen += str(empty_square_count)
                    output_fen += square
                    empty_square_count = 0
                    column_count += 1
                else:
                    empty_square_count += 1
                    column_count += 1
            row_count += 1

        return output_fen
    

    def move_is_legal(self, old_pos, new_pos):
        """Returns True/False depending on the move's legitimity.
        
        :param old_pos: tuple, (row, column)
        :param new_pos: tuple, (row, column)
        """

        # For quicker access:
        old_y, old_x = old_pos
        new_y, new_x = new_pos

        # Old board is self.__board because when calling this function
        # the position hasn't changed yet
        old_board = self.__board

        old_square = old_board[old_y][old_x]
        

        transposed_board = self.transpose(old_board)
        

        def check_diagonal():
            """Checks if the new square is in the correct diagonal. 
            Also checks if there are other pieces on the diagonal from
            old to new position.

            :return: bool, True if diagonal is valid and False if not
            """

            if new_y < old_y and new_x < old_x:
                for i in range(1,8):
                    if (old_x - i, old_y - i) == (new_x, new_y):
                        if abs(new_x - old_x) == 1 and abs(new_y - old_y) == 1:
                            return True
                        else:
                            for j in range(1, old_x - new_x):
                                if old_board[old_y - j][old_x - j] is not None:
                                    return False
                                else: 
                                    return True
            
            elif new_y < old_y and new_x > old_x:
                for i in range(1,8):
                    if (old_x + i, old_y - i) == (new_x, new_y):
                        if abs(new_x - old_x) == 1 and abs(new_y - old_y) == 1:
                            return True
                        else:
                            for j in range(1, new_x - old_x):
                                if old_board[old_y - j][old_x + j] is not None:
                                    return False
                                else: 
                                    return True
            
            elif new_y > old_y and new_x < old_x:
                for i in range(1,8):
                    if (old_x - i, old_y + i) == (new_x, new_y):
                        if abs(new_x - old_x) == 1 and abs(new_y - old_y) == 1:
                            return True
                        else:
                            for j in range(1, old_x - new_x):
                                if old_board[old_y + j][old_x - j] is not None:
                                    return False
                                else: 
                                    return True
            
            elif new_y > old_y and new_x > old_x:
                for i in range(1,8):
                    if (old_x + i, old_y + i) == (new_x, new_y):
                        if abs(new_x - old_x) == 1 and abs(new_y - old_y) == 1:
                            return True
                        else:
                            for j in range(1, new_x - old_x):
                                if old_board[old_y + j][old_x + j] is not None:
                                    return False
                                else: 
                                    return True
            

        def check_straight():
            """Checks if move is straight along a row or a column
            and there are no other pieces on the way going straight from
            old to new position.

            :return: bool, True if no pieces; False if pieces
            """
            if new_y == old_y:
                if new_x > old_x:
                    for i in range(old_x + 1, new_x):
                        if old_board[old_y][i] is not None:
                            return False
                    return True
                elif new_x < old_x:
                    for i in range(new_x + 1, old_x):
                        if old_board[old_y][i] is not None:
                            return False
                    return True

            # This uses basically the same code as when new_y == old_y
            # except with a transposed board
            elif new_x == old_x:
                if new_y > old_y:
                    for i in range(old_y + 1, new_y):
                        if transposed_board[old_x][i] is not None:
                            return False
                    return True
                elif new_y < old_y:
                    for i in range(new_y + 1, old_y):
                        if transposed_board[old_x][i] is not None:
                            return False
                    return True
            else:
                return False


        # False if same square
        if old_pos == new_pos:
            return False
        
        # False if trying to capture own piece
        if old_board[new_y][new_x] is not None:
            if not old_square.islower() ^ old_board[new_y][new_x].islower():
                return False 
        
        # White pawn
        if old_square == "P":
            if new_y - old_y == -1 and new_x == old_x:
                if old_board[new_y][new_x] is None:
                    return True
                else:
                    return False
            elif new_y - old_y == -1 and abs(new_x - old_x) == 1:
                if old_board[new_y][new_x] is not None:
                    return True
                else:
                    return False
            elif old_y == 6 and new_y - old_y == -2 and new_x == old_x and \
                 old_board[old_y + - 1][old_x] is None:
                if old_board[new_y][new_x] is None:
                    return True
                else:
                    return False
            return False

        # Black pawn
        elif old_square == "p":
            if new_y - old_y == 1 and new_x == old_x:
                if old_board[new_y][new_x] is None:
                    return True
                else:
                    return False
            elif new_y - old_y == 1 and abs(new_x - old_x) == 1:
                if old_board[new_y][new_x] is not None:
                    return True
                else:
                    return False
            elif old_y == 1 and new_y - old_y == 2 and new_x == old_x and \
                 old_board[old_y + 1][old_x] is None:
                if old_board[new_y][new_x] is None:
                    return True
                else:
                    return False
            else:
                return False
                
        # Rook
        elif old_square in ("r", "R"):
            if check_straight():
                return True
            else:
                return False

        # Bishop
        elif old_square in ("b", "B"):
            if self.square_is_dark(old_y, old_x):
                if self.square_is_dark(new_y, new_x):
                    if check_diagonal():
                        return True
                    else:
                        return False
            else:
                if not self.square_is_dark(new_y, new_x):
                    if check_diagonal():
                        return True
                    else:
                        return False
                    
        # Queen
        elif old_square in ("q", "Q"):
            if old_x == new_x or old_y == new_y:
                if check_straight():
                    return True
                else:
                    return False
            elif self.square_is_dark(old_y, old_x) and \
                 self.square_is_dark(new_y, new_x):
                if check_diagonal():
                    return True
                else:
                    return False
            
            elif not self.square_is_dark(old_y, old_x) and \
                 not self.square_is_dark(new_y, new_x):
                if check_diagonal():
                    return True
                else:
                    return False

        # King
        elif old_square in ("k", "K"):
            if abs(old_x - new_x) <= 1 and abs(old_y - new_y) <= 1:
                return True
            else:
                return False

        # Knight
        elif old_square in ("n", "N"):
            if abs(old_x - new_x) == 2 and abs(old_y - new_y) == 1:
                return True
            elif abs(old_y - new_y) == 2 and abs(old_x - new_x) == 1:
                return True
            else:
                return False


    def move_piece(self, old_pos, new_pos):
        """Takes in the old and new positions of the piece to be moved
        as a tuple: (row, column) and moves the piece in <self.__board>
        accordingly.

        :param old_pos: tuple, old position (row, column)
        :param new_pos: tuple, new position (row, column)
        """
        
        if self.move_is_legal(old_pos, new_pos):
            piece = self.__board[old_pos[0]][old_pos[1]]
            self.__board[old_pos[0]][old_pos[1]] = None
            self.__board[new_pos[0]][new_pos[1]] = piece
            return True
        else:
            return False


    def square_is_dark(self, row, column):
        """Returns True if the given square is dark.
        
        :param row: int, square's row
        :param column: int, square's column
        """

        if row % 2 == 0 and column % 2 != 0:
            return True
        elif row % 2 != 0 and column % 2 == 0:
            return True
        else:
            return False


    def transpose(self, matrix):
        """Returns the transpose of a matrix-like list data structure
        such as self.__board.

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


    def print_board(self):
        """for debug purposes
        """
        count = 0
        for row in self.__board:
            for piece in row:
                if count == 7:
                    print("{:<8}".format(str(piece)))
                    count = 0
                else:
                    print("{:<8}".format(str(piece)), end=" ")
                    count += 1


from gui import *

def main():
    gui = Gui()
    gui.mainloop()
    

if __name__ == '__main__':
    main()
