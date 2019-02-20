__author__ = 'Fitz'

import PlayerPiece as pp

class Human(pp.PlayerPiece):
    """
    The human pieces on the board are the basis of the victory conditions.
    >>> bart = Human("Buck")
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
            self.message(self.fullname + " uses the first aid kit to heal.")
            self.carried = None
        else:
            self.message(self.fullname + " needs a first aid kit to heal.")

    @property
    def indicatorstring(self):
        return "Tombstone"

