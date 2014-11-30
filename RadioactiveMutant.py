__author__ = 'Fitz'

import random

import mutants.Mutant
import mutants.Constants

class RadioactiveMutant(mutants.Mutant.Mutant):
    """
    Radioactive mutants - faster, but also "glow 'n' go", sending radiation outward
    """
    def __init__(self):
        super().__init__("RadioactiveMutant", "RadioactiveMutant", 4, 4, 3)

    def glowngo(self):
        """
        1 in 12 chance the mutant will explode in a radioactive spray.
        :return:
        """
        if random.randint(1,6) + random.randint(1,6) >= 11:
            self.message(self.fullname + " glows with radioactivity & vaporizes itself (and maybe others)")
            # simulate the gamma rays by boosting hand-to-hand & attacking
            self.handtohand += random.randint(1, 6)
            for dirct in mutants.Constants.Constants.directions:
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

