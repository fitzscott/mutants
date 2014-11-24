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
        self.__hasattacked = False

    def resetMovement(self):
        self.__moveRemaining = self.__movePts

    def getRemainingMovement(self):
        return (self.__moveRemaining)

    def canmove(self):
        #print("In canmove for " + self.fullname + " w/ move remaining: " + str(self.__moveRemaining))
        return (self.__moveRemaining > 0)

    def decrRemaining(self, howmany=1):
        self.__moveRemaining -= howmany

    def movetosquare(self, newsq, currsq=None):
        if currsq == None:
            currsq = self.__lastsquare = self.getPosition()
        if (newsq != None):
            dist = currsq.distanceto(newsq)
            if dist == -1:
                #print("Cannot move " + self.fullname + " through that.")
                return (False)
            if (dist <= self.getRemainingMovement()):
                if (self.setPosition(newsq)):
                    currsq.removePiece()
                    self.decrRemaining(dist)
                    return (True)
                else:
                    print("Piece " + self.name + " cannot move to that square.")
            else:
                print("Insufficient remaining movement for " + self.fullname)
        else:
            print("Piece " + self.name + " cannot move off the board.")
        return (False)

    def moveindirection(self, direction):
        #print("Moving " + self.name)
        if (self.__moveRemaining <= 0):
            print(self.name + " has no remaining movement points.")
            return (False)

        currsq = self.__lastsquare = self.getPosition()
        newsq = currsq.getNeighbor(direction)
        return (self.movetosquare(newsq, currsq))

    def damage(self, amount):
        self.__hitPts -= amount
        return(self.__hitPts <= 0)

    def alive(self):
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

    @property
    def ranged(self):
        if (self.__carried != None):
            totalranged = self.__ranged + self.__carried.rangedattack
        else:
            totalranged = 0    #  Cannot do a ranged attack w/o a ranged weapon
        return (totalranged)

    @ranged.setter
    def ranged(self, ranged):
        self.__ranged = ranged

    def pickup(self, tool):
        """
        move into a square and pick up what's there
        :type tool: mutants.Equipment.Equipment
        """
        if self.__carried != None and self.__lastsquare != None:
            self.__lastsquare.addequipment(self.__carried)
        self.__carried = tool

    @property
    def hasattacked(self):
        return(self.__hasattacked)

    @hasattacked.setter
    def hasattacked(self, att):
        print("In hasattacked(" + str(att) + ") setter for " + self.fullname)
        self.__hasattacked = att

    def hthattack(self, sq):
        sq.attackpiece(self.handtohand)
        return (True)

    def rngattack(self, sq, dist):
        print("In ranged attack for " + self.fullname)
        if self.ranged:
            # if ranged is positive, must have a ranged weapon
            if self.__carried.effectiverange >= dist:
                sq.attackpiece(self.ranged)
                ret = True
            else:
                print("That target is out of range.")
                ret = False
        else:
            print("Cannot do ranged attack.")
            ret = False
        return (ret)

    def attack(self, sq):
        result = False
        if self.hasattacked:
            return (False)
        dist = self.getPosition().distanceto(sq)
        if dist == -1:
            print("Cannot attack there")
        else:
            if dist == 1:
                self.hasattacked = self.hthattack(sq)
            else:
                self.hasattacked = self.rngattack(sq, dist)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

