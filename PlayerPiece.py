__author__ = 'Fitz'

import mutants.MovingPiece
import mutants.Constants

class PlayerPiece(mutants.MovingPiece.MovingPiece):
    """
    Represents humans and robots (or robotos, if we're playing in Styx Japan)
    >>> molly = PlayerPiece("Molly")
    >>> print(molly.fullname)
    Molly
    """

    def __init__(self, name):
        # first, get attributes for this piece from constants
        if name in mutants.Constants.Constants.playerpieceattributes:
            attr = mutants.Constants.Constants.playerpieceattributes[name]
            mov = attr[0]
            hp = attr[1]
            h2h = attr[2]
            rng = attr[3]
            super().__init__(name, name, mov, hp)
            self.handtohand = h2h
            self.ranged = rng
        else:
            print("No attributes for player piece " + name)

