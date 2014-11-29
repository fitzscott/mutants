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
    >>> g.getmutants()
    >>> g.placemutants()
    """

    def __init__(self, boardname=mutants.Constants.Constants.GAMEBOARD):
        self.__wave = 1
        self.__mutants = []
        self.__playerpieces = []
        #self.__humans = []
        #self.__robots = []
        self.__display = mutants.Display.Display(self)
        self.__display.loadResources(boardname)
        self.__board = self.__display.board
        self.__mutantturn = True

    def getmutants(self, overridenum=0):
        # If the board comes pre-defined with mutants, don't add new ones.
        resmuties = self.__board.residentmutants()
        if len(resmuties) > 0:
            self.__mutants = resmuties
            return
        if overridenum:
            nummutants = overridenum
        else:
            nummutants = mutants.Constants.Constants.MUTANTSPERWAVE[self.__wave - 1]
        self.__mutants = []
        for i in range(nummutants):
            self.__mutants.append(mutants.Mutant.Mutant())
            self.__mutants[i].number = i

    def placemutants(self):
        stagingarea = self.__board.emptyspace()
        numempties = len(stagingarea) - len(self.__mutants)
        for i in range(numempties):
            stgsiz = len(stagingarea)
            idx = random.randint(0, stgsiz-1)
            del stagingarea[idx]
        for i in range(len(self.__mutants)):
            self.placemutant(self.__mutants[i], stagingarea[i])

    def placemutant(self, mutie, sq):
        if mutie not in self.__mutants:
            print("Appending fixed-position mutant")
            self.__mutants.append(mutie)
        mutie.setPosition(sq)

    def placeplayerpiece(self, piece, pcgrp, sq=None):
        if piece not in pcgrp:
            pcgrp.append(piece)
        if sq == None:
            stagingarea = self.__board.emptyspace("Space")
            idx = random.randint(0, len(stagingarea)-1)
            sq = stagingarea[idx]
        piece.setPosition(sq)

    def placehuman(self, person, sq=None):
        self.placeplayerpiece(person, self.__playerpieces, sq)

    def placerobot(self, robot, sq=None):
        self.placeplayerpiece(robot, self.__playerpieces, sq)

    def movemutants(self):
        for i in range(len(self.__mutants)):
            nummoves = 0
            while self.__mutants[i].moveindirection(None):
                nummoves += 1
            self.__mutants[i].resetMovement()

    def mutantattack(self):
        for i in range(len(self.__mutants)):
            if self.__mutants[i].alive():
                self.__mutants[i].attacktarget()

    def play(self, maxloops=10000000):
        self.__display.runLoop(maxloops)

    @property
    def mutantturn(self):
        return(self.__mutantturn)

    @mutantturn.setter
    def mutantturn(self, onoff):
        """

        :type onoff: Boolean
        """
        self.__mutantturn = onoff

    def clearfoci(self):
        for i in range(len(self.__playerpieces)):
            self.__playerpieces[i].focus = False

    def piecewithfocus(self):
        for i in range(len(self.__playerpieces)):
            if self.__playerpieces[i].focus:
                return (self.__playerpieces[i])
        return (None)

    def movepiecewithfocus(self, sq, dirct=None):
        """
        Only interested in moving player pieces this way.  Mutants move on their own.
        :param sq: Square
        :return: boolean
        """
        ret = False
        for i in range(len(self.__playerpieces)):
            if self.__playerpieces[i].focus:
                if dirct == None:
                    ret = self.__playerpieces[i].movetosquare(sq)
                else:
                    ret = self.__playerpieces[i].moveindirection(dirct)
                break
        return(ret)

    def wavecomplete(self):
        return(len(self.__playerpieces) == 0 or len(self.__mutants) == 0)
        #return(len(self.__mutants) == 0)

    def nextwave(self):
        if self.__wave == len(mutants.Constants.Constants.MUTANTSPERWAVE):
            self.__board.addmessage("")
            if len(self.__playerpieces) == 0:
                self.__board.addmessage("Game over!  The evil mutants have triumphed!")
            else:
                self.__board.addmessage("Game over!  You have prevailed over the mutants!")
            self.__board.addmessage("")
            return(False)
        self.__wave += 1
        self.__board.addmessage("")
        self.__board.addmessage("        Wave " + str(self.__wave) + "!")
        self.__board.clearmutants()
        self.__mutants = []
        self.getmutants()
        self.placemutants()
        return (True)

    def clearoutdeadpieces(self, pieces):
        i = len(pieces) - 1
        while i >= 0:
            if not pieces[i].alive():
                del pieces[i]
            i -= 1

    def clearoutdead(self):
        self.clearoutdeadpieces(self.__playerpieces)
        self.clearoutdeadpieces(self.__mutants)

    def nextturn(self):
        for i in range(len(self.__playerpieces)):
            self.__playerpieces[i].resetMovement()
            self.__playerpieces[i].hasattacked = False
        for i in range(len(self.__mutants)):
            self.__mutants[i].resetMovement()
            self.__mutants[i].hasattacked = False

if __name__ == "__main__":
    import doctest
    doctest.testmod()
