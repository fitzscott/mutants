__author__ = 'Fitz'

import random
import PlayerPiece as pp

class Robot(pp.PlayerPiece):
    """
    Represents the human's helpers, carrying rifles.
    >>> r = Robot()
    >>> r.number = 1148
    >>> print("Robot full name is " + r.fullname)
    Robot full name is RO1148
    """
    def __init__(self, madefromscrap=False):
        import FileChar as fc

        super().__init__("Robot")
        self.__focus = False
        self.__number = random.randint(0, 8000) + 1000
        fc = fc.FileChar()
        rifle = fc.getEquipment(">")
        if not madefromscrap:
            self.pickup(rifle)
            self.wantpickup = False

    @property
    def fullname(self):
        return("RO" + str(self.__number))

    @property
    def number(self):
        return(self.__number)

    @number.setter
    def number(self, num):
        self.__number = num

    def deathmessage(self):
        self.message("    " + self.fullname + " has been destroyed!")

    def healthyself(self):
        if self.carried != None and self.carried.name == "SpareParts":
            self.heal(self.carried.heals)
            self.carried = None
        else:
            self.message(self.fullname + " needs spare parts to repair itself.")

    @property
    def indicatorstring(self):
        return "Debris"

