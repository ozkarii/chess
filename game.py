"""
COMP.CS.100 
Tekijä: Oskari Heinonen

Chess game logic
"""


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


    def list_to_fen(self):
        """Coverts the position information in <self.__board> 
        into a FEN-string.
        :param board: list, data structure for holding positional information
        :return: str, position as FEN-string
        """
        output_fen = ""
        empty_square_count = 0
        column_count = 0
        row_count = 0
        for row in self.__board:
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
    

    def move_piece(self, old_pos, new_pos):
        """Takes in the old and new positions of the piece to be moved
        as a tuple: (row, column) and moves the piece in <self.__board>
        accordingly.

        :param old_pos: tuple, old position (row, column)
        :param new_pos: tuple, new position (row, column)
        """
        
        piece = self.__board[old_pos[0]][old_pos[1]]
        self.__board[old_pos[0]][old_pos[1]] = None
        self.__board[new_pos[0]][new_pos[1]] = piece


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
