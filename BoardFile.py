__author__ = 'Fitz'

import os
import mutants.Board
import mutants.Constants
import mutants.FileChar
import mutants.Space
import mutants.Door
import mutants.Wall

class BoardFile():
    """
    Creates a board by reading in a file representation of the board
    >>> bf = BoardFile()
    >>> bf.basefilename = "testboard1"
    >>> print(bf.fullfilename)
    C:\\Users\\Fitz\\PycharmProjects\\Mutants\\mutants\\Resources\\Boards\\testboard1.txt
    >>> bf.readFromFile()
    """
    def __init__(self):
        self.__board = None
        self.__basefilename = None
        self.__fullfilename = None
        self.__file = None
        self.__columns = 0
        self.__lines = 0
        self.__boardlines = None

    @property
    def lines(self):
        return(self.__lines)

    @property
    def columns(self):
        return(self.__columns)

    @property
    def basefilename(self):
        return(self.__basefilename)

    @basefilename.setter
    def basefilename(self, bfnm):
        self.__basefilename = bfnm
        cwd = os.getcwd()
        self.__fullfilename = os.path.join(cwd, "Resources", "Boards", bfnm + ".txt")

    @property
    def fullfilename(self):
        return(self.__fullfilename)

    def readFromFile(self, filename=""):
        if (filename != ""):
            self.basefilename = filename
        self.__columns = 0
        self.__lines = 0
        self.__file = open(self.fullfilename, "r")
        self.__boardlines = self.__file.readlines()
        self.__columns = len(self.__boardlines[0]) - 1
        self.__lines = len(self.__boardlines)
        self.__file.close()

    def createBoard(self):
        fc = mutants.FileChar.FileChar()
        board = mutants.Board.Board()
        board.height = self.__lines
        board.width = self.__columns
        for linenum in range(len(self.__boardlines)):
            for colnum in range(len(self.__boardlines[linenum]) - 1):  #  skip CRLF
                sq = board.addSquare(colnum, linenum)
                equip = fc.getEquipment(self.__boardlines[linenum][colnum])
                piece = fc.getPiece(self.__boardlines[linenum][colnum])
                if (equip != None):
                    # equipment can only reside in clear terrain
                    terr = fc.getTerrain(" ")
                    sq.addequipment(equip)
                elif (piece != None):
                    # Mutant can only reside in clear terrain (for these purposes, at least).
                    # Computer is largely the same.
                    terr = fc.getTerrain(" ")
                    if piece.name == "Computer":
                        sq.board.placerobot(piece, sq)      # treat the computer like a non-moving robot.
                    else:
                        sq.board.placemutant(piece, sq)
                else:
                    terr = fc.getTerrain(self.__boardlines[linenum][colnum])
                sq.setTerrain(terr)
        return(board)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

