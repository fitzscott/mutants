__author__ = 'Fitz'

import random
import math

import mutants.Square
import mutants.Constants
import mutants.Mutant
import mutants.RadioactiveMutant
import mutants.LeaderMutant
import mutants.Human
import mutants.Robot

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
        self.__messages = []
        self.__maxmessages = 1
        self.__mutants = []
        self.__playerpieces = []
        self.__hypth = 10
        self.__hypcntdn = 4

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

    def emptyspace(self, inexterior="ExteriorSpace"):
        extsq = []
        for i in range(self.height):
            for j in range(self.width):
                sq = self.getSquare(j, i)
                if sq.getTerrain().name == inexterior:
                    if inexterior == "ExteriorSpace"  and sq.hasequipment():
                         sq.takeequipment()
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

    def distance(self, sq1, sq2, checkifblocked=False, checkdoors=False):
        """
        Return distance between two squares on the board.
        :param sq1: Square
        :param sq2: Square
        :param checkifblocked: Boolean
        :return: integer of distance; -1 if blocked & check is requested
        """
        xcurincr = 0.0
        ycurincr = 0.0
        xdif = sq2.getXpos() - sq1.getXpos()
        if xdif > 0:
            xdirct = mutants.Constants.Constants.RIGHT
        else:
            xdirct = mutants.Constants.Constants.LEFT
        ydif = sq2.getYpos() - sq1.getYpos()
        if ydif > 0:
            ydirct = mutants.Constants.Constants.DOWN
        else:
            ydirct = mutants.Constants.Constants.UP
        dist = abs(xdif) + abs(ydif)        # simple square-bound movement distance
        xincrdif = xdif / dist
        yincrdif = ydif / dist
        sqonpath = sq1
        if checkifblocked:
            #while sqonpath != sq2:
            while sqonpath != sq2 and (abs(xcurincr) < abs(xdif) or abs(ycurincr) < abs(ydif)):
                xcurincr += xincrdif
                if abs(xcurincr) >= 1:
                    sqonpath = sqonpath.getNeighbor(xdirct)
                    xcurincr -=  math.copysign(1, xdif)
                ycurincr += yincrdif
                if abs(ycurincr) >= 1:
                    sqonpath = sqonpath.getNeighbor(ydirct)
                    ycurincr -= math.copysign(1, ydif)
                if sqonpath != sq2 and sqonpath != sq1 and sqonpath.isblocking(checkdoors):
                    print("Can't get there from here")
                    dist = -1
                    break
            assert(dist == -1 or sqonpath == sq2)
        return (dist)

    def addmessage(self, msg):
        if len(self.__messages) > 1 and msg[0:8] == self.__messages[-1][0:8]:
            del self.__messages[-1]
        if len(self.__messages) >= self.__maxmessages:
            del self.__messages[0]
        self.__messages.append(msg)

    @property
    def messages(self):
        return(self.__messages)

    @property
    def maxmessages(self):
        return(self.__maxmessages)

    @maxmessages.setter
    def maxmessages(self, cnt):
        self.__maxmessages = cnt

    def getmutants(self, wave, overridenum=0):
        import mutants.FileChar

        # If the board comes pre-defined with mutants, don't add new ones.
        resmuties = self.residentmutants()
        if len(resmuties) > 0:
            self.__mutants = resmuties
            return
        if overridenum:
            nummutants = overridenum
        else:
            nummutants = mutants.Constants.Constants.MUTANTSPERWAVE[wave - 1]

        fc = mutants.FileChar.FileChar()
        self.__mutants = []
        bats = pipes = shotguns = 0
        for i in range(nummutants):
            if i % 10 == 8 or i % 10 == 9:
                mutie = mutants.RadioactiveMutant.RadioactiveMutant()
                mutie.pickup(fc.getEquipment(";"))
            elif i % 10 == 3:
                mutie = mutants.LeaderMutant.LeaderMutant()
                mutie.pickup(fc.getEquipment("*"))
            else:
                mutie = mutants.Mutant.Mutant()
            mutie.number = i
            # hand out goodies to the mutants
            if random.randint(1, 6) + random.randint(1, 6) >= 11:       # some shotgun hunters
                mutie.pickup(fc.getEquipment("*"))
                shotguns +=1
            elif random.randint(1, 6) + random.randint(1, 6) >= 10:       # some plumbers
                mutie.pickup(fc.getEquipment("|"))
                pipes += 1
            elif random.randint(1, 6) + random.randint(1, 6) >= 9:       # lots of baseball players, apparently
                mutie.pickup(fc.getEquipment("!"))
                bats += 1
            self.__mutants.append(mutie)
        print("Handed out " + str(bats) + " bats, " + str(pipes) + " pipes, and " + str(shotguns) + " shotguns.")

    def placemutants(self):
        stagingarea = self.emptyspace()
        numempties = len(stagingarea) - len(self.__mutants)
        print("We have " + str(numempties) + " more spaces available than mutants.")
        for i in range(numempties):
            stgsiz = len(stagingarea)
            idx = random.randint(0, stgsiz-1)
            del stagingarea[idx]
        failedplacements = 0
        for i in range(len(self.__mutants)):
            if i < len(stagingarea):
                self.placemutant(self.__mutants[i], stagingarea[i])
            else:
                failedplacements += 1
        print("Had " + str(failedplacements) + " failed mutant placements.")

    def placemutant(self, mutie, sq):
        if mutie not in self.__mutants:
            print("Appending fixed-position mutant")
            self.__mutants.append(mutie)
        mutie.setPosition(sq)

    def placeplayerpiece(self, piece, pcgrp, sq=None):
        if piece not in pcgrp:
            pcgrp.append(piece)
        if sq == None:
            stagingarea = self.emptyspace("Space")
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

    def clearoutdeadpieces(self, pieces):
        i = len(pieces) - 1
        while i >= 0:
            if not pieces[i].alive():
                if pieces[i].square != None:
                    pieces[i].square.removePiece()
                del pieces[i]
            i -= 1

    def clearoutdead(self):
        self.clearoutdeadpieces(self.__playerpieces)
        self.clearoutdeadpieces(self.__mutants)

    def clearfoci(self):
        for i in range(len(self.__playerpieces)):
            self.__playerpieces[i].focus = False

    def piecewithfocus(self):
        for i in range(len(self.__playerpieces)):
            if self.__playerpieces[i].focus:
                return (self.__playerpieces[i])
        return (None)

    def resetpieces(self, wave):
        for i in range(len(self.__playerpieces)):
            self.__playerpieces[i].resetMovement()
            self.__playerpieces[i].hasattacked = False
        for i in range(len(self.__mutants)):
            self.__mutants[i].resetMovement()
            self.__mutants[i].hasattacked = False
        if len(self.__mutants) <= self.__hypth + random.randint(wave, 10):
            print("In hyper-threshhold: " + str(self.__hypth) + ", countdown at " + str(self.__hypcntdn))
            self.__hypcntdn -= 1
            if self.__hypcntdn <= 0:
                self.addmessage("****  Mutants have gone hyper-radioactive!  *****")
                self.hypermutants(wave)
                self.__hypcntdn = 4     # reset for next time
            else:
                self.addmessage("*****  Mutants will be going hyper-radioactive soon!  *****")
        # also clean out any indicators in squares
        for sq in self.__squares:
            sq.indicator = None

    def playerpiececount(self):
        return(len(self.__playerpieces))

    def humanpiececount(self):
        cnt = 0
        for piece in self.__playerpieces:
            if isinstance(piece, mutants.Human.Human):
                cnt += 1
        return (cnt)

    def mutantpiececount(self):
        return(len(self.__mutants))

    def cripplerobots(self):
        for piece in self.__playerpieces:
            if isinstance(piece, mutants.Robot.Robot):
                piece.decrRemaining(piece.getRemainingMovement())
                piece.movement = -1

    def hypermutants(self, wave):
        import mutants.HyperRadioactiveMutant

        if wave == 3:
            glomin = 10
        else:
            glomin = 7

        for mutidx in range(len(self.__mutants)):
            hypmutie = mutants.HyperRadioactiveMutant.HyperRadioactiveMutant(self.__mutants[mutidx], glomin)
            sq = self.__mutants[mutidx].square
            sq.removePiece()
            hypmutie.setPosition(sq)
            self.__mutants[mutidx] = hypmutie

    @property
    def hyperthreshhold(self):
        return (self.__hypth)

    @hyperthreshhold.setter
    def hyperthreshhold(self, hypth):
        self.__hypth = hypth



if __name__ == "__main__":
    import doctest
    doctest.testmod()

