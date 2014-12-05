__author__ = 'Fitz'

import mutants.RadioactiveMutant

class HyperRadioactiveMutant(mutants.RadioactiveMutant.RadioactiveMutant):
    """
    HyperRadioactiveMutant - obvious, right?  Really, it's to hurry the game along
    when there aren't very many mutants left on the board.  These are those remaining
    mutants, upgraded to be faster and stronger and more likely to spontaneously combust.
    """
    def __init__(self, origmutant, mintogo=7):     # kind of a copy constructor
        super().__init__()      # but we're changing a bunch
        self.name = "HyperRadioactiveMutant"
        self.handtohand = origmutant.handtohand + 3
        self.movement = origmutant.movement + 3
        self.number = origmutant.number
        self.carried = origmutant.carried
        self.ranged = 4     # ranged, deranged, whatever
        self.image = self.name + "0" + origmutant.image[-1]
        self.__mintogo = mintogo

    def glowngo(self, mintogo=-1):
        if mintogo == -1:
            mintogo = self.__mintogo
        super().glowngo(mintogo)      # more than half the time for waves 1 & 2

    @property
    def wantpickup(self):
        retval = True
        if self.carried != None:
            weapon = self.carried.name
            if weapon == "Axe" or weapon == "Chainsaw":     # bloodier is better
                retval = False
        return (retval)



