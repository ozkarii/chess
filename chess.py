"""
COMP.CS.100 
Tekijä: Oskari Heinonen
Opiskelijanumero: 151242115

Chess
"""


import tkinter as tk
import os

class Gui:
    """
    """
    def __init__(self, board):
        """Initializes the gui-object with an empty chessboard
        and a menu.
        """
        
        self.__board = board
        self.__mainwindow = tk.Tk()
        self.__piece_images = {}

        # Save the piece images into a dict
        # Value is a PhotoImage -object
        for i in os.listdir("pieces/Cburnett"):
            self.__piece_images[i.replace(".png","")] = \
            tk.PhotoImage(file=f"pieces/Cburnett/{i}")
        
        # Squares
        self.__squares = []
        for x in range(1,9):
            self.__row = []
            for y in range(1,9):
                self.__square = tk.Button(self.__mainwindow,\
                    width=10, height=5, borderwidth=0, bg="#f0e1c7")
                self.__square.grid(row=x, column=y)
                if x % 2 == 0 and y % 2 != 0:
                    self.__square.config(bg="#a1784f")
                elif x % 2 != 0 and y % 2 == 0:
                    self.__square.config(bg="#a1784f")
                self.__row.append(self.__square)
            self.__squares.append(self.__row)

        # Menubar
        self.__menubar = tk.Menu(self.__mainwindow)

        # Game menu
        self.__game_menu = tk.Menu(self.__menubar)
        self.__game_menu.add_command(label="Load position")
        self.__game_menu.add_command(label="Reset position")
        self.__menubar.add_cascade(menu=self.__game_menu, label="Game")
        
        # Settings menu
        self.__settings_menu = tk.Menu(self.__menubar)
        self.__settings_menu.add_command(label="Game")
        self.__settings_menu.add_command(label="Style")
        self.__settings_menu.add_command(label="Network")
        self.__menubar.add_cascade(menu=self.__settings_menu, label="Settings")


        self.__mainwindow.config(menu=self.__menubar)
        

        # Labels
        for y in range(1,9):
            y_label = tk.Label(self.__mainwindow, text=str(y))
            y_label.grid(column=9, row=y)

        letters = ["A","B","C","D","E","F","G","H"]

        for x in range(1,9):
            x_label = tk.Label(self.__mainwindow, text=letters[x - 1])
            x_label.grid(column=x, row=9)



        # This should be its own method when I figure out
        # how to update the gui after init
        for row_count, row in enumerate(self.__board):
            for columnn_count, square in enumerate(row):
                if square != None:
                    # PhotoImage -object needs to be assigned to a variable
                    # because of garbage collection.
                    image_file = f"pieces/Cburnett/{str(board[row_count][columnn_count])}.png"

                    self.__squares[row_count][columnn_count].config(
                        image=self.__piece_images[f"{str(board[row_count][columnn_count])}"],
                        width=75,
                        height = 75
                        )
                else:
                    continue
    

        self.__mainwindow.mainloop()        


    def load_position(self, board):
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
        return f"{self.__color}_{self.__category}"



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


def set_position(board, pieces, fen_string):
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
                board[row][column] = pieces[char]
                column += 1


def print_board(board):
    """for debug purposes
    """
    set_position(board, pieces, START_POSITION)
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
    set_position(board, pieces, START_POSITION)
    print_board(board)
    gui = Gui(board)
    

if __name__ == '__main__':
    main()