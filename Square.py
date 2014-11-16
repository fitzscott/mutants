__author__ = 'Fitz'
import mutants.Piece
import mutants.Board

class Square():
    """
    Represents a single square position on the board.
    Maybe contain a piece.
    >>> sq = Square(None)
    >>> p = mutants.Piece.Piece("Georgina", None)
    >>> if (sq.addPiece(p)): print("Piece " + p.getName() + " added successfully.")
    Piece Georgina added successfully.
    >>> if (not sq.addPiece(p)): print("Piece " + p.getName() + " refused to be added.")
    Piece Georgina refused to be added.
    """

    def __init__(self, board, xpos = 0, ypos = 0):
        self.__piece = None
        self.__board = board
        self.__xpos = xpos
        self.__ypos = ypos

    def addPiece(self, piece):
        """
        For the time being, we will allow only one piece per square.  That will change
         once pieces (like weapons) can be picked up.
        :param piece:
        :return: Boolean
        """
        if (self.__piece == None):
            self.__piece = piece
            return(True)
        else:       # Can't move into an occupied square (for now)
            return(False)

    def getXpos(self):
        return(self.__xpos)

    def getYpos(self):
        return(self.__ypos)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
