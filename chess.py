"""
COMP.CS.100 
Tekijä: Oskari Heinonen
Opiskelijanumero: 151242115

Chess gui
"""

import tkinter as tk
import os


class Gui:
    """
    """
    def __init__(self):
        
        """Initializes the gui-object with an empty chessboard
        and a menu.
        """
        
        self.__mainwindow = tk.Tk()
        self.__piece_images = {}
        self.__empty_image = tk.PhotoImage("pieces/empty.png")
        self.__new_color = "lightblue"

        # Save the piece images into a dict
        # Value is a PhotoImage -object
        # PhotoImage -object needs to be assigned to a variable
        # because of garbage collection.
        for i in os.listdir("pieces/Cburnett"):
            self.__piece_images[i.replace(".png","")] = \
            tk.PhotoImage(file=f"pieces/Cburnett/{i}")
        
        # Squares
        self.__squares = []
        for x in range(1,9):
            self.__row = []
            for y in range(1,9):
                self.__square = tk.Button(
                    self.__mainwindow, width=10, height=5, 
                    borderwidth=0, bg="#f0e1c7",
                    )
                self.__square.grid(row=x, column=y)
                if x % 2 == 0 and y % 2 != 0:
                    self.__square.config(bg="#a1784f")
                elif x % 2 != 0 and y % 2 == 0:
                    self.__square.config(bg="#a1784f")
                self.__row.append(self.__square)
            self.__squares.append(self.__row)

        # Adds commands to all buttons
        for row_count, row in enumerate(self.__squares):
            for column_count, square in enumerate(row):
                square.config(command=lambda row=row_count, 
                              column=column_count: self.change_square_color(row, column)
                              )

        # Menubar
        self.__menubar = tk.Menu(self.__mainwindow)

        # Game menu
        self.__game_menu = tk.Menu(self.__menubar)
        self.__game_menu.add_command(label="Load position", 
                                     command=self.load_position_popup)
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
            y_label = tk.Label(self.__mainwindow, 
                               text=str(y), font=("Arial", 12)
                               )
            y_label.grid(column=9, row=y)
        letters = ["A","B","C","D","E","F","G","H"]
        for x in range(1,9):
            x_label = tk.Label(self.__mainwindow, 
                               text=letters[x - 1], font=("Arial", 12)
                               )
            x_label.grid(column=x, row=9)
        

    def change_square_color(self, row, column):
        """Changes the color of a square in the chessboard.

        :param row: int, row index of the square
        :param column: int, column index of the square
        """

        current_color = self.__squares[row][column].cget("bg")
        if current_color == "#f0e1c7" or current_color == "#a1784f":
            # Find the current new_color square, if any
            new_color_square = None
            for i in range(0,8):
                for j in range(0,8):
                    if self.__squares[i][j].cget("bg") == self.__new_color:
                        new_color_square = (i, j)
                        break
                if new_color_square:
                    break

            # If there's already a new_color square, change it to the original color
            if new_color_square:
                previous_row = new_color_square[0]
                previous_column = new_color_square[1]
                if previous_row % 2 == 0 and previous_column % 2 != 0:
                    self.__squares[previous_row][previous_column].config(bg="#a1784f")
                elif previous_row % 2 != 0 and previous_column % 2 == 0:
                    self.__squares[previous_row][previous_column].config(bg="#a1784f")
                else:
                    self.__squares[previous_row][previous_column].config(bg="#f0e1c7")

            # Set the clicked square to new_color
            self.__squares[row][column].config(bg=self.__new_color)
        
        # If the clicked square is in new_color, set it to the original color
        else:
            if row % 2 == 0 and column % 2 != 0:
                self.__squares[row][column].config(bg="#a1784f")
            elif row % 2 != 0 and column % 2 == 0:
                self.__squares[row][column].config(bg="#a1784f")
            else:
                self.__squares[row][column].config(bg="#f0e1c7")


    def load_position_popup(self):
        """Opens a popup window for loading a position.
        """
        # TODO: Needs error handling for when the FEN string is invalid.

        popup = tk.Toplevel(self.__mainwindow)
        popup.title("Load position")
        popup.geometry("500x150")
        usr_input = tk.StringVar(popup)
        entry = tk.Entry(popup,textvariable=usr_input, width=65)
        entry.grid(padx=50, pady=50, row=0, column=0)
        load_button = tk.Button(
                      popup, text="Load", 
                      command=lambda: [
                            set_position(board, pieces, entry.get()),
                            self.load_position(board)]
                      )
        load_button.grid(row=1, column=0)


    
    def load_position(self, board):
        """Sets the pieces to the correct places given by 
        the <board> parameter.

        :param board: list, pieces in the data structure
        """
        
        for row_count, row in enumerate(board):
            for columnn_count, square in enumerate(row):
                if square != None:
                    self.__squares[row_count][columnn_count].config(
                        image=self.__piece_images[
                        f"{str(board[row_count][columnn_count])}"],
                        width=75,
                        height = 75
                        )
                else:
                    self.__squares[row_count][columnn_count].config(
                        image=self.__empty_image,
                        width= 75,
                        height = 75
                        )


    def mainloop(self):
        self.__mainwindow.mainloop()


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

START_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

pieces = {
        "p": Piece("pawn", "b"), "P": Piece("pawn", "w"),
        "n": Piece("knight", "b"), "N": Piece("knight", "w"),
        "b": Piece("bishop", "b"), "B": Piece("bishop", "w"),
        "r": Piece("rook", "b"), "R": Piece("rook", "w"),
        "q": Piece("queen", "b"), "Q": Piece("queen", "w"),
        "k": Piece("king", "b"), "K": Piece("king", "w")
        }


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


def set_position(board, pieces, fen_string):
    """Interprates position information in Forsyth-Edwards Notation
    given in <fen_string> and places the pieces to the right places
    in <board>.

    :param board: list[Piece | None], data structure which holds the 
                  positional information of pieces.
    :param pieces: dict{str: Piece}, data structure which maps characters used 
                   in FEN to the corresponding Piece-objects 
    :param fen_string: str, position information in Forsyth-Edwards
                       Notation (FEN)
    """
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
                for i in range(column, column + int(char)):
                    board[row][i] = None
                column += int(char)
            else:
                board[row][column] = pieces[char]
                column += 1


def print_board(board):
    """for debug purposes
    """
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
    gui = Gui()
    gui.load_position(board)
    gui.mainloop()
    set_position(board, pieces, "4R3/8/8/2Pkp3/N7/4rnKB/1nb5/b1r5")
    print_board(board)

if __name__ == '__main__':
    main()