__author__ = 'Fitz'

import random

from mutants.Piece import Piece
import mutants.Constants

class MovingPiece(Piece):
    """
    Represents a piece that can move, either under the player's control or the computer's.
    >>> mp = MovingPiece("Ozzie", None)
    >>> mp.name
    'Ozzie'
    >>> mp.handtohand = 4
    >>> mp.handtohand
    4
    >>> if not mp.damage(1): print(mp.name + " is dead.  Aww....")
    Ozzie is dead.  Aww....
    """
    def __init__(self, name, image, movePts = 0, hitPts = 1):
        super().__init__(name, image)
        self.__movePts = movePts
        self.__moveRemaining = self.__movePts
        self.__hitPts = hitPts
        self.__handtohand = 0
        self.__ranged = 0
        self.__carried = None
        self.__lastsquare = None
        self.__hasattacked = False
        self.__wantpickup = True
        self.__maxhitpts = hitPts

    def resetMovement(self):
        self.__moveRemaining = self.__movePts

    def getRemainingMovement(self):
        return (self.__moveRemaining)

    @property
    def movement(self):
        return(self.__movePts)

    @movement.setter
    def movement(self, mvpts):
        self.__movePts = mvpts

    def canmove(self):
        #print("In canmove for " + self.fullname + " w/ move remaining: " + str(self.__moveRemaining))
        return (self.__moveRemaining > 0)

    def decrRemaining(self, howmany=1):
        self.__moveRemaining -= howmany

    @property
    def lastsquare(self):
        return(self.__lastsquare)

    def message(self, msg):
        sq = self.getPosition()
        if sq != None:
            sq.sendmessage(msg)

    def movetosquare(self, newsq, currsq=None):
        import mutants.Mutant

        if currsq == None:
            currsq = self.__lastsquare = self.getPosition()
        if newsq == currsq:
            return (False)
        if (newsq != None):
            dist = currsq.distanceto(newsq)
            if dist == -1:
                self.message("Cannot move " + self.fullname + " through that.")
                return (False)
            if (dist <= self.getRemainingMovement()):
                if (self.setPosition(newsq)):
                    currsq.removePiece()
                    self.decrRemaining(dist)
                    if not isinstance(self, mutants.Mutant.Mutant):
                        # + " moving " + self.fullname + " to (" + \
                        #             str(newsq.getXpos()) + ", " + str(newsq.getYpos()) + ")")
                        self.message(self.synopsis())
                    return (True)
                #else:
                #    print("Piece " + self.name + " cannot move to that square.")
            #else:
            #    print("Insufficient remaining movement for " + self.fullname)
        #else:
        #    print("Piece " + self.name + " cannot move off the board.")
        return (False)

    def moveindirection(self, direction):
        #print("Moving " + self.name)
        if (self.__moveRemaining <= 0):
            #self.message(self.name + " has no remaining movement points.")
            return (False)

        currsq = self.__lastsquare = self.getPosition()
        newsq = currsq.getNeighbor(direction)
        return (self.movetosquare(newsq, currsq))

    def damage(self, amount):
        self.__hitPts -= amount
        if self.__hitPts <= 0:
            self.deathmessage()
        return(self.__hitPts <= 0)

    def deathmessage(self):
        self.message("    " + self.fullname + " is dead!")

    def alive(self):
        return(self.__hitPts > 0)

    def heal(self, amount):
        if self.__hitPts + amount > self.__maxhitpts:
            self.message("Can only heal to " + self.fullname + "'s max of " + str(self.__maxhitpts))
            self.__hitPts = self.__maxhitpts
        else:
            self.__hitPts += amount

    @property
    def handtohand(self):
        if (self.__carried != None):
            totalh2h = self.__handtohand + self.__carried.handtohandhitbonus
        else:
            totalh2h = self.__handtohand
        return (totalh2h)

    @handtohand.setter
    def handtohand(self, h2h):
        self.__handtohand = h2h

    @property
    def handtohanddamage(self):
        if (self.__carried != None):
            equipdamage = self.__carried.handtohanddamagebonus
        else:
            equipdamage = 0
        return (self.__handtohand + equipdamage)

    @property
    def ranged(self):
        if (self.__carried != None):
            totalranged = self.__ranged + self.__carried.rangedhitbonus
        else:
            totalranged = 0    #  Cannot do a ranged attack w/o a ranged weapon
        return (totalranged)

    @ranged.setter
    def ranged(self, ranged):
        self.__ranged = ranged

    @property
    def rangeddamage(self):
        if (self.__carried != None):
            damage = self.__carried.rangeddamage
        else:
            damage = 0      # this should never happen
        return (damage)

    def pickup(self, tool):
        """
        move into a square and pick up what's there
        :type tool: mutants.Equipment.Equipment
        """
        if self.__carried != None and self.__lastsquare != None:
            self.__lastsquare.addequipment(self.__carried)
        self.__carried = tool

    @property
    def hasattacked(self):
        return(self.__hasattacked)

    @hasattacked.setter
    def hasattacked(self, att):
        self.__hasattacked = att

    def hthattack(self, sq):
        # Determine if the attack hits
        dieroll = random.randint(0, 5) + 1
        if self.carried != None:
            weapdescr = " with a " + self.carried.name
        else:
            weapdescr = ""
        if dieroll + self.handtohand > mutants.Constants.Constants.TOHIT:
            self.message(self.fullname + " attacks " + sq.piece.fullname + weapdescr + " for " + \
                         str(self.handtohanddamage) + " damage.")
            sq.attackpiece(self.handtohanddamage)
        else:
            self.message(self.fullname + " missed " + sq.piece.fullname + weapdescr)
        return (True)

    def rngattack(self, sq, dist):
        if self.ranged:
            # if ranged is positive, must have a ranged weapon
            if self.__carried.effectiverange >= dist:
                if dist > self.__carried.effectiverange // 2:
                    rangepenalty = - 1
                else:
                    rangepenalty = - 1
                # Determine if the attack hits
                dieroll = random.randint(0, 5) + 1
                if dieroll + self.ranged >= mutants.Constants.Constants.TOHIT:
                    # It's a hit!
                    damage = self.rangeddamage + rangepenalty
                    if self.carried != None:
                        weapdescr = " with a " + self.carried.name + " "
                    else:
                        weapdescr = ""
                    self.message(self.fullname + " hit " + sq.piece.fullname + weapdescr + " for " \
                                 + str(damage) + " damage!")
                    sq.attackpiece(damage)
                else:
                    self.message(self.fullname + " missed "+ sq.piece.fullname + " with the " \
                                 + self.__carried.name)
                ret = True
            else:
                self.message("That target is out of range.")
                ret = False
        else:
            self.message(self.fullname + " has nothing to attack with at range.")
            ret = False
        return (ret)

    def attack(self, sq):
        result = False
        if self.hasattacked:
            return (False)
        dist = self.getPosition().distanceto(sq, True, True)
        if dist == -1:
            self.message(self.fullname + " cannot hit that target.")
        else:
            if dist == 1:
                self.hasattacked = self.hthattack(sq)
            else:
                self.hasattacked = self.rngattack(sq, dist)
            result = self.hasattacked
        return (result)

    def synopsis(self):
        if self.__carried == None:
            carriedstr = "nothing"
        else:
            carriedstr = self.__carried.name
        return(self.fullname + ", hit points: " + str(self.__hitPts) + ", remaining move: " \
               + str(self.getRemainingMovement()) + ", carrying " + carriedstr)

    @property
    def carried(self):
        return(self.__carried)

    @carried.setter
    def carried(self, whattocarry):
        self.__carried = whattocarry

    @property
    def wantpickup(self):
        return (self.__wantpickup)

    @wantpickup.setter
    def wantpickup(self, pickitup):
        self.__wantpickup = pickitup

if __name__ == "__main__":
    import doctest
    doctest.testmod()

