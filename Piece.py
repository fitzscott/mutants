__author__ = 'Fitz'
import mutants.Square

class Piece:
    """
    Represents a piece / counter / chit on the board.
    >>> p = Piece("Bob", None)
    >>> print(p.getName())
    Bob
    >>> sq = mutants.Square.Square(None)
    >>> p.setPosition(sq)
    """

    def __init__(self, name, image):
        self.__name = name
        self.__image = image
        self.__square = None

    def getName(self):
        return(self.__name)

    def setPosition(self, square):
        """
        :type square: Square
        Can't seem to import it, though - will it still work?
        """
        if (square.addPiece(self)):
            self.__square = square

    def getPosition(self):
        return(self.__square)

if __name__ == "__main__":
    import doctest
    doctest.testmod()


