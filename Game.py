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
        self.__wave = 0
        self.__mutants = []
        self.__humans = None
        self.__robots = None
        self.__display = mutants.Display.Display(self)
        self.__display.loadResources(boardname)
        self.__board = self.__display.board

    def getmutants(self):
        # If the board comes pre-defined with mutants, don't add new ones.
        resmuties = self.__board.residentmutants()
        if len(resmuties) > 0:
            self.__mutants = resmuties
            return
        nummutants = mutants.Constants.Constants.MUTANTSPERWAVE[self.__wave]
        self.__mutants = []
        for i in range(nummutants):
            self.__mutants.append(mutants.Mutant.Mutant())

    def placemutants(self):
        stagingarea = self.__board.emptyexterior()
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

    def movemutants(self):
        #print("Game is moving the mutants - size: " + str(len(self.__mutants)))
        for i in range(len(self.__mutants)):
            #print("Moving mutant " + str(i) + ": " + self.__mutants[i].name)
            self.__mutants[i].move(None)
            self.__mutants[i].resetMovement()

    def play(self, maxloops=10000000):
        self.__display.runLoop(maxloops)

    def nextwave(self):
        self.__wave += 1
        print("Wave " + str(self.__wave + 1) + "!")
        self.__board.clearmutants()
        self.__mutants = []
        self.getmutants()
        self.placemutants()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
