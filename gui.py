"""
COMP.CS.100 
Tekijä: Oskari Heinonen

Chess gui
"""

import tkinter as tk
import os
from game import Game


class Gui:
    """This class handles the gui for the chess game.
    """

    # TODO: implement flipped board functionality

    def __init__(self):
        
        """Initializes the gui-object with an empty chessboard
        and a menu.
        """
        
        self.__mainwindow = tk.Tk()
        
        # Dict for mapping piece names to corresponding PhotoImage-objects
        self.__piece_images = {}
        
        # Define image-object for empty image
        self.__empty_image = tk.PhotoImage("pieces/empty.png")
        
        # Define the color to which the square clicked should turn into
        self.__new_color = "lightblue"
        
        # Init an instance of the game class to handle the logic
        self.__game = Game()
        
        # Sets the starting position
        self.__game.set_position()
        
        # True: next click will be the first meaning that clicking selects
        # the piece to be moved.
        # False: A piece has been selected and the next click will be for
        # moving that piece to the clicked square.
        self.__first_click = True
        
        
        # Save the piece images into a dict
        # Value is a PhotoImage -object
        # PhotoImage -object needs to be assigned to a variable
        # because of garbage collection.
        # The keys in self.__piece_images are named color_category
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
                              column=column_count: 
                              [self.move_piece(row, column),
                               self.change_square_color(row, column),
                               self.debug()
                               ])

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

        # Load start position
        self.load_position(self.__game.get_board())


    def change_square_color(self, row, column):
        """Changes the color of a square in the chessboard.

        :param row: int, row index of the square
        :param column: int, column index of the square
        """
        
        if self.__squares[row][column] == None:
            pass

        # If first_click == True, all squares should be normal color
        elif self.__first_click:
            for x_count, x in enumerate(self.__squares):
                for y_count, y in enumerate(x):
                    if x_count % 2 == 0 and y_count % 2 != 0:
                        y.config(bg="#a1784f")
                    elif x_count % 2 != 0 and y_count % 2 == 0:
                        y.config(bg="#a1784f")
                    else:
                        y.config(bg="#f0e1c7")
        else:
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
        # TODO: add error message when self.__game.set_position(entry.get())
        # returns False
        load_button = tk.Button(
                      popup, text="Load", 
                      command=lambda: [
                            self.__game.set_position(entry.get()),
                            self.load_position(self.__game.get_board())]
                      )
        load_button.grid(row=1, column=0)


    def load_position(self, board):
        """Sets the pieces to the correct places given by 
        the <board> parameter.

        :param board: list, pieces in the data structure
        """
        
        # This dict matches self.__piece_images's keys with FEN
        # which is used in <board>
        piece_dict = {
                "p": "b_pawn", "P": "w_pawn",
                "n": "b_knight", "N": "w_knight",
                "b": "b_bishop", "B": "w_bishop",
                "r": "b_rook", "R": "w_rook",
                "q": "b_queen", "Q": "w_queen",
                "k": "b_king", "K": "w_king"
                }
        for row_count, row in enumerate(board):
            for columnn_count, square in enumerate(row):
                if square != None:
                    self.__squares[row_count][columnn_count].config(
                        image=self.__piece_images[
                        f"{piece_dict[board[row_count][columnn_count]]}"],
                        width=75,
                        height = 75
                        )
                else:
                    self.__squares[row_count][columnn_count].config(
                        image=self.__empty_image,
                        width= 75,
                        height = 75
                        )
    

    def move_piece(self, row, column):
        """
        """
        if self.__game.get_board()[row][column] == None and self.__first_click:
            pass
        elif self.__first_click:
            self.__old_position = (row, column)
            self.__first_click = False
        elif not self.__first_click:
            self.__new_position = (row, column)
            self.__game.move_piece(self.__old_position, self.__new_position)
            self.load_position(self.__game.get_board())
            self.__first_click = True



    # def move_piece(self, old_pos, new_pos = (None,None)):
    #     """
    #     """
    #     if self.__first_click:
    #         self.__old_position = old_pos
    #         self.__first_click = False
        
    #     elif not self.__first_click:
    #         self.__game.move_piece(old_pos, new_pos)
    #         self.__first_click = True
            


    def mainloop(self):
        """Executes mainloop for <self.__mainwindow>.
        """
        self.__mainwindow.mainloop()

    
    def debug(self):
        """This method is used for debugging by executing 
        it from the main function.
        """
        
        # self.__game.move_piece((1,0), (2,0))
        # self.load_position(self.__game.get_board())
        # self.load_position(self.__game.get_board())
        # self.__game.print_board()
        # current_board = self.__game.get_board()
        # print(self.__game.list_to_fen())



def main():
    gui = Gui()
    gui.mainloop()
    

if __name__ == '__main__':
    main()