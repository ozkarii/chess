

# Maybe have an instance of Game class for each game.
# When a new game is started create new Game object.
class Game():
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

        
        self.__pieces = "pPnNbBrRqQkK"


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



    def record_move(self):
        return


    def threatened_pieces(piece, board):
        """Returns a list of pieces which are threathened by the parameter piece.
        """
        return
    

    def legal_moves(piece, board):
        """
        """
        return


    def in_check(piece):
        """
        """
        if piece.get_category() == "king":
            return None
        else:
            return None
        

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
