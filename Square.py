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
        self.__equipment = None

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
            print("Cannot move " + piece.name + " through " + self.__terrain.name)
            return (False)
        if (not self.isOccupied()):
            self.__piece = piece
            if self.hasequipment() and piece.wantpickup:
                piece.pickup(self.takeequipment())
            return(True)
        else:       # Can't move into an occupied square (for now)
            #print("Square at (" + str(self.getXpos()) + ", " + str(self.getYpos()) + ") is occupied." )
            return(False)

    def removePiece(self):
        if self.__piece != None:
            #if self.__piece.name != "Mutant":
            #    print("Removing " + self.__piece.name + " from (" + str(self.__xpos) + ", " + str(self.__ypos) + ")")
            self.__piece = None

    def getTerrain(self):
        return(self.__terrain)

    def setTerrain(self, terrain):
        self.__terrain = terrain

    def getNeighbor(self, direction, distance=1):
        #print("            Getting neighbor from square, distance " + str(distance))
        neighX = self.__xpos + direction[0] * distance
        neighY = self.__ypos + direction[1] * distance
        neighbor = self.__board.getSquare(neighX, neighY)
        return(neighbor)

    def getXpos(self):
        return(self.__xpos)

    def getYpos(self):
        return(self.__ypos)

    def getPosStr(self):
        return("(" + str(self.__xpos) + ", " + str(self.__ypos) + ")")

    def addequipment(self, tool):
        """
        We're just going to overwrite any equipment in the square.  Don't drop
        stuff into squares with stuff you still want.
        :param tool:
        :return:
        """
        self.__equipment = tool

    def getequipment(self):
        return (self.__equipment)

    def takeequipment(self):
        tool = self.__equipment
        self.__equipment = None
        return (tool)

    def hasequipment(self):
        return(self.__equipment != None)

    @property
    def showing(self):
        whatsShowing = None
        if self.isOccupied():
            whatsShowing = self.piece
        elif self.hasequipment():
            whatsShowing = self.__equipment
        else:
            whatsShowing = self.__terrain
        return (whatsShowing)

    def distanceto(self, sq, checkblocked=True, checkdoor=False):
        return (self.__board.distance(self, sq, checkblocked, checkdoor))

    def isblocking(self, checkdoors=False):
        #print("Checking whether we can attack through " + self.getTerrain().name)
        terr = self.getTerrain()
        ternm = terr.name
        if checkdoors:
            #print("    We should also check doors for " + self.getTerrain().name)
            return (self.isOccupied() or ternm == "Wall" or \
                    (ternm == "Door" and not terr.getmovethru()))
        else:
            return (self.isOccupied() or self.getTerrain().name == "Wall")

    def attackpiece(self, damage):
        if self.__piece != None:
            result = self.__piece.damage(damage)
            if result:     #  piece was killed
                equip = self.__piece.carried
                self.removePiece()
                if equip != None:
                    self.addequipment(equip)

    def sendmessage(self, msg):
        self.__board.addmessage(msg)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
