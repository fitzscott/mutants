__author__ = 'Fitz'

import random

import mutants.Board
import mutants.BoardFile
import mutants.Human
import mutants.Display
import mutants.Constants
import mutants.Mutant

class Game():
    """
    Represents the game as a whole.
    Contains the display, the board (though the display creates it), the player's pieces,
    the mutant's pieces.
    >>> g = Game()
    >>> g.board.getmutants(1)
    >>> g.board.placemutants()
    """

    def __init__(self, boardname=mutants.Constants.Constants.GAMEBOARD):
        self.__wave = 1
        self.__display = mutants.Display.Display(self)
        self.__display.loadResources(boardname)
        self.__board = self.__display.board
        self.__mutantturn = False

    def play(self, maxloops=10000000):
        self.__display.runLoop(maxloops)

    @property
    def board(self):
        return(self.__board)

    @property
    def mutantturn(self):
        return(self.__mutantturn)

    @mutantturn.setter
    def mutantturn(self, onoff):
        """

        :type onoff: Boolean
        """
        self.__mutantturn = onoff

    # lots of delegating going on here.
    def clearfoci(self):
        self.board.clearfoci()

    def piecewithfocus(self):
        return (self.board.piecewithfocus())

    def movepiecewithfocus(self, sq, dirct=None):
        """
        Only interested in moving player pieces this way.  Mutants move on their own.
        :param sq: Square
        :return: boolean
        """
        ret = False
        piece = self.piecewithfocus()
        if piece != None:
            if dirct == None:
                ret = piece.movetosquare(sq)
            else:
                ret = piece.moveindirection(dirct)
        return(ret)

    def wavecomplete(self):
        return(self.board.playerpiececount() == 0 or self.board.mutantpiececount() == 0)
        #return(len(self.__mutants) == 0)

    def nextwave(self):
        if self.__wave == len(mutants.Constants.Constants.MUTANTSPERWAVE):
            #self.__board.addmessage("")
            if self.board.playerpiececount() == 0:
                self.__board.addmessage("Game over!  The evil mutants have triumphed!")
            else:
                humansleft = self.board.humanpiececount()
                if humansleft > 3:
                    self.__board.addmessage("Game over!  Decisive human victory over the mutants!")
                elif humansleft > 1:
                    self.__board.addmessage("Game over!  Marginal human victory over the mutants!")
                elif humansleft == 1:
                    self.__board.addmessage("Game over!  It's a draw!")
                else:
                    self.__board.addmessage("Game over!  Marginal victory for the mutants!")
            #self.__board.addmessage("")
            return(False)
        self.__wave += 1
        self.__board.addmessage("")
        self.__board.addmessage("        Wave " + str(self.__wave) + "!")
        self.__board.clearmutants()
        self.__mutants = []
        self.board.getmutants(self.__wave)
        self.board.placemutants()
        return (True)

    def clearoutdead(self):
        self.board.clearoutdead()

    def nextturn(self):
        self.board.resetpieces()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
