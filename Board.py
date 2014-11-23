__author__ = 'Fitz'

import mutants.Square

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

    def emptyexterior(self):
        extsq = []
        for i in range(self.height):
            for j in range(self.width):
                sq = self.getSquare(j, i)
                if sq.getTerrain().name == "ExteriorSpace":
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()

