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

    def healthyself(self):
        if self.carried != None and self.carried.name == "FirstAid":
            self.heal(self.carried.heals)
            self.carried = None
        else:
            self.message(self.fullname + " needs a first aid kit to heal.")
