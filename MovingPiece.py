mo__author__ = 'Fitz'

from mutants.Piece import Piece
import mutants.Constants

class MovingPiece(Piece):
    """
    Represents a piece that can move, either under the player's control or the computer's.
    >>> mp = MovingPiece("Ozzie", None)
    >>> mp.getName()
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

    def move(self, direction):
        currsq = self.getPosition()
        newsq = currsq.getNeighbor(direction)
        if (newsq != None):
            if (self.setPosition(newsq)):
                currsq.removePiece()
                self.__moveRemaining -= 1
            else:
                print("Piece " + self.getName() + " cannot move to that square.")
        else:
            print("Piece " + self.getName() + " cannot move off the board.")

if __name__ == "__main__":
    import doctest
    doctest.testmod()

