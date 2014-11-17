__author__ = 'Fitz'
import mutants.Piece
import mutants.Board
import mutants.Constants
import mutants.Terrain
import mutants.Space

class Square():
    """
    Represents a single square position on the board.
    Maybe contain a piece.
    >>> sq = Square(None)
    >>> p = mutants.Piece.Piece("Georgina", None)
    >>> if sq.addPiece(p): print("Piece " + p.name + " added successfully.")
    Piece Georgina added successfully.
    >>> if not sq.addPiece(p): print("Piece " + p.name + " refused to be added.")
    Piece Georgina refused to be added.
    """

    def __init__(self, board, xpos = 0, ypos = 0):
        self.__piece = None
        self.__board = board
        self.__xpos = xpos
        self.__ypos = ypos
        self.__terrain = mutants.Space.Space()

    def isOccupied(self):
        return (self.__piece != None)

    @property
    def piece(self):
        return (self.__piece)

    def addPiece(self, piece):
        """
        For the time being, we will allow only one piece per square.  That will change
         once pieces (like weapons) can be picked up.
        :param piece:
        :return: Boolean
        """
        if (not self.__terrain.movethru(piece)):
            print("Cannot move " + piece.getName() + " through " + self.__terrain.name)
            return (False)
        if (not self.isOccupied()):
            self.__piece = piece
            return(True)
        else:       # Can't move into an occupied square (for now)
            return(False)

    def removePiece(self):
        self.__piece = None

    def getTerrain(self):
        return(self.__terrain)

    def setTerrain(self, terrain):
        self.__terrain = terrain

    def getNeighbor(self, direction):
        neighX = self.__xpos + direction[0]
        neighY = self.__ypos + direction[1]
        neighbor = self.__board.getSquare(neighX, neighY)
        return(neighbor)

    def getXpos(self):
        return(self.__xpos)

    def getYpos(self):
        return(self.__ypos)

    def getPosStr(self):
        return("(" + str(self.__xpos) + ", " + str(self.__ypos) + ")")

if __name__ == "__main__":
    import doctest
    doctest.testmod()
