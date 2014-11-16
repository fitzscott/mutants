__author__ = 'Fitz'

import mutants.Square

class Board():
    """
    Represents the game board.
    >>> b = Board()
    >>> b.setWidth(10)
    >>> b.fill()
    Must assign width and height before filling the board.
    False
    >>> b.setHeight(5)
    >>> b.fill()
    True
    >>> sq = b.getSquare(3, 4)
    >>> print("Square's X = " + str(sq.getXpos()) + " and Y = " + str(sq.getYpos()))
    Square's X = 3 and Y = 4
    """

    def __init__(self):
        self.__squares = []
        self.__width = 0
        self.__height = 0

    def setWidth(self, width):
        self.__width = width

    def setHeight(self, height):
        self.__height = height

    def addSquare(self, xpos, ypos):
        self.__squares.append(mutants.Square.Square(self, xpos, ypos))

    def getSquare(self, xpos, ypos):
        assert((self.__height != 0) and (self.__width != 0))
        return(self.__squares[xpos + ypos * self.__width])

    def fill(self):
        if ((self.__width == 0) or (self.__height == 0)):
            print("Must assign width and height before filling the board.")
            return(False)

        for i in range(self.__height):
            for j in range(self.__width):
                self.addSquare(j, i)

        return(True)

if __name__ == "__main__":
    import doctest
    doctest.testmod()



