__author__ = 'Fitz'

import math

import mutants.Square
import mutants.Constants

class Board():
    """
    Represents the game board.
    >>> b = Board()
    >>> b.width = 10
    >>> b.fill()
    Must assign width and height before filling the board.
    False
    >>> b.height = 5
    >>> b.fill()
    True
    >>> sq = b.getSquare(3, 4)
    >>> print("Square's X = " + str(sq.getXpos()) + " and Y = " + str(sq.getYpos()))
    Square's X = 3 and Y = 4
    >>> sq = b.getSquare(9, 4)
    >>> print("Square's X = " + str(sq.getXpos()) + " and Y = " + str(sq.getYpos()))
    Square's X = 9 and Y = 4
    """

    def __init__(self):
        self.__squares = []
        self.__width = 0
        self.__height = 0
        self.__messages = []
        self.__maxmessages = 1

    @property
    def width(self):
        return(self.__width)

    @width.setter
    def width(self, width):
        self.__width = width

    @property
    def height(self):
        return (self.__height)

    @height.setter
    def height(self, height):
        self.__height = height

    # I think these need to be redefined as properties, but I'm not sure how yet.
    def addSquare(self, xpos, ypos):
        sq = mutants.Square.Square(self, xpos, ypos)
        self.__squares.append(sq)
        return (sq)

    def getSquareIndex(self, xpos, ypos):
        return(xpos + ypos * self.__width)

    def getSquare(self, xpos, ypos):
        assert((self.__height != 0) and (self.__width != 0))
        if ((xpos >= self.__width) or (ypos >= self.__height)):
            return None
        if ((xpos < 0) or (ypos < 0)):
            return None
        return(self.__squares[self.getSquareIndex(xpos, ypos)])

    def fill(self):
        if ((self.__width == 0) or (self.__height == 0)):
            print("Must assign width and height before filling the board.")
            return(False)

        for i in range(self.__height):
            for j in range(self.__width):
                self.addSquare(j, i)

        return(True)

    def emptyspace(self, inexterior="ExteriorSpace"):
        extsq = []
        for i in range(self.height):
            for j in range(self.width):
                sq = self.getSquare(j, i)
                if sq.getTerrain().name == inexterior and not sq.hasequipment():
                    extsq.append(sq)
        return(extsq)

    def residentmutants(self):
        muties = []
        for i in range(self.height):
            for j in range(self.width):
                sq = self.getSquare(j, i)
                if sq.isOccupied() and sq.piece.name == "Mutant":
                    muties.append(sq.piece)
        return(muties)

    def clearmutants(self):
        for i in range(self.height):
            for j in range(self.width):
                sq = self.getSquare(j, i)
                if sq.isOccupied() and sq.piece.name == "Mutant":
                    sq.removePiece()

    def distance(self, sq1, sq2, checkifblocked=False):
        """
        Return distance between two squares on the board.
        :param sq1: Square
        :param sq2: Square
        :param checkifblocked: Boolean
        :return: integer of distance; -1 if blocked & check is requested
        """
        xcurincr = 0.0
        ycurincr = 0.0
        xdif = sq2.getXpos() - sq1.getXpos()
        if xdif > 0:
            xdirct = mutants.Constants.Constants.RIGHT
        else:
            xdirct = mutants.Constants.Constants.LEFT
        ydif = sq2.getYpos() - sq1.getYpos()
        if ydif > 0:
            ydirct = mutants.Constants.Constants.DOWN
        else:
            ydirct = mutants.Constants.Constants.UP
        dist = abs(xdif) + abs(ydif)        # simple square-bound movement distance
        xincrdif = xdif / dist
        yincrdif = ydif / dist
        sqonpath = sq1
        if checkifblocked:
            #while sqonpath != sq2:
            while sqonpath != sq2 and (abs(xcurincr) < abs(xdif) or abs(ycurincr) < abs(ydif)):
                xcurincr += xincrdif
                if abs(xcurincr) >= 1:
                    sqonpath = sqonpath.getNeighbor(xdirct)
                    xcurincr -=  math.copysign(1, xdif)
                ycurincr += yincrdif
                if abs(ycurincr) >= 1:
                    sqonpath = sqonpath.getNeighbor(ydirct)
                    ycurincr -= math.copysign(1, ydif)
                if sqonpath != sq2 and sqonpath != sq1 and sqonpath.isblocking():
                    print("Can't get there from here")
                    dist = -1
                    break
            assert(dist == -1 or sqonpath == sq2)
        return (dist)

    def addmessage(self, msg):
        if len(self.__messages) > 1 and msg[0:8] == self.__messages[-1][0:8]:
            del self.__messages[-1]
        if len(self.__messages) >= self.__maxmessages:
            del self.__messages[0]
        self.__messages.append(msg)

    @property
    def messages(self):
        return(self.__messages)

    @property
    def maxmessages(self):
        return(self.__maxmessages)

    @maxmessages.setter
    def maxmessages(self, cnt):
        self.__maxmessages = cnt

if __name__ == "__main__":
    import doctest
    doctest.testmod()

