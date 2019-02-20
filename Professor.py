__author__ = 'Fitz'

import random

import Human as hum
import Robot as rob
import Constants as const

class Professor(hum.Human):
    """
    The Professor - bright but not good in a fight.  Really, he's only good for his
    special ability:  Making robots out of spare parts.
    """
    def __init__(self):
        super().__init__("Professor")
        self.__focus = False

    def special(self):
        """
        The professor makes robots out of spare parts.
        :return:
        """
        if self.hasattacked:
            self.message(self.fullname + " will have to try again later.")
            return (False)

        if self.carried == None or self.carried.name != "SpareParts":
            self.message(self.fullname + " needs spare parts to make a robot.")
            return (False)

        # He succeeds half the time.
        if random.randint(1, 6) >= 4:
            robot = rob.Robot(True)       # made from scrap => no gun
            placetoput = None
            # figure out where to put it
            if self.lastsquare != None and not self.lastsquare.isOccupied():
                placetoput = self.lastsquare
            else:
                # check around
                for dirct in const.Constants.directions:
                    nsq = self.square.getNeighbor(dirct)
                    if nsq != None and not nsq.isOccupied() and nsq.getTerrain().movethru():
                        placetoput = nsq
                        break
            if placetoput != None:
                placetoput.board.placerobot(robot, placetoput)
                self.carried = None
                self.hasattacked = True
            else:
                self.message(self.fullname + " cannot find a place for the new robot.")
        else:
            self.message(self.fullname + " needs some more time to create a robot - try again later.")
            self.hasattacked = True
            return (False)





