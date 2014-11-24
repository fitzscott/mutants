__author__ = 'Fitz'

import random
import mutants.PlayerPiece
import mutants.FileChar

class Robot(mutants.PlayerPiece.PlayerPiece):
    """
    Represents the human's helpers, carrying rifles.
    >>> r = Robot()
    >>> r.number = 1148
    >>> print("Robot full name is " + r.fullname)
    Robot full name is RO1148
    """
    def __init__(self):
        super().__init__("Robot")
        self.__focus = False
        self.__number = random.randint(0, 8000) + 1000
        fc = mutants.FileChar.FileChar()
        rifle = fc.getEquipment(">")
        self.pickup(rifle)

    @property
    def focus(self):
        return (self.__focus)

    @focus.setter
    def focus(self, onoff):
        if onoff:
            print("Robot " + self.name + " has focus.")
        self.__focus = onoff

    @property
    def fullname(self):
        return("RO" + str(self.__number))

    @property
    def number(self):
        return(self.__number)

    @number.setter
    def number(self, num):
        self.__number = num


