__author__ = 'Fitz'

import random

import mutants.Constants
import mutants.MovingPiece
import mutants.ExteriorSpace
import mutants.Space
import mutants.Door
import mutants.Wall
import mutants.Equipment
import mutants.Robot
import mutants.Human
import mutants.Professor

class Mutant(mutants.MovingPiece.MovingPiece):
    """
    The most important class in the game. Well, the one the game is named after, I guess.
    >>> m = Mutant()
    >>> print(m.MUTANTINTEREST[4])
    <class 'mutants.Equipment.Equipment'>
    """

    # hierarchy of things of interest to mutants
    MUTANTINTEREST = [
        #mutants.Wall.Wall,
        mutants.ExteriorSpace.ExteriorSpace,
        mutants.Space.Space,
        mutants.Door.Door,
        mutants.Equipment.Equipment,
        mutants.Robot.Robot,
        mutants.Human.Human,
        mutants.Professor.Professor
    ]

    def __init__(self, name="Mutant", image="Mutant2", movePts=2, hitPts=3, h2h=3):
        image = name + "0" + str(random.randint(1,9))
        super().__init__(name, image, movePts, hitPts)
        self.handtohand = h2h
        self.__dir2go = 0
        # We will need to figure out the "last space" logic later.  It is intended
        # to keep mutants from bouncing back & forth between two spaces.
        self.__lastSpace = None
        self.__doorsExplored = []
        self.__squaresExplored = []
        self.__number = 0
        self.ranged = 2

    @property
    def number(self):
        return(self.__number)

    @number.setter
    def number(self, num):
        self.__number = num

    @property
    def fullname(self):
        return(self.name + " " + str(self.number))

    def moretosee(self, sq):
        nm = sq.showing.name
        #return(nm != "Wall" and nm != "Door" and nm != "Mutant")
        return(nm != "Wall" and nm != "Mutant")

    def evaluatesquare(self, sq, dirct, dist=1):
        if sq == None:
            return (None)
        nsq = sq.getNeighbor(dirct, dist)
        if nsq == None:
            return (None)
        if dist > mutants.Constants.Constants.MAXMUTANTEYESIGHT:
            return (None)
        if not self.moretosee(nsq):
            return (None)
        return(nsq)

    def checkDirection(self, sq, dirct, dist, seenGood, seenOk, diridx):
        nsq = self.evaluatesquare(sq, dirct, dist)
        if nsq == None:
            return (False)
        if type(nsq.showing) not in self.MUTANTINTEREST:
            return (False)
        idx = self.MUTANTINTEREST.index(type(nsq.showing))
        if idx > seenOk[diridx]:
            seenOk[diridx] = idx
            if idx > 3 or nsq not in self.__squaresExplored and \
                    nsq not in self.__doorsExplored:
                seenGood[diridx] = idx
        return(True)

    def chooseDirection(self):
        #self.message(self.fullname + ": Choosing direction")
        sq = self.square
        distance = 1
        things2find = True
        thingsseen = [-1, -1, -1, -1]   # up, down, left, right
        thingsseen2ndary = [-1, -1, -1, -1]   # up, down, left, right
        dirbools = [True, True, True, True]
        # look around a bit
        while things2find:
            for diridx in range(len(dirbools)):
                if dirbools[diridx]:
                    dirbools[diridx] = self.checkDirection(sq, mutants.Constants.Constants.directions[diridx], \
                                                        distance, thingsseen, thingsseen2ndary, diridx)
                    if thingsseen[diridx] > 3:      #  A real target
                        dirbools[diridx] = False
            distance += 1
            things2find = dirbools[0] or dirbools[1] or dirbools[2]or dirbools[3]
        #self.message(self.fullname + " pri: " + self.stringseen(thingsseen) + \
        #    ", 2nd: " + self.stringseen(thingsseen2ndary))
        # Record how many ties we have for chosen direction
        dirsatmax = []
        max = maxidx = -1
        for i in range(len(thingsseen)):
            if thingsseen[i] > max:
                max = thingsseen[i]
                maxidx = i
                dirsatmax = []
            if thingsseen[i] == max and max > -1:
                dirsatmax.append(i)
        #print("Initial chosen direction is " + str(maxidx) + " = " + mutants.Constants.Constants.dirStrings[diridx])
        # If there are ties for chosen direction, pick one randomly.
        # Not ideal, but maybe it'll be enough.
        lendam = len(dirsatmax)
        if (lendam > 1):
            tiebreaker = random.randint(0, lendam-1)
            #print("Length of tied array is " + str(lendam) + ", tiebreaker is " + str(tiebreaker))
            maxidx = dirsatmax[tiebreaker]
        #print("Second chosen direction is " + str(maxidx) + " = " + mutants.Constants.Constants.dirStrings[diridx])
        if maxidx == -1:
            # Need to go through the secondary list
            nonnegones = []
            for i in range(len(thingsseen2ndary)):
                if thingsseen2ndary[i] != -1:
                    nonnegones.append(i)
            if len(nonnegones) == 1:
                #print("Non-negative - only 1 option")
                maxidx = nonnegones[0]
            elif len(nonnegones) > 1:
                nnidx = random.randint(0, len(nonnegones)-1)
                #print("Non-negative - " + str(len(nonnegones)) +  " options, chose " + str(nnidx) + \
                #    " = " + str(nonnegones[nnidx]))
                maxidx = nonnegones[nnidx]
            else:
                maxidx = -1    # all dressed up with nowhere to go
        #print("Final chosen direction is " + str(maxidx) + " = " + mutants.Constants.Constants.dirStrings[diridx])
        return (maxidx)     # direction to go

    def stringseen(self, seen):
        strret = ""
        for i in range(len(seen)):
            mistr = str(self.MUTANTINTEREST[seen[i]]).split(".")[2][0:4]
            strret += mutants.Constants.Constants.dirStrings[i] + ":" + mistr + " "
        return (strret)

    def moveindirection(self, direction):
        dirct = self.chooseDirection()
        #self.message("Moving mutant in direction " + str(dirct) + ": " + mutants.Constants.Constants.dirStrings[dirct])
        if dirct != -1:
            go_to = mutants.Constants.Constants.directions[dirct]
        else:    # not moving this turn, I guess...
            self.message(self.fullname + " can't move...  boo hoo hoo")
            return(False)

        # check if it's a door.  Mutants must smash doors to go through
        if len(self.__squaresExplored) > mutants.Constants.Constants.MAXMUTANTSQUAREMEM:
            #print("Resetting squares explored")
            self.__squaresExplored = []
            if len(self.__doorsExplored) >= 1:
                self.__doorsExplored = []
        currsq = self.getPosition()
        if len(self.__squaresExplored) > 2 and self.__squaresExplored[-1] == self.__squaresExplored[-2]:
            #print("Deleting from squares explored, size " + str(len(self.__squaresExplored)))
            del self.__squaresExplored[-1]
        elif currsq not in self.__squaresExplored:
            self.__squaresExplored.append(currsq)
        if super().moveindirection(go_to):
            self.__lastSpace = currsq
            # Trick mutants into not going back & forth through same door
            if currsq.getTerrain().name == "Door":
                if currsq not in self.__doorsExplored:
                    self.__doorsExplored.append(currsq)
                    if len(self.__doorsExplored) > 3:
                        del self.__doorsExplored[0]
            return (True)
        else:
            return (False)

    def attacktarget(self):
        target = None
        if self.carried != None and self.carried.effectiverange > 0:
            maxdist = self.carried.effectiverange
        else:
            maxdist = 1         # hand-to-hand only
        currdist = 1
        while currdist <= maxdist:
            for dirct in mutants.Constants.Constants.directions:
                goodsq = self.evaluatesquare(self.getPosition(), dirct, currdist)
                if goodsq != None and type(goodsq.showing) in self.MUTANTINTEREST \
                        and self.MUTANTINTEREST.index(type(goodsq.showing)) > 3:
                    self.message(self.fullname + " is attacking " + goodsq.showing.fullname)
                    self.attack(goodsq)
                    currdist = maxdist      # make sure we exit the outer loop
                    break       # only get to attack once
            currdist += 1

    @property
    def wantpickup(self):
        retval = True
        if self.carried != None:
            weapon = self.carried.name
            if weapon == "Axe" or weapon == "Shotgun":
                retval = False
        return (retval)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
