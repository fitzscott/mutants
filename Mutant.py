__author__ = 'Fitz'

import random

import mutants.MovingPiece
import mutants.ExteriorSpace
import mutants.Space
import mutants.Door
import mutants.Equipment
import mutants.Robot
import mutants.Human
import mutants.Wall
import mutants.Constants

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
        mutants.Human.Human
    ]

    def __init__(self, name="Mutant", image="Mutant", movePts=2, hitPts=2, h2h=2):
        super().__init__(name, image, movePts, hitPts)
        self.handtohand = h2h
        self.__dir2go = 0
        # We will need to figure out the "last space" logic later.  It is intended
        # to keep mutants from bouncing back & forth between two spaces.
        self.__lastSpace = None
        self.__doorsExplored = []
        self.__squaresExplored = []

    def doneLooking(self, sq):
        nm = sq.showing.name
        return(nm != "Wall" and nm != "Door" and nm != "Mutant")

    def checkDirection(self, sq, dir, dist, seenGood, seenOk, diridx):
        if sq == None:
            return (False)
        nsq = sq.getNeighbor(dir, dist)
        if nsq == None:
            return (False)
        if dist > mutants.Constants.Constants.MAXMUTANTEYESIGHT:
            return (False)
        #print("Looking at " + nsq.showing.name + " in direction " + \
        # mutants.Constants.Constants.dirStrings[diridx] + \
        #    " at distance " + str(dist))
        if type(nsq.showing) in self.MUTANTINTEREST:
            idx = self.MUTANTINTEREST.index(type(nsq.showing))
            if idx > seenOk[diridx]:
                seenOk[diridx] = idx
                if nsq not in self.__squaresExplored and \
                        nsq not in self.__doorsExplored:
                    seenGood[diridx] = idx
                    #print("        Really good!")
                #print("I see something more interesting: " + nsq.showing.name)
        return(self.doneLooking(nsq))

    def chooseDirection(self):
        sq = self.square
        distance = 1
        things2find = True
        thingsseen = [-1, -1, -1, -1]   # up, down, left, right
        thingsseen2ndary = [-1, -1, -1, -1]   # up, down, left, right
        up = True
        down = True
        left = True
        right = True
        # look around a bit
        while things2find:
            if up:
                up = self.checkDirection(sq, mutants.Constants.Constants.UP, distance, \
                                         thingsseen, thingsseen2ndary, 0)
            if down:
                down = self.checkDirection(sq, mutants.Constants.Constants.DOWN, distance, \
                                         thingsseen, thingsseen2ndary, 1)
            if left:
                left = self.checkDirection(sq, mutants.Constants.Constants.LEFT, distance, \
                                         thingsseen, thingsseen2ndary, 2)
            if right:
                right = self.checkDirection(sq, mutants.Constants.Constants.RIGHT, distance, \
                                         thingsseen, thingsseen2ndary, 3)
            distance += 1
            things2find = up or down or left or right
        # Record how many ties we have for chosen direction
        #print("Primary seen: " + self.stringseen(thingsseen))
        #print("Secondary seen: " + self.stringseen(thingsseen2ndary))
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
            mistr = str(self.MUTANTINTEREST[seen[i]]).split(".")[2]
            strret += str(i) + ":" + mutants.Constants.Constants.dirStrings[diridx] + ":" + \
                      str(seen[i]) + ":" + mistr + " "
        return (strret)

    def moveindirection(self, direction):
        dirct = self.chooseDirection()
        #print("Moving mutant in direction " + str(dirct) + ": " + mutants.Constants.Constants.dirStrings[diridx])
        # this is not elegant...  need to figure out how to sew up the direction
        # strings and the offset from Constants.
        if dirct == 0:
            go_to = mutants.Constants.Constants.UP
        elif dirct == 1:
            go_to = mutants.Constants.Constants.DOWN
        elif dirct == 2:
            go_to = mutants.Constants.Constants.LEFT
        elif dirct == 3:
            go_to = mutants.Constants.Constants.RIGHT
        else:    # not moving this turn, I guess...
            #print("I can't move...  boo hoo hoo")
            return(False)

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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
