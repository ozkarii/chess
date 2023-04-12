"""
COMP.CS.100
Author: Oskari Heinonen

Chess game
"""

from gui import *
from game import *

def main():
    game = Game()
    gui = Gui(game)
    gui.start()


if __name__ == "__main__":
    main()