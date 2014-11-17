mo__author__ = 'Fitz'

from mutants.Piece import Piece
import mutants.Constants

class MovingPiece(Piece):
    """
    Represents a piece that can move, either under the player's control or the computer's.
    >>> mp = MovingPiece("Ozzie", None)
    >>> mp.name
    'Ozzie'
    """
    def __init__(self, name, image, movePts = 0):
        super().__init__(name, image)
        self.__movePts = movePts
        self.__moveRemaining = self.__movePts

    def resetMovement(self):
        self.__moveRemaining = self.__movePts

    def getRemainingMovement(self):
        return (self.__moveRemaining)

    def decrRemaining(self, howmany=1):
        self.__moveRemaining -= howmany

    def move(self, direction):
        if (not self.__moveRemaining):
            print(self.name + " has no remaining movement points.")
            return (False)

        currsq = self.getPosition()
        newsq = currsq.getNeighbor(direction)
        if (newsq != None):
            if (self.setPosition(newsq)):
                currsq.removePiece()
                self.decrRemaining()
                return (True)
            else:
                print("Piece " + self.name + " cannot move to that square.")
        else:
            print("Piece " + self.name + " cannot move off the board.")

        return (False)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

