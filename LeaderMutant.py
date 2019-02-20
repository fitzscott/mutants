__author__ = 'Fitz'

import Mutant as m

class LeaderMutant(m.Mutant):
    """
    Boss mutant.  Not like a boss monster in other games -
    more like a boss in the workplace.
    """
    def __init__(self):
        super().__init__("LeaderMutant", "LeaderMutant", 5, 8, 5)

    @property
    def wantpickup(self):
        retval = True
        if self.carried != None:
            weapon = self.carried.name
            if weapon == "Rifle" or weapon == "Shotgun":    # Leaders prefer ranged weapons
                retval = False
        return (retval)
