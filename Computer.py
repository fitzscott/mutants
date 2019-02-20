__author__ = 'Fitz'

import PlayerPiece as pp

class Computer(pp.PlayerPiece):
    """
    The Computer controls the robots' movements.  It is a non-moving piece,
    unlike a piece of equipment.
    c = Computer()
    c.damage(20)
    """
    def __init__(self):
        super().__init__("Computer")

    def deathmessage(self):
        self.message("    " + self.fullname + " has been destroyed!")
        self.message("Without " + self.fullname + " control, existing robots may not move.")
        self.square.board.cripplerobots()

    @property
    def hasattacked(self):
        return(True)

    @hasattacked.setter
    def hasattacked(self, att):
        pass    # The computer never attacks, so this is irrelevant.  Still need to define it, though.

    @property
    def indicatorstring(self):
        return "Debris"

if __name__ == "__main__":
    import doctest
    doctest.testmod()
