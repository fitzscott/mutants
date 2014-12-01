__author__ = 'Fitz'

import mutants.PlayerPiece

class Computer(mutants.PlayerPiece.PlayerPiece):
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
        self.message("Without " + self.fullname + " control, robots may not move.")
        self.square.board.cripplerobots()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
