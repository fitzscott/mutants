__author__ = 'Fitz'

import random
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

    def movethru(self, piece=None):
        import mutants.Mutant

        if (self.__smashed):            # not really a door any more
            return (True)
        if (piece == None):
            return (False)
        if (isinstance(piece, mutants.Mutant.Mutant)):
            retval = self.smash()
            piece.decrRemaining(2)
            if retval:
                piece.message(piece.fullname + " smashes the door open")
            else:
                piece.message(piece.fullname + " fails to smash the door open")
            return (retval)
        elif (isinstance(piece, mutants.MovingPiece.MovingPiece)):
            piece.decrRemaining(1)
            return (True)
        else:
            return(False)

    def smash(self):
        """
        We'll have smashing to be a
        2 in 3 for mutants in the game.
        :return:
        """
        onedie = random.randint(1, 6)
        if (onedie >= 3):
            self.__smashed = True
            self.image = "SmashedDoor"
            return (True)
        else:
            return (False)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
