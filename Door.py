__author__ = 'Fitz'

import mutants.Terrain
import mutants.MovingPiece

class Door(mutants.Terrain.Terrain):
    """
    Represents a door.
    There will be some interesting interaction checking required for the
    move through check:  Humans and robots should be able to move through
    doors smoothly (maybe requiring one extra movement point),
    but mutants will need to smash doors to get through (because they're
    mutants, after all).
    >>> d = Door()
    >>> if (not d.movethru(None)): print("You can't move through a door, apparently.")
    You can't move through a door, apparently.
    """

    def __init__(self):
        super().__init__("Door", "Door")
        self.__smashed = False

    def movethru(self, piece):
        if (self.__smashed):
            return (True)
        if (isinstance(piece, mutants.MovingPiece.MovingPiece)):
            piece.decrRemaining(1)
            return (True)
        else:
            return(False)

    def smash(self):
        """
        For now, we'll have smashing be automatic.  I think we'll only want it to be a
        2 in 3 for mutants in the game, though.
        :return:
        """
        self.__smashed = True

if __name__ == "__main__":
    import doctest
    doctest.testmod()
