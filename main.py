"""
COMP.CS.100
Author: Oskari Heinonen

Chess game with a gui.

Features:
    - Can only make legal moves
    - Basic AI to play against
    - Customizable board
    - 2 player mode

Limitations:
    - Can only play as white against AI
    - AI is stupid
    - No castling, en passant, or promotions
    - Doesn't recognize checkmates except usually for black when
      using defensive AI
    - Doesn't recognize stalemates
"""

from gui import *
from game import *

def main():
    game = Game()
    gui = Gui(game)
    gui.start()

if __name__ == "__main__":
    main()
