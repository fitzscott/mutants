__author__ = 'Fitz'

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
                if sq.getTerrain().name == inexterior:
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
        xdif = sq1.getXpos() - sq2.getXpos()
        ydif = sq1.getYpos() - sq2.getYpos()
        dist = abs(xdif) + abs(ydif)
        sqonpath = sq1
        if checkifblocked:
            # This is a kludge.  Need to re-work it later.
            while abs(xdif) + abs(ydif) > 0:
                if abs(xdif) >= abs(ydif):
                    # go left or right
                    if xdif < 0:
                        dirct = mutants.Constants.Constants.RIGHT
                        xdif += 1
                    else:
                        dirct = mutants.Constants.Constants.LEFT
                        xdif -= 1
                else:
                    # go up or down
                    if ydif < 0:
                        dirct = mutants.Constants.Constants.DOWN
                        ydif += 1
                    else:
                        dirct = mutants.Constants.Constants.UP
                        ydif -= 1
                sqonpath = sqonpath.getNeighbor(dirct)
                if sqonpath != sq2 and sqonpath.isblocking():
                    dist = -1
                    break
        return (dist)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

