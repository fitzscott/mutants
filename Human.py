__author__ = 'Fitz'

import mutants.PlayerPiece

class Human(mutants.PlayerPiece.PlayerPiece):
    """
    The human pieces on the board are the basis of the victory conditions.
    >>> bart = Human("Bart")
    >>> molly = Human("Molly")
    >>> charlie = Human("Charlie")
    >>> if charlie.canmove(): print("Charlie can move.")
    Charlie can move.
    """
    def __init__(self, name):
        super().__init__(name)
        self.__focus = False

    @property
    def focus(self):
        return (self.__focus)

    @focus.setter
    def focus(self, onoff):
        if onoff:
            print("Human " + self.name + " has focus.")
        self.__focus = onoff



