"""
COMP.CS.100 
Tekijä: Oskari Heinonen
Opiskelijanumero: 151242115

Chess
"""


import tkinter as tk

class Gui:
    """
    """
    def __init__(self):
        """Initializes the gui-object with an empty chessboard
        and a menu.
        """
        self.__mainwindow = tk.Tk()
        self.__buttons = []
        for x in range(1,9):
            self.__row = []
            for y in range(1,9):
                self.__button = tk.Button(self.__mainwindow,\
                    width=10, height=5, borderwidth=1)
                self.__button.grid(row=x, column=y)
                if x % 2 == 0 and y % 2 != 0:
                    self.__button.config(bg="brown")
                elif x % 2 != 0 and y % 2 == 0:
                    self.__button.config(bg="brown")
                self.__row.append(self.__button)
            self.__buttons.append(self.__row)

        self.__menubar = tk.Menu(self.__mainwindow)
        self.__file_menu = tk.Menu(self.__menubar)
        self.__file_menu.add_command(label="Load position")
        self.__menubar.add_cascade(menu=self.__file_menu, label="File")
        self.__mainwindow.config(menu=self.__menubar)
        self.__mainwindow.mainloop()        


    def set_position(self, board):
        """Sets the pieces to the correct places given by 
        the <board> parameter.

        :param board: list, pieces in the data structure
        """
        



class Piece:
    """
    """
    def __init__(self, category, color):
        self.__category = category
        self.__color = color

    def get_category(self):
        """
        """
        return self.__category
    
    def get_color(self):
        """
        """
        return self.__color
    
    def __str__(self):
        """
        """
        return f"{self.__color} {self.__category}"



# Data structure which holds the positional information of the pieces
board = [
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None]
        ]

def threatened_pieces(piece, board):
    """Returns a list of pieces which are threathened by the parameter piece.
    """
    return
    
def legal_moves(piece, board):
    return


def in_check(piece):
    """
    """
    if piece.get_category() == "king":
        return False

    else:
        return None

START_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

# Lowercase = black , uppercase = white
pieces = {
        "p": Piece("pawn", "b"), "P": Piece("pawn", "w"),
        "n": Piece("knight", "b"), "N": Piece("knight", "w"),
        "b": Piece("bishop", "b"), "B": Piece("bishop", "w"),
        "r": Piece("rook", "b"), "R": Piece("rook", "w"),
        "q": Piece("queen", "b"), "Q": Piece("queen", "w"),
        "k": Piece("king", "b"), "K": Piece("king", "w")
        }


def load_position(board, pieces, fen_string):
    row = 0
    column = 0
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
                column += int(char)

            else:
                print(row)

                board[row][column] = pieces[char]
                column += 1


def print_board(board):
    """for debug purposes
    """
    load_position(board, pieces, START_POSITION)
    count = 0
    for row in board:
        for piece in row:
            if count == 7:
                print("{:<8}".format(str(piece)))
                
                count = 0
            else:
                print("{:<8}".format(str(piece)), end=" ")
                count += 1

def main():
    load_position(board, pieces, START_POSITION)
    print_board(board)
    gui = Gui()

if __name__ == '__main__':
    main()