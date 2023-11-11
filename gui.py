"""
COMP.CS.100 
Tekijä: Oskari Heinonen

Gui for chess
"""

import tkinter as tk
from tkinter import ttk, colorchooser
import os
import winsound
import ai
import game
from server import *
from async_tkinter_loop import async_mainloop, async_handler


class Gui:
    """This class handles the gui for the chess game.
    """

    def __init__(self, game: game.Game):
        
        """Initializes the gui-object with an empty chessboard
        and a menu.

        :param game: game-object used in the game instance
        """
        
        self.__mainwindow = tk.Tk()
        self.__mainwindow.geometry("+600+100")
        self.__mainwindow.resizable(False, False)
        self.__mainwindow.title("Chess")
        logo = tk.PhotoImage(file="pictures/logo.png")
        self.__mainwindow.iconphoto(True, logo)

        # Dict for mapping piece names to corresponding PhotoImage-objects
        self.__piece_images = {}
        
        # Define image-object for empty square
        self.__empty_image = tk.PhotoImage("pieces/empty.png")
        
        # load style attributes from file
        self.style_from_file("config/style.txt")

        # Load game config attributes from file
        self.game_config_from_file("config/game.txt")
        
        # Pass the game object to an attribute
        self.__game = game

        # Init attribute which tells which pieces are played by the player
        self.__play_as_white = True

        # Indicates wether or not online mode is enabled
        self.__playing_online = False

        self.__server = None

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
        for i in os.listdir("pictures/pieces/Cburnett"):
            self.__piece_images[i.replace(".png","")] = \
            tk.PhotoImage(file=f"pictures/pieces/Cburnett/{i}")
        
        
        # Squares
        self.__squares = []
        for x in range(1,9):
            self.__row = []
            for y in range(1,9):
                self.__square = tk.Button(
                    self.__mainwindow, width=10, height=5, 
                    borderwidth=0, bg=self.__light_square_color)
                self.__square.grid(row=x, column=y)
                if self.__game.square_is_dark(x, y):
                    self.__square.config(bg=self.__dark_square_color)
                self.__row.append(self.__square)
            self.__squares.append(self.__row)

        # Adds commands to all buttons
        for row_count, row in enumerate(self.__squares):
            for column_count, square in enumerate(row):
                # square.config(command=async_handler(lambda row=row_count,
                #               column=column_count: self.move_piece(row, column)))
                square.config(command=lambda row=row_count,
                              column=column_count: 
                              [self.move_piece(row, column),
                               self.change_square_color(row, column)])

        # Menubar
        self.__menubar = tk.Menu(self.__mainwindow, tearoff=0)

        # Game menu
        self.__game_menu = tk.Menu(self.__menubar, tearoff=0)
        self.__game_menu.add_command(label="Load position", 
                                command=self.load_position_popup)
        self.__game_menu.add_command(label="Reset position",
                                command=self.set_start_config)
        self.__menubar.add_cascade(menu=self.__game_menu, label="Game")
        
        # Settings menu
        self.__settings_menu = tk.Menu(self.__menubar, tearoff=0)
        self.__settings_menu.add_command(label="Game", command=self.game_popup)
        self.__settings_menu.add_command(label="Style",
                                         command=self.style_popup)
        self.__menubar.add_cascade(menu=self.__settings_menu, label="Settings")

        # Online menu
        self.__online_menu = tk.Menu(self.__menubar, tearoff=0)
        self.__online_menu.add_command(label="Host game", 
                                       command=self.host_game_popup)
        self.__online_menu.add_command(label="Join game",
                                       command=self.join_game_popup)
        self.__menubar.add_cascade(menu=self.__online_menu, label="Online")

        self.__mainwindow.config(menu=self.__menubar)
        
        # Labels TODO fix order
        for y in range(1,9):
            y_label = tk.Label(self.__mainwindow, 
                               text=str(y), font=("Arial", 13)
                               )
            y_label.grid(column=0, row=y)
        letters = ["A","B","C","D","E","F","G","H"]
        for x in range(1,9):
            x_label = tk.Label(self.__mainwindow, 
                               text=letters[x - 1], font=("Arial", 13)
                               )
            x_label.grid(column=x, row=9)
        
        tk.Label(self.__mainwindow, text="   ").grid(row=2, column=9)

        # Checkmate label
        self.__checkmate_label = tk.Label(self.__mainwindow, text="Checkmate!",
                                          fg="red", font=("Arial", 10))
        
        self.set_start_config()


    def set_start_config(self):
        """Asks the player which pieces they want to play and then loads
        the game's starting configuration accordingly
        """

        # TODO: fix popup not being on top
        popup = tk.Toplevel(self.__mainwindow)
        popup.grab_set()
        popup.title("Play as?")
        popup.geometry("250x100+800+300")
        popup.resizable(False, False)

        def set_play_as_white(value):
            self.__play_as_white = value
            popup.destroy()

        white = tk.Button(popup, text="White", command=lambda: set_play_as_white(True), width=10, height=2)
        black = tk.Button(popup, text="Black", command=lambda: set_play_as_white(False), width=10, height=2)
        
        white.grid(row=0, column=0, padx=10, pady=10)
        black.grid(row=0, column=1, padx=10, pady=10)

        popup.wait_window()  # Wait for the popup window to be closed

        # Set starting position in the game object
        self.__game.set_start_position(self.__play_as_white)
        self.load_position(self.__game.get_board())


    def ai_move(self):
        """Executes ai move
        """

        if self.__ai_playstyle == "None":
            pass

        elif self.__ai_playstyle == "Defensive":
                old, new = ai.calculated_move(self.__game, 
                                              self.__game.get_board(), "black")
                if new is None:
                    self.__checkmate_label.grid(row=10, column=1)
                else:
                    self.__game.move_piece(old, new)
                    self.load_position(self.__game.get_board())

        elif self.__ai_playstyle == "Random":
            ai.random_move(self.__game, self.__game.get_board(), "black")
            self.load_position(self.__game.get_board())
        
        elif self.__ai_playstyle == "Mixed":
            pass


    def host_game_popup(self):
        """
        """

        popup = tk.Toplevel(self.__mainwindow)
        popup.grab_set()
        popup.title("Host game")
        main_x = self.__mainwindow.winfo_rootx()
        main_y = self.__mainwindow.winfo_rooty()
        popup.geometry(f"350x200+{main_x + 125}+{main_y + 200}")
        popup.resizable(False, False)
        
        async def start_server():
            self.__game.enable_online_mode()
            self.__playing_online = True
            self.__server = Server('localhost', 5000, self)
            await self.__server.start_server()
    

        start = tk.Button(popup, text="Start", command=async_handler(start_server))
        start.grid()


    def join_game_popup(self):
        """
        """

        popup = tk.Toplevel(self.__mainwindow)
        popup.grab_set()
        popup.title("Join game")
        main_x = self.__mainwindow.winfo_rootx()
        main_y = self.__mainwindow.winfo_rooty()
        popup.geometry(f"350x200+{main_x + 125}+{main_y + 200}")
        popup.resizable(False, False)


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
                    if self.__game.square_is_dark(x_count, y_count):
                        y.config(bg=self.__dark_square_color)
                    else:
                        y.config(bg=self.__light_square_color)
        else:
            current_color = self.__squares[row][column].cget("bg")
            if current_color == self.__light_square_color or \
               current_color == self.__dark_square_color:
                # Find the current new_color square, if any
                new_color_square = None
                for i in range(0,8):
                    for j in range(0,8):
                        if self.__squares[i][j].cget("bg") == \
                            self.__highlight_color:
                            new_color_square = (i, j)
                            break
                    if new_color_square:
                        break

                # If there's already a new_color square, 
                # change it to the original color
                if new_color_square:
                    previous_row = new_color_square[0]
                    previous_column = new_color_square[1]
                    if self.__game.square_is_dark(previous_row,
                                                  previous_column):
                        self.__squares[previous_row][previous_column].config(
                            bg=self.__dark_square_color)
                    else:
                        self.__squares[previous_row][previous_column].config(
                            bg=self.__light_square_color)

                # Set the clicked square to highlight color
                self.__squares[row][column].config(bg=self.__highlight_color)

            # If the clicked square is in highlight color, 
            # set it to the original color
            else:
                if self.__game.square_is_dark(row, column):
                    self.__squares[row][column].config(
                        bg=self.__dark_square_color)
                else:
                    self.__squares[row][column].config(
                        bg=self.__light_square_color)


    def style_from_file(self, path):
        """Assigns style settings to the attributes from a file.

        :param path: str, path to style file
        """

        with open(path, "r") as style_file:
            lines = style_file.readlines()
            style_dict = {}
            for line in lines:
                line = line.strip()
                style_dict[line.split(";")[0]] = \
                line.split(";")[1].replace("\n","")

        try:
            self.__light_square_color = style_dict["lightsquare"]
            self.__dark_square_color = style_dict["darksquare"]
            self.__highlight_color = style_dict["highlight"]
            self.__piece_style = style_dict["pieces"]

        except KeyError:
            self.__light_square_color = "#f0e1c7"
            self.__dark_square_color = "#a1784f"
            self.__highlight_color = "red"
            self.__piece_style = "Cburnett"


    def style_to_file(self, path):
        """Writes the current style attributes to the style file.

        :param path: str, relative path to style file
        """

        with open(path, "r") as style_file:
            lines = style_file.readlines()
            for line in lines:
                line = line.strip()

        lines[0] = f"lightsquare;{self.__light_square_color}\n"
        lines[1] = f"darksquare;{self.__dark_square_color}\n"
        lines[2] = f"highlight;{self.__highlight_color}\n"
        lines[3] = f"pieces;{self.__piece_style}\n"

        with open(path, "w") as style_file:
            for line in lines:
                style_file.write(f"{line.strip()}\n")


    def game_config_from_file(self, path):
        """Assigns game settings to the attributes from a file.

        :param path: str, path to game config file
        """

        with open(path, "r") as game_config_file:
            lines = game_config_file.readlines()
            game_config_dict = {}
            for line in lines:
                line = line.strip()
                game_config_dict[line.split(";")[0]] = \
                line.split(";")[1].replace("\n","")

        try:
            self.__ai_playstyle = game_config_dict["ai_playstyle"]
            self.__ai_playstyle_var = tk.StringVar(
                self.__mainwindow, game_config_dict["ai_playstyle"])

        except KeyError:
            self.__ai_playstyle = "Defensive"
            self.__ai_playstyle_var = tk.StringVar(self.__mainwindow,
                                                   "Defensive")


    def game_config_to_file(self, path):
        """Writes the current game config attributes to the style file.

        :param path: str, relative path to game config file
        """

        with open(path, "r") as game_config_file:
            lines = game_config_file.readlines()
            for line in lines:
                line = line.strip()

        lines[0] = f"ai_playstyle;{self.__ai_playstyle_var.get()}\n"

        with open(path, "w") as game_config_file:
            for line in lines:
                game_config_file.write(f"{line.strip()}\n")


    def load_position_popup(self):
        """Opens a popup window for loading a position.
        """

        popup = tk.Toplevel(self.__mainwindow)
        popup.grab_set()
        popup.title("Load position")
        main_x = self.__mainwindow.winfo_rootx()
        main_y = self.__mainwindow.winfo_rooty()
        popup.geometry(f"500x150+{main_x + 20}+{main_y + 20}")
        popup.resizable(False, False)

        usr_input = tk.StringVar(popup)
        entry = tk.Entry(popup,textvariable=usr_input, width=65)
        entry.grid(padx=50, pady=25, row=0, column=0)
        
        def set_pos():
            if self.__game.set_position(entry.get()):
                self.load_position(self.__game.get_board())
                error_label = tk.Label(popup, text=" Valid FEN-string ",
                                       fg="green")
                error_label.grid(row=2, pady=10)
            else:
                error_label = tk.Label(popup, text="Invalid FEN-string",
                                       fg="red")
                error_label.grid(row=2, pady=10)
        
        load_button = tk.Button(popup, text="Load", command=set_pos)
        load_button.grid(row=1, column=0)


    def style_popup(self):
        """Opens a popup window for the style settings.
        """

        def set_color(target):
            """Sets the square colors based on current square_color attributes

            :param target: str, specifies which style element is edited
            """

            if target == "highlight":
                self.__highlight_color = colorchooser.askcolor()[1]

            elif target == "lightsquare":
                self.__light_square_color = colorchooser.askcolor()[1]    
                for x in range(0,8):
                    for y in range(0,8):
                        if self.__game.square_is_dark(x, y):
                            self.__squares[x][y].config(
                                bg=self.__dark_square_color)
                        else:
                            self.__squares[x][y].config(
                                bg=self.__light_square_color)
            
            elif target == "darksquare":
                self.__dark_square_color = colorchooser.askcolor()[1]
                for x in range(0,8):
                    for y in range(0,8):
                        if self.__game.square_is_dark(x, y):
                            self.__squares[x][y].config(
                                bg=self.__dark_square_color)
            
            elif target == "reset":
                self.__light_square_color = "#f0e1c7"
                self.__dark_square_color = "#a1784f"
                self.__highlight_color = "red"
                for x in range(0,8):
                    for y in range(0,8):
                        if self.__game.square_is_dark(x, y):
                            self.__squares[x][y].config(
                                bg=self.__dark_square_color)
                        else:
                            self.__squares[x][y].config(
                                bg=self.__light_square_color)


        popup = tk.Toplevel(self.__mainwindow)
        popup.grab_set()
        popup.title("Style settings")
        main_x = self.__mainwindow.winfo_rootx()
        main_y = self.__mainwindow.winfo_rooty()
        popup.geometry(f"300x150+{main_x + 20}+{main_y + 20}")
        popup.resizable(False, False)

        pick_highlight_color = tk.Button(popup, text="Highlight color...")
        pick_highlight_color.config(command= lambda: set_color("highlight"))
        pick_highlight_color.grid(row=0, column=1, padx=10, pady=5)

        pick_light_sqr_color = tk.Button(popup, text="Light square color...")
        pick_light_sqr_color.config(command= lambda: set_color("lightsquare"))
        pick_light_sqr_color.grid(row=1, column=1, padx=10, pady=5)

        pick_dark_sqr_color = tk.Button(popup, text="Dark square color...")
        pick_dark_sqr_color.config(command= lambda: set_color("darksquare"))
        pick_dark_sqr_color.grid(row=2, column=1, padx=10, pady=5)

        reset_colors = tk.Button(popup, text="Reset colors")
        reset_colors.config(command= lambda: set_color("reset"))
        reset_colors.grid(row=3, column=1, padx=10, pady=5)

        piece_style_menu = ttk.Combobox(popup, state="readonly")
        piece_style_menu["values"] = ("Cburnett")
        piece_style_menu["state"] = 'readonly'
        piece_style_menu.current(0)
        piece_style_menu.grid(row=1, column=0, padx=10)

        piece_style_label = tk.Label(popup, text="Piece style", 
                                     font=("Arial", 10))
        piece_style_label.grid(row=0, column=0)

        save_changes = tk.Button(popup, text="Save changes", height=1,
                                 command= lambda: 
                                 self.style_to_file("config/style.txt"))
        save_changes.grid(row=3, column=0)


    def game_popup(self):
        """Loads a popup window for game settings.
        """
        
        popup = tk.Toplevel(self.__mainwindow)
        popup.grab_set()
        popup.title("Game settings")
        main_x = self.__mainwindow.winfo_rootx()
        main_y = self.__mainwindow.winfo_rooty()
        popup.geometry(f"275x175+{main_x + 20}+{main_y + 20}")
        popup.resizable(False, False)

        ai_playstyle_1 = tk.Radiobutton(popup, text="Defensive", 
                                        variable=self.__ai_playstyle_var,
                                        value="Defensive")
        ai_playstyle_2 = tk.Radiobutton(popup, text="Random", 
                                        variable=self.__ai_playstyle_var,
                                        value="Random")
        # ai_playstyle_3 = tk.Radiobutton(popup, text="Mixed", 
        #                                 variable=self.__ai_playstyle_var,
        #                                 value="Mixed")
        ai_playstyle_4 = tk.Radiobutton(popup, text="No AI (2-player mode)",
                                        variable=self.__ai_playstyle_var,
                                        value="None")

        ai_playstyle_1.grid(row=1, padx=100)
        ai_playstyle_2.grid(row=2, padx=100)
        # ai_playstyle_3.grid(row=3, padx=60)
        ai_playstyle_4.grid(row=4, padx=60)

        save_button = tk.Button(popup, text="Save", command=lambda: [
                                self.game_config_to_file("config/game.txt"),
                                self.game_config_from_file("config/game.txt")],
                                width=10)
        
        save_button.grid(row=5, padx=60, pady=30)

        ai_label = tk.Label(popup, text="AI playstyle", font=("Helvetica", 11))
        ai_label.grid(row=0, padx=60, pady=2)


    def play_as_popup(self):
        popup = tk.Toplevel(self.__mainwindow)
        popup.grab_set()
        popup.title("Play as?")
        popup.geometry(f"220x100+{500}+{500}")
        popup.resizable(False, False)

        def set_play_as_white(value):
            setattr(self, '__play_as_white', value)
            popup.destroy()
            return value

        white = tk.Button(popup, text="White", command=lambda: set_play_as_white(True), width=10, height=2)
        black = tk.Button(popup, text="Black", command=lambda: set_play_as_white(False), width=10, height=2)
        
        white.grid(row=0, column=0, padx=10, pady=10)
        black.grid(row=0, column=1, padx=10, pady=10)


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
        """Moves the previously clicked piece to the now clicked square

        :param row: int, row of the currently clicked square
        :param column: int, column of the currently clicked square
        """

        if self.__game.get_board()[row][column] is None and self.__first_click:
            pass
        elif self.__first_click:
            self.__old_position = (row, column)
            self.__first_click = False
        else:
            self.__new_position = (row, column)
            # If game.move_piece-function returns True i.e. the move is legal,
            # move the pieces
            if self.__game.move_piece(self.__old_position, self.__new_position):
                self.load_position(self.__game.get_board())
                if self.__old_position != self.__new_position:
                    winsound.Beep(587, 100)
                    self.ai_move()
                    # if self.__playing_online:
                    #     await self.online_move()
                self.__first_click = True
            else:
                self.__first_click = True

    def online_move_piece(self, old_pos, new_pos):
        """This function gets (currently) only called by the server
        when it receives a move from the client.
        """

        if self.__game.move_piece(old_pos, new_pos, True):
            self.load_position(self.__game.get_board())
            self.__game.chance_turn()


    def start(self):
        """Executes mainloop for <self.__mainwindow> ie. starts the gui.
        """
        async_mainloop(self.__mainwindow)
        # self.__mainwindow.mainloop()
