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
        """
        print(old_pos, new_pos)
        # #TODO: needs variable for old board
        # For quicker access:
        old_x = old_pos[1]
        old_y = old_pos[0]
        new_x = new_pos[1]
        new_y = new_pos[0]

        old_board = self.__board
        old_square = old_board[old_y][old_x]
        
        # False if same square
        if old_pos == new_pos:
            return False
        
        # White pawn
        elif old_square == "P":
            if new_y - old_y == -1 and new_x == old_x:
                if old_board[new_y][new_x] == None:
                    return True
                else:
                    return False
            elif new_y - old_y == -1 and abs(new_x - old_x) == 1:
                if old_board[new_y][new_x] != None:
                    return True
                else:
                    return False
            elif old_y == 6 and new_y - old_y == -2 and new_x == old_x and \
                 old_board[old_y + - 1][old_x] == None:
                if old_board[new_y][new_x] == None:
                    return True
                else:
                    return False

            
        # Black pawn
        elif old_square == "p":
            if new_y - old_y == 1 and new_x == old_x:
                if old_board[new_y][new_x] == None:
                    return True
                else:
                    return False
            elif new_y - old_y == 1 and abs(new_x - old_x) == 1:
                if old_board[new_y][new_x] != None:
                    return True
                else:
                    return False
            elif old_y == 1 and new_y - old_y == 2 and new_x == old_x and \
                 old_board[old_y + 1][old_x] == None:
                if old_board[new_y][new_x] == None:
                    return True
                else:
                    return False
                
        # Rook
        elif old_square in ("r", "R"):
            if new_x == old_x or new_y == old_y:
                if new_y == old_y:
                    if new_x > old_x:
                        for i in range(old_x + 1, new_x):
                            if old_board[old_y][i] != None:
                                print(i)
                                return False
                        return True
                    
                    elif new_x < old_x:
                        for i in range(new_x, old_x - 1):
                            if old_board[old_y][i] != None:
                                print(i)
                                return False
                        return True
            else:
                return False
        
        # Bishop
        


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
