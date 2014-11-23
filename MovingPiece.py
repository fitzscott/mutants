__author__ = 'Fitz'

from mutants.Piece import Piece
import mutants.Constants

class MovingPiece(Piece):
    """
    Represents a piece that can move, either under the player's control or the computer's.
    >>> mp = MovingPiece("Ozzie", None)
    >>> mp.name
    'Ozzie'
    >>> mp.handtohand = 4
    >>> mp.handtohand
    4
    >>> if not mp.damage(1): print(mp.name + " is dead.  Aww....")
    Ozzie is dead.  Aww....
    """
    def __init__(self, name, image, movePts = 0, hitPts = 1):
        super().__init__(name, image)
        self.__movePts = movePts
        self.__moveRemaining = self.__movePts
        self.__hitPts = hitPts
        self.__handtohand = 0
        self.__ranged = 0
        self.__carried = None
        self.__lastsquare = None

    def resetMovement(self):
        self.__moveRemaining = self.__movePts

    def getRemainingMovement(self):
        return (self.__moveRemaining)

    def decrRemaining(self, howmany=1):
        self.__moveRemaining -= howmany

    def move(self, direction):
        #print("Moving " + self.name)
        if (self.__moveRemaining <= 0):
            print(self.name + " has no remaining movement points.")
            return (False)

        currsq = self.__lastsquare = self.getPosition()
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

    def damage(self, amount):
        self.__hitPts -= amount
        return(self.__hitPts > 0)

    def heal(self, amount):
        self.__hitPts += amount

    @property
    def handtohand(self):
        if (self.__carried != None):
            totalh2h = self.__handtohand + self.__carried.handtohandadd
        else:
            totalh2h = self.__handtohand
        return (totalh2h)

    @handtohand.setter
    def handtohand(self, h2h):
        self.__handtohand = h2h

    def pickup(self, tool):
        """
        move into a square and pick up what's there
        :type tool: mutants.Equipment.Equipment
        """
        if self.__carried != None:
            self.__lastsquare.addequipment(self.__carried)
        self.__carried = tool

if __name__ == "__main__":
    import doctest
    doctest.testmod()

