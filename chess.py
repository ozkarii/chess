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
        pass
        


class Piece:
    """
    """
    def __init__(self, category, color, position):
        self.__category = category
        self.__color = color
        self.__position = position
        self.__alive = True

    def move(self, target):
        """
        """

    def die(self):
        """
        """
        self.__alive = False

    def get_position(self):
        """
        maybe tuple
        """
        return self.__position

    def get_category(self):
        """
        """
        return self.__category
    
    def get_color(self):
        """
        """
        return self.__color

    def attacked_squares(self):
        """
        """
        if self.__category == "pawn":
            pass

        elif self.__category == "knight":
            pass

        elif self.__category == "bishop":
            pass

        elif self.__category == "rook":
            pass

        elif self.__category == "queen":
            pass

        elif self.__category == "king":
            pass




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

def threatened_pieces(piece):
    """Returns a list of pieces which are threathened by the parameter piece.
    """
    

def in_check(piece):
    """
    """
    if piece.get_category() == "king":
        return False

    else:
        return None


def initialze_game(board):
    """Puts all the pieces into their starting positions.
    """
    for square in board[1]:
        square = Piece("pawn")

def main():
   
    return

if __name__ == '__main__':
    main()