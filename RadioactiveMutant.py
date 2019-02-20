__author__ = 'Fitz'

import random

import Mutant as m
import Constants as const

class RadioactiveMutant(m.Mutant):
    """
    Radioactive mutants - faster, but also "glow 'n' go", sending radiation outward
    """
    def __init__(self):
        super().__init__("RadioactiveMutant", "RadioactiveMutant", 4, 4, 3)

    def glowngo(self, mintogo=11):
        """
        1 in 12 chance the mutant will explode in a radioactive spray.
        :return:
        """
        # I don't know why this happens - bug
        if self.square == None:
            print(self.fullname + " has no square - bailing out.")
            return
        if random.randint(1,6) + random.randint(1,6) >= mintogo:
            self.message(self.fullname + " glows with radioactivity & vaporizes itself (and maybe others)")
            # simulate the gamma rays by boosting hand-to-hand & attacking
            self.handtohand += random.randint(1, 6)
            for dirct in const.Constants.directions:
                self.hasattacked = False
                attsq = self.square.getNeighbor(dirct, 1)
                if attsq != None and attsq.isOccupied():
                    attsq.attackpiece(self.handtohand)
            self.square.attackpiece(self.handtohand)

    def resetMovement(self):
        super().resetMovement()
        self.glowngo()

    @property
    def wantpickup(self):
        retval = True
        if self.carried != None:
            weapon = self.carried.name
            if weapon == "Chainsaw":        # they love their chainsaws
                retval = False
        return (retval)

